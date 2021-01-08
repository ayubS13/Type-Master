import pygame
import sys
import random
import math
import enemyShip as enemy
import bullet as bullet

hashSize= 1000 # this is the size of the hashTable (aka dictionary)
Dict = {} # this is the empty dictionary ; aka the hashTable

bulletCollisonImg = pygame.image.load('TexturePacks/Bullets/BlueShots/impactImage.png')
bulletImage = pygame.image.load('TexturePacks/Bullets/BlueShots/blueShot.png')
backgroundImage = pygame.image.load('TexturePacks/Backgrounds/asteroidBackGroundMagnified.jpg')
empImage = pygame.transform.scale(pygame.image.load('TexturePacks/EMP/plasmaEMP.jpg'), (40,40))
spaceShipImage = pygame.transform.scale(pygame.image.load('TexturePacks/Ships/defaultTextures/spaceShip.png'), (50,50))
shockWaveImage = pygame.transform.scale(pygame.image.load('TexturePacks/Shockwave/blue.png'), (50,50))
print(spaceShipImage.get_width(), spaceShipImage.get_height())

white = [255,255,255]
red = [255,0,0]
orange = [229,83,0]
green = [0,100,0]

pygame.init()
width = 900
height = 650
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceforce")

spaceShipX = 420
spaceShipY = 550
spaceShipWidth = 50
spaceShipHeight = 60

points = None
acceleration = 2 #this is the upcoming spaceships speed
crash_sound = pygame.mixer.Sound("soundFiles/crashSound.mp3")

numberOfEnemyShips = 4 # this is how many enemy ships will be in the list by default
enemyShipsList = []
bulletsFiredList = [] # thi si the lsit of bullets fired by the ship

defaultEnemyTypes = ['enemyType1.jpg','enemyType2.jpg','enemyType3.jpg','enemyType4.jpg'] # the 4 types of ship images
defaultImageSizes = [[68,90],[60,63],[87,98],[85,73]] # the 4 types of ships have different sizes

alienEnemyTypes = ['alienBig.png','alienBig2.png','alienMedium1.png','alienMedium2.png','alienMedium3.png']
alienImageSizes = [[100,80],[150,167],[100,124],[100,165],[80,137]]

font = pygame.font.SysFont("Times New Roman", 22) #this is the font we will use to display each word with each enemyship
font2  = pygame.font.SysFont("Times New Roman", 22, True )
font3 = pygame.font.SysFont("Times New Roman", 40, True )

crashed = False

lives = None
gameRound = 1
usingEMP = False
wordsTyped = None
startTime = None

def setHashSize(size):
    if isValidSize(size) is True:
        hashSize = size
    else:
        hashSize = getValidSize(size)
        print('Dictionary Size set to: ' + str(hashSize))

    #after setting the hashSize, initialize the dictionary    
    initDictionary() # loop through the dictionary and initialize the lists

def initDictionary():
    for x in range(1000):
        Dict.setdefault(x, []) # loop through the dictionary and at each key make a list

def isValidSize(temp):
    if temp <= 1:
        return False
    if temp == 2:
        return True
    if(temp % 2 == 0):
        return False
    for i in range (3, temp, 2):
        if(i*i <= temp):
            if (temp %i == 0):
                return False
    return True
    
def getValidSize(size):
    while isValidSize(size) == False:
        size+=1
    return size

#smallWords text file has 1531 words
#largeWords text file has 25143 words
def readFile(fileName = "Data/smallWords.txt", action = "r"):
    temp = 0
    with open(fileName, action) as inputFile:
        for line in inputFile:
            temp +=1
            #print(line.strip('\n'))
            word = line.strip('\n')
            key = getHashKey(word) 
            Dict[key].append(word)
    print("Total Words Read: " + str(temp))       
        

def getHashKey(word):
    num = 131
    total = 0
    for x in word:
        total = (total*num) + ord(x)
    return (total % hashSize) # this is the hashKey that each word is stored at

    
def rotateImage(enemyShipObj, image, angle, xPos, yPos):
    rotated_image = pygame.transform.rotate(image, -angle+90)
    enemyShipObj.setAngle(-angle+90)

    new_rect = rotated_image.get_rect(center = image.get_rect(center = (xPos, yPos)).center)
    return rotated_image, new_rect

def rotateEnemyAndDisplayWord(enemyShipObj, spaceShipX, spaceShipY):
    font = pygame.font.SysFont("Times New Roman", 25) #this is the fond we will use to display each word with each enemyship
    wordPrinted = font.render(enemyShipObj.getWord(), True, enemyShipObj.getColor() )

    mydegrees = math.degrees(math.atan2(spaceShipY-enemyShipObj.getY(), spaceShipX-enemyShipObj.getX()))#get the angle in radians and convert to degrees
    rotated_image, new_rect= rotateImage(enemyShipObj,enemyShipObj.getImage(), mydegrees, enemyShipObj.getX()+enemyShipObj.getWidth()/2, enemyShipObj.getY()+enemyShipObj.getHeight()/2)
    window.blit(rotated_image, new_rect.topleft)

    if ((enemyShipObj.getY() > 0) and (enemyShipObj.getY() < height )):
        if((enemyShipObj.getX() > 0) and (enemyShipObj.getX() < width)):
            window.blit(wordPrinted, (enemyShipObj.getX(),enemyShipObj.getY()-30))
            

def getRandomWord(): # returns a random word from the dictionary of words
    randomKey = random.randrange(0,1000) # get a number between 0 to a 1000, this is the hashkey of each word
    randomIndexInList = random.randrange(0, len(Dict[randomKey]))
    return Dict[randomKey][randomIndexInList]

def unpause():
    pygame.mixer.music.unpause()

def startSound():
    pygame.mixer.music.load("soundFiles/spaceNoise.mp3")
    pygame.mixer.music.play(-1) # this will play the background music indefinitely

def displayDangerLevel():
    # we will use the math.hypot function to get the distance between the enemy ships and the user ship
    # the smaller the distance, the greater the danger

    highestY = 1000
    for temp in enemyShipsList:
        dist = math.hypot(spaceShipX-temp.getX(),spaceShipY-temp.getY())
        if(dist< highestY):
            highestY = dist
        
    if(highestY < 200):
        dangerLvl= font2.render("High", True, red)
        window.blit(dangerLvl, (150, 540))
    elif(highestY > 200 and highestY < 400):
        dangerLvl= font2.render("Medium", True, orange)
        window.blit(dangerLvl, (150, 540))
    elif(highestY > 400):
        dangerLvl= font2.render("Safe", True, green)
        window.blit(dangerLvl, (150, 540))
    
    return highestY
def displayShipAngle(angle):
    angle = font.render(str(round(angle+90, 2)), True, white)
    window.blit(angle, (200,570))

def displayCurrentWord(word):
    displayWord = font2.render(word, True, orange)
    window.blit(displayWord, (90,510))

def displayWPM(totalWords):
    wordsInMinutes = font2.render(str(totalWords), True, white)
    window.blit(wordsInMinutes, (850,50))

def displayStats():
    distance = font.render("Nearest Ship: " + str(round(displayDangerLevel(),2)), True, white)
    trajectory = font.render("Angle of Trajectory:", True, white)
    dangerLevel = font.render("Danger Level:", True, white)
    score = font.render("Score: " + str(points), True, white)
    emp = font.render("EMP's: ", True, white)
    wordsPerMinute = font.render("Words Typed: ", True, white)
    wordTyping = font.render("Typing: ", True, white)

    window.blit(dangerLevel, (10, 540))
    window.blit(trajectory, (10, 570))
    window.blit(distance, (10, 600))
    window.blit(score, (720,600))
    window.blit(emp, (720, 20))
    window.blit(wordsPerMinute, (720, 50))
    window.blit(wordTyping, (10, 510))

    
# this calculates the position of each spaceship
# need rectangle's center, the speed traveling at , and the angle in radians
def calculat_new_xy(old_x, old_y,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_x, new_y

#this calculates the position of each bullet
def calculate_bullet_xy(old_x, old_y,speed, angle_in_radians):
    new_x =old_x+(speed*math.cos(angle_in_radians))
    new_y =old_y+(speed*math.sin(angle_in_radians))
    return new_x, new_y

def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def updateFPS(fps):
    frames = font.render("FPS: " +str(fps), True, (255,255,255))
    window.blit(frames, (720, 570))

def initializeEnemyShips(total):
    global enemyShipsList
    enemyShipsList = [] # reset the enemyShipsList
    for x in range(total):
        randomIndex = random.randrange(0,4) # since there are only 4 types of ships with each unique sizes
        enemyImage = pygame.transform.scale(pygame.image.load("TexturePacks/Ships/defaultTextures/"+defaultEnemyTypes[randomIndex]), (defaultImageSizes[randomIndex]))
        randomWord = getRandomWord()
        randomSpeed = random.randrange(1,acceleration)/10 # random Acceleration
        randomX = random.randrange(0,1200) # random x
        randomY = random.randrange(100,300)*-1 # random y
        randomWidth = enemyImage.get_width() #width of image
        randomHeight = enemyImage.get_height() # height of image

        # create a temporary Enemy ship object given the above generated values
        tempShip = enemy.enemyShip(enemyImage, randomWord, randomX, randomY, randomWidth, randomHeight, randomSpeed)
        enemyShipsList.append(tempShip)
def printBulletsList():
    for x in bulletsFiredList:
        x.toString()

def printEnemyShipsList():
    for x in enemyShipsList:
        x.toString()

def printEMPS():
    firstX = 790
    for x in range(lives):
        window.blit(empImage, (firstX, 10))
        firstX += 30

def useEMP():
    global shockWaveImage
    global lives

    shipsToDelete = [] 
    if(lives > 0):
        for ship in enemyShipsList:
            if(ship.getY() > 200):
                shipsToDelete.append(ship)

        for temp in shipsToDelete:
            enemyShipsList.remove(temp)

        lives -= 1
        printEMPS()
    
    
goRight = True
gotLeft = False
def animateBackground(backgroundXPos, backgroundShiftSpeed):
    global goRight
    global goLeft
    if(goRight == True):
        backgroundXPos -= backgroundShiftSpeed
        if(backgroundXPos <= -600):
            goRight = False
            goLeft = True
    elif(goLeft  == True):
        backgroundXPos += backgroundShiftSpeed
        if(backgroundXPos >= 0):
            goLeft = False
            goRight = True

    return backgroundXPos


def rotateShipByAngle(image, angle, xPos, yPos):
    rotated_image = pygame.transform.rotate(image, angle) # 0 is top, -90 -> -180 right, 90 -> 180 is left
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (xPos, yPos)).center)
    return rotated_image, new_rect

def rotateUserSpaceShip(img, shipLookingAt):
    mydegrees = shipLookingAt.getAngle()
    
    displayShipAngle(mydegrees)
    rotated_image, new_rect= rotateShipByAngle(img, mydegrees, spaceShipX+spaceShipWidth/2, spaceShipY+spaceShipHeight/2)
    window.blit(rotated_image, new_rect.topleft)

def shipsCrashed(enemyX, enemyY, enemyWidth, enemyHeight):
    #the crash ship sound
    pygame.mixer.Sound.play(crash_sound).set_volume(.1)
    quitGame()

def roundCompleted(gameRound):
    gmr =  font3.render("Round " + str(gameRound), True, white)
    window.blit(gmr, (20,10))

def rotateBulletByAngle(bulletImg, angle, xPos, yPos):
    rotated_image = pygame.transform.rotate(bulletImg, angle) # 0 is top, -90 -> -180 right, 90 -> 180 is left
    new_rect = rotated_image.get_rect(center = bulletImg.get_rect(center = (xPos, yPos)).center)
    return rotated_image, new_rect

def rotateBulletAndPrint(bullet, target):
    #the bullets angle and targets angle match
    #print(bullet.getAngle(), target.getAngle())
    
    # the bullet images are rotated properly, but the x and y positions are off
    rotatedImage, bulletRectangle = rotateBulletByAngle(bullet.getImage(), bullet.getAngle(), bullet.getX(), bullet.getY())
    window.blit(rotatedImage, bulletRectangle.topleft)

def addNewBullet(shipFacing):
    bulletTrajectory = shipFacing.getAngle() #this is the initial angle the bullet is facing
    bulletInitialX = 440
    bulletInitialY = 550
    bulletWidth = bulletImage.get_width()
    bulletHeight = bulletImage.get_height()
    bulletSpeed = -20 

    bulletFired = bullet.bullet(bulletImage, bulletInitialX, bulletInitialY, bulletWidth, bulletHeight, bulletSpeed, bulletTrajectory, shipFacing)
    bulletsFiredList.append(bulletFired)

def getRotatedImpactImage(blt):
    rotated_image = pygame.transform.rotate(bulletCollisonImg, blt.getAngle())
    xPos = blt.getShipHeadedTowards().getX() + blt.getShipHeadedTowards().getWidth()/2
    yPos = blt.getShipHeadedTowards().getY() + blt.getShipHeadedTowards().getHeight()/2
    new_rect = rotated_image.get_rect(center = blt.getImage().get_rect(center = (xPos, yPos)).center)

    print("Yollo")
    return rotated_image, new_rect

def startGame():
    global numberOfEnemyShips
    global points
    global acceleration
    global crashed 
    global lives
    global gameRound
    global gameRound
    global wordsTyped
    global usingEMP
    global bulletCollisonImg

    wordsTyped = 0
    lives = 3
    points = 0
    gameRunning = True
    magnifier = 60
    locationY = spaceShipY+spaceShipHeight/2
    locationX = spaceShipX+spaceShipWidth/2

    time= pygame.time.Clock()

    backgroundXPos = 0
    backgroundShiftSpeed = .2
    startSound()
    
    currentWord = ""
    indexOfOriginal = -1

    #this is where the ship is initially looking at, straight up ahead
    shipLookingAt = enemy.enemyShip(None, "pointing to", width/2, height/2, 10, 10, .1)
    currentWord = ""

    while gameRunning:
        
        window.blit(backgroundImage, (backgroundXPos,0)) # cover the sceen with the backgroundImage
        printEMPS()
        backgroundXPos = animateBackground(backgroundXPos, backgroundShiftSpeed) #animate the background  
        
        #the enemy list has all the correct attributes assigned including the angle of trajectory
        #printEnemyShipsList()
        first = True
        if(first == True):
            roundCompleted(gameRound)
            first = False


        displayStats() # display the side stats
        displayCurrentWord(currentWord)
        updateFPS(str(int(time.get_fps()))) # display the FPS 
        displayWPM(wordsTyped)  

        index = -1
        if (len(enemyShipsList) == 0):
            numberOfEnemyShips += 2
            acceleration += 1
            gameRound +=  1
            roundCompleted(gameRound)
            initializeEnemyShips(numberOfEnemyShips)

        
        if(usingEMP == True):
            shockWaveImage = pygame.transform.scale(pygame.image.load('TexturePacks/Shockwave/blue.png'), (magnifier, magnifier))
            window.blit(shockWaveImage, (locationX,locationY))
            magnifier += 10
            locationY -= 5
            locationX -= 5.5
            
            if(locationY <= 250):
                magnifier = 60
                locationY = spaceShipY+spaceShipHeight/2
                locationX = spaceShipX+spaceShipWidth/2
                usingEMP = False

        if(crashed == False):
            # will need a for loop here that will iterate through the bullets list and move them accross the screen
            if(len(bulletsFiredList) > 0):
                for bl in bulletsFiredList: #detect whether the bullet hits the target
                    if(bl.getY() < 0 or bl.getX() < 0 or bl.getY() > 700 or bl.getX() > 900):
                        bulletsFiredList.remove(bl)

                    # we can use the pygame collideRect method to see if the enemy spaceSihp collides with the homespaceship
                    target = bl.getShipHeadedTowards()
                    targetRect = pygame.Rect(target.getX(), target.getY(), target.getWidth(), target.getHeight())
                    bulletRect = pygame.Rect(bl.getX(), bl.getY(), bl.getWidth(), bl.getHeight())
                    if (targetRect.colliderect(bulletRect)):
                        # if the bullet collides with the target rectangle, do the impactImage animation
                        if(len(bulletsFiredList) > 0):
                            bulletsFiredList.remove(bl)
                            

                for blt in bulletsFiredList:
                    target = blt.getShipHeadedTowards() # the target of the current bullet
                    bulletX, bulletY = calculate_bullet_xy(blt.getX(), blt.getY(), blt.getSpeed(), target.getRadians())
                    #print(bulletX, bulletY)
                    blt.setX(bulletX)
                    blt.setY(bulletY)
                    # we update the values of the bullelts
                    #then call the rotateBulletAnd Print Method
                    rotateBulletAndPrint(blt, target)

            for temp in enemyShipsList: # iterate through each enenyShip object in the
                
                         
                index +=1 # this will iterate through 0 to enemyShipsList size -1      

                enemyXPos = 0
                enemyYPos = 0

                #this bit of code allows the enemy spaceships to travel at an angle accross the screen
                angleInRadians= math.atan2(spaceShipY-temp.getY(), spaceShipX-temp.getX())
                angleInRaidansForBullets = math.atan2(spaceShipY-temp.getY()-temp.getHeight()/2, spaceShipX-temp.getX()-temp.getWidth()/2)
                temp.setRadians(angleInRaidansForBullets)
                enemyXPos, enemyYPos = calculat_new_xy(temp.getX(), temp.getY(), temp.getAcceleration(), angleInRadians)
                temp.setX(enemyXPos)
                temp.setY(enemyYPos)

                #printEnemyShipsList()
                # this method rotates the enemy image to the correct angle and moves it across the screen
                rotateEnemyAndDisplayWord(temp, spaceShipX, spaceShipY)#display the word
                
                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        gameRunning = False
                
                    if event.type == pygame.KEYDOWN: # key down is for if a key is pressed 
                        if(pygame.key.name(event.key) == 'return'):
                            if(lives > 0):
                                useEMP()
                                currentWord = ""
                                usingEMP = True
                                magnifier = 60
                                locationY = spaceShipY+spaceShipHeight/2
                                locationX = spaceShipX+spaceShipWidth/2

                        alphabet = str(event.unicode)
                        for x in range(len(enemyShipsList)):
                            #this if statement grabs the word associated with the first letter you startTyping
                            #print(currentWord)
                            if(enemyShipsList[x].getWord()[0:1] == alphabet and len(currentWord) == 0):
                                #print("this is the word and index:",x, currentWord)
                                #print(enemyShipsList[x].getWord())

                                currentWord = enemyShipsList[x].getWord()
                                enemyShipsList[x].word = currentWord = enemyShipsList[x].word[1:] # remove the first letter and set it to currentword
                                displayCurrentWord(currentWord)
                                # this changes the color of the text to be displayed to be red
                                enemyShipsList[x].setColor(orange) 
                                indexOfOriginal = x # this is where the first word we get is located

                                shipLookingAt = enemyShipsList[x] #gets the enemy ship whose word we are currently editing
                                rotateUserSpaceShip(spaceShipImage,  shipLookingAt) 
                                
                                #add a new bullet every time a key is typed and a letter is removed from the word
                                addNewBullet(shipLookingAt)
                                #used to turn the homeship to face the enemyShip
                                #the shooting sound
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound("soundFiles/shotFired.mp3"))
                                
                        #print(indexOfOriginal, index)
                        if(len(currentWord) > 0): # if the index matches and the key typed matches 
                            #print(alphabet, currentWord)
                            if (alphabet == currentWord[0:1] and indexOfOriginal < len(enemyShipsList)):#if(enemyShipsList[x].getWord() == currentWord):
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound("soundFiles/shotFired.mp3"))
                                currentWord = currentWord[1:]
                                displayCurrentWord(currentWord)
                                enemyShipsList[indexOfOriginal].word = currentWord

                                #add a new bullet every time a key is typed and a letter is removed from the word
                                addNewBullet(shipLookingAt)

                            if(len(currentWord)== 0 and indexOfOriginal < len(enemyShipsList)):
                                #printEnemyShipsList()
                                #print(indexOfOriginal)
                                del enemyShipsList[indexOfOriginal]
                                points += 100
                                currentWord = ""
                                indexOfOriginal = -1
                                wordsTyped += 1

                    rotateEnemyAndDisplayWord(temp, spaceShipX, spaceShipY)#display the word
                    #pygame.display.flip()

                # here we will try to detect if the enemyShip has crashed in to our homeShip
                # we can use the pygame collideRect method to see if the enemy spaceSihp collides with the homespaceship
                enemyRect = pygame.Rect(temp.getX(), temp.getY(), temp.getWidth(), temp.getHeight())
                spaceShipRect  = pygame.Rect(spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight)
                if (enemyRect.colliderect(spaceShipRect)):
                    #the crash animation goes here
                    shipsCrashed(temp.getX(), temp.getY(), temp.getWidth(), temp.getHeight())
                    crashed = True

                #the default place the spaceship is looking at
                rotateUserSpaceShip(spaceShipImage,  shipLookingAt) 

            pygame.display.flip() 
            ticks = time.tick(3000) # framerate, the lower the number the slower the objects move
        
            

def main():
    setHashSize(50000) # set the hash size to roughly 50,000
    readFile("Data/largeWords.txt", "r") # read in the file
    initializeEnemyShips(numberOfEnemyShips) # the default number of enemy ships are 4
    startGame()

main()
