class enemyShip:
    image = None
    word = None
    x= None
    y = None
    height = None
    width = None
    speed = None
    color = [255,255,255]
    angleHeaded = 0
    raidans = None

    def __init__(self, image, word, x, y, width, height, speed):
        self.image = image
        self.word = word
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self. speed = speed

    def getRadians(self):
        return self.radians
        
    def getAngle(self):
        return self.angleHeaded

    def getColor(self):
        return self.color

    def getWord(self):
        return self.word
        
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getAcceleration(self):
        return self.speed

    def getImage(self):
        return self.image

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setColor(self, color):
        self.color = color

    def setAngle(self, angle):
        self.angleHeaded = angle

    def setRadians(self, radians):
        self.radians = radians

    def toString(self):
        print("Word:",self.word,"XPos:", self.x, "YPos:",self.y, "Width:", self.width, "Height:", self.height, "Speed", self.speed, "Angle Facing", self.angleHeaded)

