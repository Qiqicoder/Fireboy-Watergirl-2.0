from xml.dom.minidom import CharacterData
from cmu_graphics import *
from PIL import Image
import os, pathlib
from Character import Character
from Obstacles import Obstacles, GameClearDoor, gameClearFunction
from Button import Button, helpMenuButtonFunction, gameScreen, pauseButtonFunction

def onAppStart(app):
#________startScreen____________________________________________________________
    #button#
    app.startButtList = [Button(400,300,20,gameScreen, "", 'StartGame',align = "center"),
                    Button(400,400,20,helpMenuButtonFunction, "", 'HelpMenu',align = "center")]
    app.textVisible = False
    #background_StartImage#
    app.startImage = Image.open("images/startScreenBackground.jpg")
    app.startImageWidth, app.startImageHeight = app.startImage.width, app.startImage.height
    app.startImage = CMUImage(app.startImage)
    #titleImage#
    app.gameNameImage = Image.open("images/gameName.png")
    app.gameNameImageWidth,app.gameNameImageHeight = app.gameNameImage.width,app.gameNameImage.height
    app.gameNameImage = CMUImage(app.gameNameImage)
    #watergirlImage#
    spritestripW = Image.open('images/watergirlStanding.png')
    app.spritesW = []
    for i in range(14):
        frameF = spritestripW.crop((100*i, 0, 100+100*i, 140))
        spriteW = CMUImage(frameF)
        app.spritesW.append(spriteW)
    #fireboyImage#
    spritestripF = Image.open('images/fireboyStanding.png')
    app.spritesF = []
    for i in range(8):
        frameF = spritestripF.crop((100*i, 0, 100+100*i, 140))
        spriteF = CMUImage(frameF)
        app.spritesF.append(spriteF)
    app.spriteCounter = 0
    app.stepCounter = 0
    app.stepsPerSecond = 50
#________gameScreen_____________________________________________________________
    #background_GameImage#
    app.gameImage = Image.open("images/gameBackground.jpg")
    app.gameImageWidth,app.gameImageHeight = app.width,app.height
    app.gameImage = CMUImage(app.gameImage)
    #characterImage#
    app.fireboy = Character('images/fireboyStandingSingle.png', 50, 450, 0.5)
    # app.fireboyList = []
    # for i in range(14):
    #     framefireboy = spritesfireboy.crop((100*i, 0, 100+100*i, 140))
    #     fireboytype = CMUImage(framefireboy)
    #     app.fireboyList.append(fireboytype)
    app.watergirl = Character('images/watergirlStandingSingle.png', 700, 400, 0.5)
    # app.watergirlList = []
    # for i in range(14):
    #     framewatergirl = spriteswatergirl.crop((100*i, 0, 100+100*i, 140))
    #     watergirltype = CMUImage(framewatergirl)
    #     app.watergirlList.append(watergirltype)
    app.characterList = [app.fireboy, app.watergirl]
    app.move = 5
    #obstacle#
    app.obstacleList = [
        Obstacles(0, 480, 800, 20),
        Obstacles(0, 0, 800, 20),
        Obstacles(0, 0, 20, 500),
        Obstacles(780, 0, 20, 500),

        Obstacles(0, 400, 150, 20),
        Obstacles(650, 400, 150, 20),
        Obstacles(200, 300, 500, 20),
        Obstacles(600, 200, 200, 20),
        Obstacles(200, 100, 100, 20),
        Obstacles(600, 100, 100, 20),
    ]
    #hoorimage#
    app.gameClearVisible = False
    app.fireboyDoor = GameClearDoor('images/fireboyDoor.png', 220, 40, gameClearFunction,0.5)
    app.watergirlDoor = GameClearDoor('images/watergirlDoor.png', 620, 40, gameClearFunction, 0.5)
    app.characterDoorList = [app.fireboyDoor, app.watergirlDoor]
    #button#
    app.pause = False #it should stop the character moving.
    app.gameButtList = [Button(750,20,20,pauseButtonFunction, "blue", 'PAUSE')]
#_______________StartScreen_____________________________________________________
def start_onStep(app):
    app.stepCounter += 1
    if app.stepCounter>= 8:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesW)
        app.stepCounter = 0 
    
    app.stepCounter += 1
    if app.stepCounter>= 8:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesF)
        app.stepCounter = 0 

def start_redrawAll(app):
    # drawRect(0,0,app.width,app.height,fill ="pink")
    drawImage(app.startImage, 0,0,width = app.width, height = app.height, opacity=80)
    newWidth, newHeight = (app.gameNameImageWidth/1.2, app.gameNameImageHeight/1.2)
    drawImage(app.gameNameImage, 400,100,width = newWidth, height = newHeight, align = "center")
    # drawLabel('Fireboy and Watergirl',400,50,size=50,bold=True, align = 'center')
    for butt in app.startButtList:
        butt.draw()
    if app.textVisible:
        drawLabel("helpMenuButtonbalabala", app.width//2, app.height//2, 
                  fill = "black", align = "center")
    spriteW = app.spritesW[app.spriteCounter]
    drawImage(spriteW,150, 400, align = 'center')
    
    spriteF = app.spritesF[app.spriteCounter]
    drawImage(spriteF,650, 400, align = 'center')
    
def start_onMousePress(app, mouseX, mouseY):
    for butt in app.startButtList:
        if butt.checkForPress(app, mouseX, mouseY):
            setActiveScreen("next")
#_______________gameScreen______________________________________________________
def next_onKeyPress(app,key):
    if key == 'p':
        setActiveScreen("start")
def next_redrawAll(app):
    newWidth, newHeight = (app.gameImageWidth,app.gameImageHeight)
    drawImage(app.gameImage,0,0,width=newWidth,height=newHeight,opacity=100)
    drawLabel("Fireboy&Watergirl", 120, 30, size=16)
    drawLabel("Press ↑↓←→ to move the Fireboy", 120, 50)
    drawLabel("Press wsad to move the Watergirl", 120, 70)
    #obstacle#
    for obstacle in app.obstacleList:
        obstacle.drawObstacles()
    #Door#
    app.fireboyDoor.drawDoor()
    app.watergirlDoor.drawDoor()
    #character#
    app.fireboy.drawCharacter()
    app.watergirl.drawCharacter()
    #button#
    for butt in app.gameButtList:
        butt.draw()
    if app.pause:
        drawRect(400,250,app.width-100, app.height//2, 
                  fill = "grey", align = "center")
        drawLabel("PAUSED", app.width//2, app.height//2-80, 
                  fill = "black", align = "center",size = 50)
        drawLabel("END", app.width//2-200, app.height//2, 
                  fill = "black", align = "center",size = 40)
        drawLabel("RETRY", app.width//2+170, app.height//2, 
                  fill = "black", align = "center",size = 40)
        drawLabel("BACK", app.width//2, app.height//2+80, 
                  fill = "black", align = "center",size = 40)
    # sprite = app.sprites[app.spriteCounter]
    # drawImage(sprite,200, 200)
    #Door_checkForWin#
    # if app.fireboyDoor.checkForWin(app, app.fireboy) and app.watergirlDoor.checkForWin(app, app.watergirl):
    #     pass
    if app.gameClearVisible:    
        drawLabel("You win the game", app.width//2, app.height//2, 
                fill = "red", align = "center", size = 40)

def next_onMousePress(app, mouseX, mouseY):
    for butt in app.gameButtList:
        if butt.checkForPress(app, mouseX, mouseY):
            setActiveScreen("start")

def next_defKeyHold(app, character, keys, left, right):
    if right in keys and left not in keys:
        character.x += app.move
        character.moving = True
        if character.x > app.width - character.imageWidth:
            character.x = character.imageWidth

    elif left in keys and right not in keys:
        character.x -= app.move
        character.moving = True
        if character.x < character.imageWidth:
            character.x = app.width - character.imageWidth

def next_onKeyPress(app, keys):
    if 'up' in keys and not app.fireboy.drop:
        print("upin")
        app.fireboy.jumping()
    if 'w' in keys and not app.watergirl.drop:
        app.watergirl.jumping()

def next_onKeyHold(app, keys):
    next_defKeyHold(app, app.fireboy, keys, 'left', 'right')
    next_defKeyHold(app, app.watergirl, keys, 'a', 'd')

def next_onStep(app): 
    #character&obstacle_collision#
    for character in app.characterList:
        characterDrop(app, character)
        if character.drop:
            characterJump(app, character)
        for obstacle in app.obstacleList:
            collisionField = obstacle.collisionField(character)
            if collisionField != None:
                print(collisionField)
                character.standField = collisionField
                character.adjustMove()
                if not character.drop:
                    character.y = obstacle.y - character.imageHeight
    #character&door_collision#
    for i in range(2):
        chardoor = app.characterDoorList[i]
        character = app.characterList[i]
        if (chardoor.x + chardoor.width/2 - 10 < character.x + character.imageWidth/2 < chardoor.x + chardoor.width/2 + 10 and 
            chardoor.y < character.y + character.imageHeight and 
            character.y < chardoor.y + chardoor.height):
            character.win = True

    if app.characterList[0].win and app.characterList[1].win:
        app.gameClearVisible = True

def characterJump(app, character):
    if character.y <= app.height - character.imageHeight:
        character.takeStep()
        character.y = max(100, character.y)
    else:
        character.drop = False

def characterDrop(app, character):
    if character.standField != None:
        left, right = character.standField
        if character.x + character.imageHeight/2 < left or character.x + character.imageHeight/2 > right:
            character.drop = True


def main():
    runAppWithScreens("start",width=800,height=500)

main()