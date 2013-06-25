#Simulating robots

import math
import random

import robo_visualize
import pylab

# For Python 2.7:
from robo_verify_movement27 import testRobotMovement


position_change=0




class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)



class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.tile={}
        self.width=width
        self.height=height
        for i in range(0,width):
            for j in range(0,height):
                self.tile[(float(i),float(j))]=False
        self.noOfTilesCleaned=0
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        temp=(math.floor(pos.getX()),math.floor(pos.getY()))
        if temp in self.tile and self.tile[temp]!=True:
            self.tile[temp]=True
            self.noOfTilesCleaned+=1
        
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        temp=(math.floor(m),math.floor(n))
        if self.tile[temp]==True:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height
        

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return self.noOfTilesCleaned
        

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """        
        return Position(random.randrange(0,self.width),random.randrange(0,self.height))

    def getFixedPosition(self):
        """"
        Return a fixed position inside the room.

        returns a Position Object.
        """
        return Position(0.2,0.2)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX()<float(self.width) and pos.getY()<float(self.height) and pos.getX() >=0 and pos.getY() >=0
        



#hardCodedRobot
class HardRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.room=room
        self.speed=speed
        self.direction=90
        self.position=self.room.getFixedPosition()
        self.room.cleanTileAtPosition(self.position)        
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """       
        return self.position
        
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
        

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position=position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction=direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError

class HardWiredRobot(HardRobot):
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        temp=self.position.getNewPosition(self.direction,self.speed)
        if(self.room.isPositionInRoom(temp)): 
            self.position=self.position.getNewPosition(self.direction,self.speed)
            if (self.room.isTileCleaned(math.floor(self.position.x),math.floor(self.position.y))) == False:
                self.room.cleanTileAtPosition(self.position)
            if(self.direction==360)and self.position.x<1:
                self.direction=90
            if(self.direction==360):
                self.direction=270
        else:
            self.setRobotDirection(360)
            return self.position                 


    

#StandardRobot
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.room=room
        self.speed=speed
        self.direction=random.randint(0,359)
        self.position=self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)        
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """       
        return self.position
        
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
        

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position=position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction=direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError

class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        temp=self.position.getNewPosition(self.direction,self.speed)
        if(self.room.isPositionInRoom(temp)): 
            self.position=self.position.getNewPosition(self.direction,self.speed)
            if (self.room.isTileCleaned(math.floor(self.position.x),math.floor(self.position.y))) == False:
                self.room.cleanTileAtPosition(self.position)
        else:
            self.setRobotDirection(random.randint(0,359))
            return self.position                 


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    average_time_Steps=[]
    counter=num_trials
    num=num_robots
    while(num_robots!=0):
        while num_trials!=0:
            room=RectangularRoom(width,height)
            aRobot=robot_type(room,speed)
            average=0
            while get_coverage(aRobot,room)<min_coverage:
                aRobot.updatePositionAndClean()
                average+=1
            average_time_Steps.append(average)            
            num_trials-=1
        result=0
        num_robots-=1
    for i in average_time_Steps:
        result+=i
    result=int(result/counter)
    
    
        
    return math.floor(result/num)

def get_coverage(aRobot,room):
    
    return float(aRobot.room.getNumCleanedTiles())/float(aRobot.room.getNumTiles())


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        temp=self.position.getNewPosition(self.direction,self.speed)
        if(self.room.isPositionInRoom(temp)): 
            self.position=self.position.getNewPosition(self.direction,self.speed)
            if (self.room.isTileCleaned(math.floor(self.position.x),math.floor(self.position.y))) == False:
                self.room.cleanTileAtPosition(self.position)
            self.setRobotDirection(random.randint(0,359))
        else:
            self.setRobotDirection(random.randint(0,359))
            return self.position

class LateralWalkRobot(Robot):
    """changing locations at 180 degree"""
    def updatePositionAndClean(self):
        temp=self.position.getNewPosition(self.direction,self.speed)
        if(self.room.isPositionInRoom(temp)): 
            self.position=self.position.getNewPosition(self.direction,self.speed)
            if (self.room.isTileCleaned(math.floor(self.position.x),math.floor(self.position.y))) == False:
                self.room.cleanTileAtPosition(self.position)
            self.setRobotDirection(random.randint(0,179))
        else:
            self.setRobotDirection(random.randint(0,179))
            return self.position

#testing hardwired robot here replace HardWiredRobot by StandardRobot or RandomWalkRobot to see different results.
testRobotMovement(HardWiredRobot, RectangularRoom)
testRobotMovement(StandardRobot, RectangularRoom)
testRobotMovement(RandomWalkRobot, RectangularRoom)








def showPlot1(title, x_label, y_label):
    """
    tie it takes 1-10 robots  to clean 80% of a room.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
        times3.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, HardWiredRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot','HardWiredRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
#displaying graph -1
showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room","Number of Robots","Time-steps")
def showPlot2(title, x_label, y_label):
    """
    Time it takes for a robot to clean 80% of various shaped rooms
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
#showPlot2("Time It Takes A Robot To Clean 80% Of Variously Shaped Rooms","Aspect Ratio","Time-steps")  
