import tkinter
import pygame
import sys
import random
import math
import enemyShip as enemy
#this will be used for animation



hashSize= 1000 # this is the size of the hashTable (aka dictionary)
Dict = {} # this is the empty dictionary ; aka the hashTable

backgroundImage = pygame.image.load('TexturePacks/Backgrounds/asteroidBackGround.jpg')
#load the spaceShip image and transform it to the desired size
spaceShipImage = pygame.transform.scale(pygame.image.load('TexturePacks/Ships/defaultTextures/spaceShip.png'), (50,50))
print(spaceShipImage.get_width(), spaceShipImage.get_height())

white = [255,255,255]

pygame.init()
width = 900
height = 650
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('First Game')

spaceShipX = 420
spaceShipY = 550
spaceShipWidth = 50
spaceShipHeight = 60

acceleration = .4 #this is the upcoming spaceships speed
crash_sound = pygame.mixer.Sound("soundFiles/crashSound.mp3")

numberOfEnemyShips = 4 # this is how many enemy ships will be in the list by default
enemyShipsList = []

defaultEnemyTypes = ['enemyType1.jpg','enemyType2.jpg','enemyType3.jpg','enemyType4.jpg'] # the 4 types of ship images
defaultImageSizes = [[68,90],[60,63],[87,98],[85,73]] # the 4 types of ships have different sizes

alienEnemyTypes = ['alienBig.png','alienBig2.png','alienMedium1.png','alienMedium2.png','alienMedium3.png']
alienImageSizes = [[100,80],[150,167],[100,124],[100,165],[80,137]]

font = pygame.font.SysFont("Times New Roman", 22) #this is the fond we will use to display each word with each enemyship

def setHashSize(size):
    if isValidSize(size) is True:
        hashSize = size
    else:
        hashSize = getValidSize(size)
        print('Dictionary Size set to: ' + str(hashSize))

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

def getWordInDict(key, word):
    for x in Dict[key]:
        #,print(x)
        if(x == word):
            print("word is found")

def displaySpaceShip():
    window.blit(spaceShipImage, (spaceShipX, spaceShipY))
    

def rotateEnemyAndDisplayWord(enemyImage,enemyPositionX, enemyPositionY, enemyWidth, enemyHeight, spaceShipX, spaceShipY, randomWord):
    font = pygame.font.SysFont("Times New Roman", 25) #this is the fond we will use to display each word with each enemyship
    wordPrinted = font.render(randomWord, True, (255,255,255) )

    mydegrees = math.degrees(math.atan2(spaceShipY+20-enemyPositionY, spaceShipX+20-enemyPositionX))#get the angle in radians and convert to degrees
    rotated_image, new_rect= rotateImage(enemyImage, mydegrees, enemyPositionX+enemyWidth/2, enemyPositionY+enemyHeight/2)
    window.blit(rotated_image, new_rect.topleft)

    if ((enemyPositionY > 0) and (enemyPositionY < height )):
        if((enemyPositionX > 0) and (enemyPositionX < width)):
            window.blit(wordPrinted, (enemyPositionX,enemyPositionY-30))
            

def getRandomWord(): # returns a random word from the dictionary of words
    randomKey = random.randrange(0,1000) # get a number between 0 to a 1000, this is the hashkey of each word
    randomIndexInList = random.randrange(0, len(Dict[randomKey]))
    return Dict[randomKey][randomIndexInList]

def rotateImage(image, angle, xPos, yPos):
    rotated_image = pygame.transform.rotate(image, -angle+90)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (xPos, yPos)).center)
    return rotated_image, new_rect

def crash():
    pygame.mixer.Sound.play(crash_sound).set_volume(.1)
    pygame.mixer.music.pause()
    print("crashed")

def unpause():
    pygame.mixer.music.unpause()

def startSound():
    pygame.mixer.init() 
    pygame.mixer.music.load("soundFiles/spaceNoise.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play() 

def displayStats():
    distance = font.render("Nearest Ship:", True, (255,255,255))
    trajectory = font.render("Angle of Trajectory:", True, (255,255,255))
    dangerLevel = font.render("Danger Level:", True, (255,255,255))
    lives = font.render("Lives Left:", True, (255,255,255))
    score = font.render("Score:", True, (255,255,255))

    window.blit(lives, (10,510))
    window.blit(dangerLevel, (10, 540))
    window.blit(trajectory, (10, 570))
    window.blit(distance, (10, 600))
    window.blit(score, (720,600))
    

# need rectangle's center, the speed traveling at , and the angle in radians
def calculat_new_xy(old_x, old_y,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_x, new_y

def quitGame():
    while True:
        print("the game has ended")
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
        randomSpeed = random.randrange(1,4)/10 # random Acceleration
        randomX = random.randrange(0,1200) # random x
        randomY = random.randrange(100,300)*-1 # random y
        randomWidth = enemyImage.get_width() #width of image
        randomHeight = enemyImage.get_height() # height of image

        # create a temporary Enemy ship object given the above generated values
        tempShip = enemy.enemyShip(enemyImage, randomWord, randomX, randomY, randomWidth, randomHeight, randomSpeed)
        enemyShipsList.append(tempShip)




def printEnemyShipsList():
    for x in enemyShipsList:
        x.toString()

goRight = True
gotLeft = False
def animateBackground(backgroundXPos, backgroundShiftSpeed):
    global goRight
    global goLeft
    if(goRight == True):
        backgroundXPos -= backgroundShiftSpeed
        if(backgroundXPos <= -200):
            goRight = False
            goLeft = True
    elif(goLeft  == True):
        backgroundXPos += backgroundShiftSpeed
        if(backgroundXPos >= 0):
            goLeft = False
            goRight = True

    return backgroundXPos



def startGame():
    global numberOfEnemyShips
    gameRunning = True

    time= pygame.time.Clock()
    ticks = 0

    backgroundXPos = 0
    backgroundShiftSpeed = .2
    startSound()

    currentWord = ""
    indexOfOriginal = -1

    while gameRunning:
        window.blit(backgroundImage, (backgroundXPos,0)) # cover the sceen with the backgroundImage
        
        backgroundXPos = animateBackground(backgroundXPos, backgroundShiftSpeed) #animate the background       
        displaySpaceShip() #display the homeship
        displayStats() # display the side stats
        updateFPS(str(int(time.get_fps()))) # display the FPS


        #after all the enemyShips in the current/default list have been destroyed, make a new List
        """
        if(len(enemyImageList) == 0):
            numberOfEnemyShips += 1
            addNewEnemyShips()
            printLists()
            numberOfEnemyShips -=1
        """

        currentWord = ""
        index = 0
        for temp in enemyShipsList: # iterate through each enenyShip object in the     
            index +=1 # this will iterate through 0 to enemyShipsList size -1      
            
            enemyXPos = 0
            enemyYPos = 0

            #this bit of code allows the enemy spaceships to travel at an angle accross the screen
            angleInRadians= math.atan2(spaceShipY-temp.getY(), spaceShipX-temp.getX())
            enemyXPos, enemyYPos = calculat_new_xy(temp.getX(), temp.getY(), temp.getAcceleration(), angleInRadians)
            temp.setX(enemyXPos)
            temp.setY(enemyYPos)

            #printEnemyShipsList()
            # this method rotates the enemy image to the correct angle and moves it across the screen
            rotateEnemyAndDisplayWord(temp.getImage(), temp.getX(), temp.getY(), temp.getWidth(), temp.getHeight(), spaceShipX, spaceShipY, temp.getWord())#display the word
            
            # if the are looking at the ship whose words have all been typed
            # then remove it
            """
            if(indexOfOriginal == x and (len(enemyWordList[indexOfOriginal]) == 0)):  
                removeEnemyShips(indexOfOriginal)
                indexOfOriginal = -1      
                currentWord = ""      
            """   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                if event.type == pygame.KEYDOWN: # key down is for if a key is pressed ; pygame.key.name(event.key)
                    for x in range(len(enemyShipsList)):

                        if(enemyShipsList[x].getWord()[0:1] == pygame.key.name(event.key) and len(currentWord) == 0):
                            currentWord = enemyShipsList[x].getWord()
                            enemyShipsList[x].word = currentWord = enemyShipsList[x].word[1:]
                            indexOfOriginal = x 
                    """
                    if(pygame.key.name(event.key) == temp.getWord()[0:1] and len(currentWord) == 0):# if the first letter typed is the randomword and currentWOrd is empty
                        currentWord = temp.getWord()
                        temp.word = temp.word[1:]
                        indexOfOriginal = index"""

                    if((indexOfOriginal == index) and (pygame.key.name(event.key) == temp.getWord()[0:1])): # if the index matches and the key typed matches 
                        temp.word = temp.word[1:]                
                    if(len(enemyShipsList[indexOfOriginal].word)== 0):
                        print("reset the current word")
                        currentWord = ""
                        indexOfOriginal = -1

                rotateEnemyAndDisplayWord(temp.getImage(), temp.getX(), temp.getY(), temp.getWidth(), temp.getHeight(), spaceShipX, spaceShipY, temp.getWord())#display the word
                #pygame.display.flip()

            # here we will try to detect if the enemyShip has crashed in to our homeShip
            # we can use the pygame collideRect method to see if the enemy spaceSihp collides with the homespaceship
            enemyRect = pygame.Rect(temp.getX(), temp.getY(), temp.getWidth(), temp.getHeight())
            spaceShipRect  = pygame.Rect(spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight)
            if (enemyRect.colliderect(spaceShipRect)):

                #the crash animation goes here
                s = pygame.Surface((spaceShipWidth,spaceShipHeight))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill((255,255,255))           # this fills the entire surface
                window.blit(s, (spaceShipX,spaceShipY)) 

                q = pygame.Surface((temp.getWidth(),temp.getHeight()))  # the size of your rect
                q.set_alpha(128)                # alpha level
                q.fill((255,255,0))           # this fills the entire surface
                window.blit(q, (temp.getX(),temp.getY())) 
                #pygame.draw.rect(window, pygame.Color(255, 255, 255), (spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight))
                pygame.display.flip()
                crash()
                quitGame()

        pygame.display.flip()
        ticks = time.tick(300) # framerate, the lower the number the slower the objects move
        

def main():
    setHashSize(50000) # set the hash size to roughly 50,000
    initDictionary() # loop through the dictionary and initialize the lists
    readFile("Data/largeWords.txt", "r") # read in the file
    initializeEnemyShips(numberOfEnemyShips) # the default number of enemy ships are 4
    printEnemyShipsList()
    startGame()
    

main()

"""
    print("collision detected")
    #print(spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight)
    #print(enemyXPos, enemyYPos, enemyWidth, enemyHeight)
    
    
    #gameOver screen Fade out
    s = pygame.Surface((1000,750))
    s.set_alpha(128)                
    s.fill((255,255,255))          
    window.blit(s, (0,0)) 

    s = pygame.Surface((spaceShipWidth,spaceShipHeight))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    window.blit(s, (spaceShipX,spaceShipY)) 

    q = pygame.Surface((enemyWidth,enemyHeight))  # the size of your rect
    q.set_alpha(128)                # alpha level
    q.fill((255,255,0))           # this fills the entire surface
    window.blit(q, (enemyXPos,enemyYPos)) 
    #pygame.draw.rect(window, pygame.Color(255, 255, 255), (spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight))
    pygame.display.update()
    """