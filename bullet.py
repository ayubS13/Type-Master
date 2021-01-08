class bullet:
    image = None
    x= None
    y = None
    width = None
    height = None
    speed = None
    angleHeaded = 0
    shipHeadedTowards = None

    def __init__(self, image, x, y, width, height, speed, angleHeaded, shipHeadedTowards):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.angleHeaded = angleHeaded
        self.shipHeadedTowards = shipHeadedTowards

    def getShipHeadedTowards(self):
        return self.shipHeadedTowards

    def getAngle(self):
        return self.angleHeaded
        
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getSpeed(self):
        return self.speed

    def getImage(self):
        return self.image   

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setImage(self, image):
        self.image = image

    def setAngle(self, angle):
        self.angleHeaded = angle

    def setShipHeadedTowards(self, shipHeadedTowards):
        self.shipHeadedTowards = shipHeadedTowards
        
    def toString(self):
        print("XPos:", self.x, "YPos:",self.y, "Width:", self.width, "Height:", self.height, "Speed", self.speed, "Angle Facing", self.angleHeaded)