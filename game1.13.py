from pygame_functions13 import *

def enemyKilled(enemy):
    currentScene.Enemies.remove(enemy)
    link.kills += 1
    itemDrop = dropChart(link.kills)
    print(itemDrop)
    if itemDrop == 0:
        aRupee = Rupee()
        aRupee.move(enemy.rect.x, enemy.rect.y)
        currentScene.Items.append(aRupee)
        showSprite(aRupee)
    elif itemDrop == 1:
        aHeart = Heart()
        aHeart.move(enemy.rect.x, enemy.rect.y)
        currentScene.Items.append(aHeart)
        showSprite(aHeart)
    elif itemDrop == 2:
        pass
        #To Do Program Fairy
    elif itemDrop == 3:
        pass
        #To Do Program Bomb
    elif itemDrop == 4:
        pass
        #To Do Program Timer
    elif itemDrop ==5:
        aBRupee = BlueRupee()
        aBRupee.move(x,y)
        currentScene.Items.append(aBRupee)
        showSprite(aBRupee)
    killSprite(enemy)

#Initial Screen Settings
HUD_Height = 32
tile_size = 32
screen_width=tile_size*32
screen_height=tile_size*24 + HUD_Height
screen = screenSize(screen_width,screen_height)

#Save Select Screen
background = Background()
introMusic = makeMusic("01-intro.mp3")
background.setTiles("saveSelectScreen.png")
select = False
playMusic(99)
#Load in any names found in the DataBase
conn = MakeConn()
names = SelectNames(conn)
maxSelect = 0
saveLabels = []
yPos = 290
EliminationMode = False
for name in names:
    saveText = makeLabel(name, 68, 510, yPos, 'white', 'system', 'black')
    saveLabels.append(saveText)
    showLabel(saveText)
    yPos +=80
    maxSelect+=1
selected = 1
yPos = 280
selectRect = drawRect(180, 280, 650, 75, "yellow", 5)
while select == False:
    pause(10)
    if keyPressed("down"):
        screen.blit(background.surface, [0, 0])
        pause(100)
        yPos += 75
        selected +=1
        if yPos > 580:
            yPos = 280
            selected = 1
        pygame.display.update()
        drawRect(180, yPos, 650, 75, "yellow", 5)
    if keyPressed("up"):
        screen.blit(background.surface, [0, 0])
        pause(100)
        yPos -= 75
        selected -=1
        if yPos < 280:
            yPos = 580
            selected = 5
        pygame.display.update()
        drawRect(180, yPos, 650, 75, "yellow", 5)
    if keyPressed("return"):
        pause(100)
        if EliminationMode == True and selected < 4:
            for label in saveLabels:
                hideLabel(label)
            screen.blit(background.surface, [0, 0])
            Delete_Game(conn, selected)
            names = SelectNames(conn)
            maxSelect = 0
            yPos = 290
            saveLabels = []
            for name in names:
                saveText = makeLabel(name, 68, 510, yPos, 'white', 'system', 'black')
                saveLabels.append(saveText)
                showLabel(saveText)
                yPos +=80
                maxSelect+=1
            EliminationMode = False
            yPos = 280
            drawRect(180, yPos, 650, 75, "yellow", 5)
            selected = 1
        else:
            if selected == 5:
                #Elimination Mode
                EliminationMode = True
            elif selected == 4 or selected>maxSelect:
                #Make User Type Name
                nameInputBox = makeTextBox(180, yPos, 650, 2, "Type Name", 10, 68)
                newName = textBoxInput(nameInputBox)
                if maxSelect < 3:
                    selected = maxSelect + 1
                else:
                    selected = 3
                    Delete_Game(conn, selected)
                game = [selected, newName, 3, 0]
                Make_Save(conn, game)
                hideLabel(nameInputBox)
                select = True
                for label in saveLabels:
                    hideLabel(label)
            else:
                select = True
                for label in saveLabels:
                    hideLabel(label)
            
    updateDisplay()
stopMusic()

#Change Music, Unload Only works if pygame2.0
if pygame.version.vernum[0] >=2:
    pygame.mixer.music.unload()
music = makeMusic("linkMusic.mp3")
playMusic(99)

#Set Up HUD
HealthLabel = makeLabel("Health = 6", 32, 50, 8, "white", "system")
RupeeLabel = makeLabel("Rupee = 0", 32, 200, 8, "white", "system")



#Set Up Sprites
setAutoUpdate(False)
link = Player()
sword = Sword(link)

#Change Link's Stuff based upon save file
loadGame(conn, selected, link)
changeLabel(HealthLabel, "Health = " + str(link.health))
changeLabel(RupeeLabel, "Rupee = " + str(link.rupee))

#Set up Scenes
scene1 = Scene(link, "ZeldaMapTilesBrown.png", "map1.txt", 6,8)
scene2 = Scene(link, "ZeldaMapTilesBrown.png", "map2.txt", 6,8)
scene3 = Scene(link, "ZeldaMapTilesWhite.png", "map3.txt", 6,8)
scene4 = Scene(link, "ZeldaMapTilesGreen.png", "map4.txt", 6,8)

scenes = [[scene1, scene3], [scene2, scene4]]
currentScene = scene1


showBackground(currentScene)

showSprite(link)
for enemy in scene1.Enemies:
    showSprite(enemy)

showLabel(HealthLabel)
showLabel(RupeeLabel)

nextFrame = clock()
frame = 0
# i is the list number
# j is the element number
i = 0
j= 0

while True:
    if clock() >nextFrame:
        frame= (frame + 1)%2
        nextFrame += 80
        pause(10)
        
        for wall in currentScene.Wall_Tiles:
            if touching(wall, link):
                link.speed = -link.speed
                link.move(frame)
                link.speed = - link.speed
        if keyPressed("s"):
            Save(conn, (link.health, link.rupee, selected))
        elif keyPressed("down"):
            
            link.orientation =0
            link.move(frame)
        elif keyPressed("up"):
            link.orientation =1
            link.move(frame)
        elif keyPressed("right"):
            link.orientation =2
            link.move(frame)
        elif keyPressed("left"):
            link.orientation =3
            link.move(frame)
        elif keyPressed("space"):
            changeSpriteImage(link, link.orientation + 8)
        #Sword Swing Code
            sword.swing()
            if len(currentScene.PProjectiles) == 0:
                aSwordProjectile = SwordProjectile()
                aSwordProjectile.orientation = link.orientation
                aSwordProjectile.rect.x = link.rect.x
                aSwordProjectile.rect.y = link.rect.y
                currentScene.PProjectiles.append(aSwordProjectile)
                showSprite(aSwordProjectile)
            for enemy in currentScene.Enemies:
                if touching(sword, enemy):
                    killed = enemy.hit(1)
                    if killed:
                        enemyKilled(enemy)
        if not keyPressed("space") or keyPressed("left") or keyPressed("right") or keyPressed("up") or keyPressed("down"):
            hideSprite(sword)
        if keyPressed("h"):
            changeSpriteImage(link, frame+12)
        
        for enemy in currentScene.Enemies:
            projectile = enemy.move(frame)
            if projectile:
                currentScene.EProjectiles.append(projectile)
            if touching(enemy, link):
                link.hit(currentScene.Wall_Tiles)
            for wall in currentScene.Wall_Tiles:
                while touching(enemy, wall) or enemy.rect.x > screen_width or enemy.rect.y>screen_height or enemy.rect.x<0 or enemy.rect.y<0:
                    enemy.turn()
                    projectile = enemy.move(frame)
                    if projectile:
                        killSprite(projectile)
        for projectile in currentScene.PProjectiles:
            projectile.move(frame)
            if projectile.rect.x > screen_width or projectile.rect.x < 0 or projectile.rect.y > screen_height or projectile.rect.y < 0:
                currentScene.PProjectiles.remove(projectile)
                killSprite(projectile)
            for enemy in currentScene.Enemies:
                if touching(enemy, projectile):
                    killed = enemy.hit(projectile.damage)
                    currentScene.PProjectiles.remove(projectile)
                    killSprite(projectile)
                    if killed:
                        enemyKilled(enemy)
        for projectile in currentScene.EProjectiles:
            projectile.move(frame)
            for wall in currentScene.Wall_Tiles:
                if projectile.wall_collide == True:
                    if touching(wall, projectile):
                        try:
                            currentScene.EProjectiles.remove(projectile)
                            killSprite(projectile)
                        except:
                            print(currentScene.EProjectiles)
                            print(projectile.rect.x, projectile.rect.y)
                        finally:
                            killSprite(projectile)
            if touching(link, projectile):
                link.hit(currentScene.Wall_Tiles)
        for item in currentScene.Items:
            item.animate(frame)
            if touching(item, link):
                link.collect(item)
                currentScene.Items.remove(item)
                killSprite(item)
                changeLabel(HealthLabel, "Health = " + str(link.health))
                changeLabel(RupeeLabel, "Rupee = " + str(link.rupee))
        if link.rect.x + tile_size//2 > screen_width:
            hideBackground(currentScene)
            i += 1
            currentScene = scenes[i][j]
            showBackground(currentScene)
            hideSprite(link)
            link.rect.x = 32
            showSprite(link)
        elif link.rect.x - tile_size//2 < 0:
            hideBackground(currentScene)
            i -= 1
            currentScene = scenes[i][j]
            showBackground(currentScene)
            hideSprite(link)
            link.rect.x = screen_width -32
            showSprite(link)
        elif link.rect.y + tile_size//2 > screen_height:
            hideBackground(currentScene)
            j += 1
            currentScene = scenes[i][j]
            showBackground(currentScene)
            hideSprite(link)
            link.rect.y = 64
            showSprite(link)
        elif link.rect.y - tile_size//2 < 32:
            hideBackground(currentScene)
            j -= 1
            currentScene = scenes[i][j]
            showBackground(currentScene)
            hideSprite(link)
            link.rect.y = screen_height - 32
            showSprite(link)
        updateDisplay()

endWait()