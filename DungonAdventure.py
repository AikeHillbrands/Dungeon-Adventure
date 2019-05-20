import pygame as pg
import random as rnd
import math
from threading import Thread

dispSize = (1600,900)

frameRate =40
blockSize = 100
worldSize = (20,20)
enemyAttackrange = 3

pg.init()
pg.display.init()
screen = pg.display.set_mode(dispSize, pg.SWSURFACE | pg.DOUBLEBUF)





loading = pg.transform.scale(pg.image.load('loading.png'),dispSize).convert()
gameover = pg.transform.scale(pg.image.load('gameover.png'),dispSize).convert_alpha()





font = pg.font.Font(None, 35)






class Map:

    BOSS = 'BOSS'
    NORMAL = 'NORMAL'
    MINI = 'MINI'
        
    def __init__(self, dispSize, blockSize):
        
        self.dispSize=dispSize
        self.blockSize = blockSize
        self.chestSize = int(blockSize*1.5)
        self.camPos = (0,0)
        self.blocks = []
        self.lights = []
        self.chunks = []
        self.chests = []
        self.enemys = []
        self.hitboxes = []
        self.varianceImgs=[]
        self.particles = []
        self.relevantHitBoxes = []
        self.relevantEnemys = []
        self.items = []


        self.playerArmor = 0

        self.loadTexturepack("default")
        

    def loadTexturepack(self,arg):
        self.chestImgs = []
        self.chestImgs.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\chest0.png').convert_alpha(),(self.chestSize,self.chestSize)))
        self.chestImgs.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\chest1.png').convert_alpha(),(self.chestSize,self.chestSize)))
        self.chestImgs.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\chest2.png').convert_alpha(),(self.chestSize,self.chestSize)))
        self.chestImgs.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\chest3.png').convert_alpha(),(self.chestSize,self.chestSize)))

        self.playerImgs = []
        self.playerImgs.append(pg.image.load('texturepacks\\'+arg+'\char0.png').convert_alpha())
        self.playerImgs.append(pg.image.load('texturepacks\\'+arg+'\char1.png').convert_alpha())
        self.playerImgs.append(pg.image.load('texturepacks\\'+arg+'\char2.png').convert_alpha())
        self.playerImgs.append(pg.image.load('texturepacks\\'+arg+'\char3.png').convert_alpha())

        self.groundVariance = []
        self.groundVariance.append(pg.image.load('texturepacks\\'+arg+'\crack.png').convert_alpha())
        self.groundVariance.append(pg.image.load('texturepacks\\'+arg+'\puddle.png').convert_alpha())
        self.groundVariance.append(pg.image.load('texturepacks\\'+arg+'\skull.png').convert_alpha())
        
        self.scorpion = []
        self.scorpion.append(pg.image.load('texturepacks\\'+arg+'\scorpion.png').convert_alpha())
        self.scorpion.append(pg.image.load('texturepacks\\'+arg+'\scorpion1.png').convert_alpha())
        self.scorpion.append(pg.image.load('texturepacks\\'+arg+'\scorpion2.png').convert_alpha())
        self.scorpion.append(pg.image.load('texturepacks\\'+arg+'\scorpion3.png').convert_alpha())
        self.scorpion.append(pg.image.load('texturepacks\\'+arg+'\scorpion4.png').convert_alpha())


        self.varianceImgs = []
        self.varianceImgs.append(pg.image.load('texturepacks\\'+arg+'\wallVariance1.png').convert_alpha())
        self.varianceImgs.append(pg.image.load('texturepacks\\'+arg+'\wallVariance2.png').convert_alpha())
        self.varianceImgs.append(pg.image.load('texturepacks\\'+arg+'\wallVariance3.png').convert_alpha())
        self.varianceImgs.append(pg.image.load('texturepacks\\'+arg+'\wallVariance4.png').convert_alpha())
        self.varianceImgs.append(pg.image.load('texturepacks\\'+arg+'\wallVariance5.png').convert_alpha())

        self.bloodList = []
        self.bloodList.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\lood1.png'),(blockSize,blockSize)))
        self.bloodList.append(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\lood2.png'),(blockSize,blockSize)))

        self.lightImg = pg.image.load('texturepacks\\'+arg+'\LightMap.png')
        self.shadow = pg.image.load('texturepacks\\'+arg+'\shadow.png')



        self.charImgs = []
        self.charImgs.append(pg.transform.rotate(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\char0.png').convert_alpha(),
                                                                    (blockSize*charSize,blockSize*charSize)),90+180))
        self.charImgs.append(pg.transform.rotate(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\char1.png').convert_alpha(),
                                                                    (blockSize*charSize,blockSize*charSize)),90+180))
        self.charImgs.append(pg.transform.rotate(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\char2.png').convert_alpha(),
                                                                    (blockSize*charSize,blockSize*charSize)),90+180))
        self.charImgs.append(pg.transform.rotate(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\char3.png').convert_alpha(),
                                                                    (blockSize*charSize,blockSize*charSize)),90+180))
        self.charImgs.append(pg.transform.rotate(pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\char4.png').convert_alpha(),
                                                                    (blockSize*charSize,blockSize*charSize)),90+180))

        self.wallImg = pg.image.load('texturepacks\\'+arg+'\wall.png').convert()

        self.groundImg = pg.image.load('texturepacks\\'+arg+'\ground.png').convert()

        self.healthImg = pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\Health.png').convert_alpha(),(50,50))
        self.shieldImg = pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\Shield.png').convert_alpha(),(50,50))
        self.invBack = pg.transform.scale(pg.image.load('texturepacks\\'+arg+'\InvBackground.png').convert_alpha(),(52,52))

                

        
        
    def genWorld(self,worldSize):
        wb = self.worldBuilder()
        self.worldSize=(worldSize[0]*3+1,worldSize[1]*3+1)
        ra = wb.genRoomArray(worldSize[0],worldSize[1])


        for room in ra:
            self.buildRoom(room)

        for i in range(ra[-1][0][0]*3+3):
            self.addBlock((0,i),self.wallImg)
        for i in range(ra[-1][0][1]*3+3):
            self.addBlock((i,ra[-1][0][0]*3+3),self.wallImg)

        self.genHitboxes()
                
        return ra

    

    def reGenWorld(self,worldSize,ra):
        self.camPos = (0,0)
        self.playerArmor = 0
        self.blocks = []
        self.lights = []
        self.chests = []
        self.enemys = []
        self.hitboxes = []
        self.particles = []
        self.relevantHitBoxes = []
        self.relevantEnemys = []
        self.items = []

        for room in ra:
            self.buildRoom(room)

        for i in range(ra[-1][0][0]*3+3):
            self.addBlock((0,i),self.wallImg)
        for i in range(ra[-1][0][1]*3+3):
            self.addBlock((i,ra[-1][0][0]*3+3),self.wallImg)

        self.genHitboxes()

        
        

    def buildRoom(self,room):

        if rnd.randrange(2) ==1:
            self.lights.append((room[0][0]*3+2,room[0][1]*3+2))
        
        self.addBlock(((room[0][0])*3,(room[0][1])*3),self.wallImg)
        self.addBlock(((room[0][0]+1)*3,(room[0][1])*3),self.wallImg)
        self.addBlock(((room[0][0]+1)*3,(room[0][1]+1)*3),self.wallImg)
        if not room[1]:
            self.addBlock(((room[0][0])*3+1,(room[0][1])*3),self.wallImg)
            self.addBlock(((room[0][0])*3+2,(room[0][1])*3),self.wallImg)
        if not room[2]:
            self.addBlock(((room[0][0])*3+3,(room[0][1])*3+1),self.wallImg)
            self.addBlock(((room[0][0])*3+3,(room[0][1])*3+2),self.wallImg)
        if room[5]:
            self.chests.append([((room[0][0])*3+1.5,(room[0][1])*3+1.5),0,self.chestImgs[0]])
            self.hitboxes.append(self.Hitbox(((room[0][0])*3+1.2,(room[0][1])*3+1.2),(0.6,0.6)))
        if room[4]:
            e = self.Enemy(self.scorpion,((room[0][0])*3+1.5,(room[0][1])*3+1.5),rnd.randrange(360),0.05,250,2,15,40,self.relevantHitBoxes,self.BOSS,self)
            self.enemys.append(e)
            e.walking = True
            print("Boss")

        #self.filterBlocks()
            
    def spawnRandomEnemysOffScreen(self,count):
        for _ in range(count):
            succ = False
            pos = (0,0)
            while not succ:
                pos = (rnd.randrange(self.worldSize[0]),rnd.randrange(self.worldSize[1]))
                succ = self.checkPosOnMap(pos) and self.dist(pos,self.playerPos)>5
                
            e = self.Enemy(self.scorpion,pos,rnd.randrange(360),0.05,100,1,5,30,self.relevantHitBoxes,self.NORMAL,self)
            self.enemys.append(e)
            e.walking = True
            
    
    def genHitboxes(self):
        for block in self.blocks:
            self.hitboxes.append(self.Hitbox((block[0][0]-0.5,block[0][1]-0.5),(1,1)))

    def filterBlocks(self):
        for b in self.blocks:
            if not (self.isBlock(b[0][0]-1,b[0][1]) or
                    self.isBlock(b[0][0]+1,b[0][1]) or
                    self.isBlock(b[0][0]  ,b[0][1]-1) or
                    self.isBlock(b[0][0]  ,b[0][1]+1)):
                self.blocks.remove(b)

    def isBlock(self,x,y):
        for b in self.blocks:
            if (b[0][0] == x and b[0][1] == y):
                return True
        return False
            
    
    def addBlock(self,pos,img):
        double = False
        for block in self.blocks:
            if block[0]==pos:
                double = True
                break
        if not double:
            self.blocks.append((pos,img))

    def setCam(self,pos):
        self.camPos=pos

    def focusPlayer(self):
        self.camPos = self.playerPos

    def movePlayer(self,pos):
        if self.checkPos(pos):
            self.playerPos = pos
        elif self.checkPos((pos[0],self.playerPos[1])):
            self.playerPos = (pos[0],self.playerPos[1])
        elif self.checkPos((self.playerPos[0],pos[1])):
            self.playerPos = (self.playerPos[0],pos[1])

    def checkPosOnMap(self,pos):
            for hb in self.hitboxes:
                if hb.checkColl(pos,0.2):
                    return False
            return True

    def checkPos(self,pos):
            for hb in self.relevantHitBoxes:
                if hb.checkColl(pos,0.3):
                    return False
            return True
    
    def createPlayer(self,pos):
        self.healTicks  = 0
        self.healthSlot = 0
        self.playerPos = pos
        self.playerDir = 0
        self.playerMaxHelath = 100
        self.playerHealth = self.playerMaxHelath
        self.playerDmg = 20
        self.playerRange = 1
        self.playerState = 0
        self.playerUp=False
        self.playerDown=False
        self.playerRight=False
        self.playerLeft=False
        self.playerSpeed = 0.1
        
    
    def renderNearbyWorld(self):
        '''
        enemySurface = pg.Surface((int(self.dispSize[0]/2),int(self.dispSize[1]/2)))
        enemySurface.convert_alpha()
        enemyRenderThread = Thread(target=self.renderEnemySurface, args=([enemySurface]))
        enemyRenderThread.start()

        chestSurface = pg.Surface((int(self.dispSize[0]/2),int(self.dispSize[1]/2)))
        chestSurface.convert_alpha()
        chestRenderThread = Thread(target=self.renderChestSurface, args=([chestSurface]))
        chestRenderThread.start()
        '''
        screen.fill((0,0,0))
        screen.blit(self.worldSurface,(-self.blockSize/2-self.camPos[0]*self.blockSize+self.dispSize[0]/2,
                                       -self.blockSize/2-self.camPos[1]*self.blockSize+self.dispSize[1]/2))

        #RENDER DYNAMIC ON MAP
        
        '''
        chestRenderThread.join()
        enemyRenderThread.join()


        screen.blit(chestSurface,(0,0))
        screen.blit(enemySurface,(0,0))
        '''

        for chest in self.chests:
            if (chest[0][0]>self.camPos[0]-self.dispSize[0]/self.blockSize and
                chest[0][0]<self.camPos[0]+self.dispSize[0]/self.blockSize + self.blockSize and
                chest[0][1]>self.camPos[1]-self.dispSize[1]/self.blockSize and
                chest[0][1]<self.camPos[0]+self.dispSize[1]/self.blockSize + self.blockSize):
                surface = chest[2]
                screen.blit(surface,(chest[0][0]*blockSize-self.camPos[0]*self.blockSize+self.dispSize[0]/2-surface.get_size()[0]/2,
                                     chest[0][1]*blockSize-self.camPos[1]*self.blockSize+self.dispSize[1]/2-surface.get_size()[1]/2))

        for enemy in self.relevantEnemys:
                surface = enemy.get_Surface()
                screen.blit(surface,(enemy.pos[0]*blockSize-self.camPos[0]*self.blockSize+self.dispSize[0]/2-surface.get_size()[0]/2,
                                     enemy.pos[1]*blockSize-self.camPos[1]*self.blockSize+self.dispSize[1]/2-surface.get_size()[1]/2))
        
        self.renderPlayer()

        for p in self.particles:
            screen.blit(p[2],(p[0][0]*self.blockSize+self.dispSize[0]/2-self.camPos[0]*self.blockSize-p[2].get_size()[0]/2,
                              p[0][1]*self.blockSize+self.dispSize[1]/2-self.camPos[1]*self.blockSize-p[2].get_size()[1]/2))
        
        screen.blit(self.lightMap,(-self.blockSize/2-self.camPos[0]*self.blockSize+self.dispSize[0]/2,
                                       -self.blockSize/2-self.camPos[1]*self.blockSize+self.dispSize[1]/2),special_flags=pg.BLEND_MULT)       

        #screen.blit(playerLight,(self.playerPos[0]-self.camPos[0]+self.dispSize[0]/2-playerLight.get_size()[0]/2,
        #                         self.playerPos[1]-self.camPos[1]+self.dispSize[1]/2-playerLight.get_size()[0]/2),special_flags=pg.BLEND_MULT)


        for item in self.items:
            surface = pg.transform.rotozoom(item[1],0,self.itemSizeFunction(item[2])*2)
            screen.blit(surface,(item[0][0]*blockSize-self.camPos[0]*self.blockSize+self.dispSize[0]/2-surface.get_size()[0]/2,
                                 item[0][1]*blockSize-self.camPos[1]*self.blockSize+self.dispSize[1]/2-surface.get_size()[1]/2))
        
        self.renderHUD()
        pg.display.update((0,0,dispSize[0],dispSize[1]))

    def itemSizeFunction(self,x):
        return x/10-(x*x)/400
    

    def renderHUD(self):
        lbs = int(self.dispSize[0] * 0.6 * (self.playerHealth/100))
        if lbs < 0:
            lbs = 0
        lifeBarSurface = pg.Surface((lbs,20))
        lifeBarSurface.fill((255,0,0))

        lifeBarSurfaceBackground = pg.Surface((int(self.dispSize[0]*0.6+2),20+2))
        lifeBarSurfaceBackground.fill((50,50,50))
        
        screen.blit(lifeBarSurfaceBackground,(int(self.dispSize[0]/2-self.dispSize[0]*0.3-1),self.dispSize[1]-30-1))
        screen.blit(lifeBarSurface,(int(self.dispSize[0]/2-self.dispSize[0]*0.3),self.dispSize[1]-30))
        
        if self.playerArmor>0:
            absize = int(self.dispSize[0] * 0.6 * (self.playerArmor/100))
            
            armorBarS = pg.Surface((absize,7))
            armorBarS.fill((0,0,255))

            armorBarSB = pg.Surface((int(self.dispSize[0]*0.6+2),7+2))
            armorBarSB.fill((50,50,50))
            
            screen.blit(armorBarSB,(int(self.dispSize[0]/2-self.dispSize[0]*0.3-1),self.dispSize[1]-30-16-1))
            screen.blit(armorBarS, (int(self.dispSize[0]/2-self.dispSize[0]*0.3  ),self.dispSize[1]-30-16  ))

        screen.blit(self.invBack,( int(self.dispSize[0]/2-self.dispSize[0]*0.3 - 71),self.dispSize[1] - 62))
        screen.blit(self.healthImg,( int(self.dispSize[0]/2-self.dispSize[0]*0.3 - 70),self.dispSize[1] - 61))

        text = font.render(str(self.healthSlot), True, (255,255,255))
        screen.blit(text,(int(self.dispSize[0]/2-self.dispSize[0]*0.3 - 70),self.dispSize[1] - 61+50-text.get_size()[1]))

        
            

    def renderEnemySurface(self,out):
        
        for enemy in self.enemys:
            eSurf = enemy.get_Surface()
            out.blit(eSurf,(0,0))

    def renderChestSurface(self,out):
        for chest in self.chests:
            if (chest[0][0]>self.camPos[0]-self.dispSize[0]/self.blockSize and chest[0][0]<self.camPos[0]+self.dispSize[0]/self.blockSize + self.blockSize and
                chest[0][1]>self.camPos[1]-self.dispSize[1]/self.blockSize and chest[0][1]<self.camPos[0]+self.dispSize[1]/self.blockSize + self.blockSize):
                cSurf = chest[2]
                out.blit(cSurf,((chest[0][0]-self.camPos[0])*self.blockSize-self.dispSize[0]-cSurf.get_size()[0],
                                (chest[0][1]-self.camPos[1])*self.blockSize-self.dispSize[1]-cSurf.get_size()[1]))
        
    
    def getChunkSurface(self,chunkList,x,y):
        result = pg.Surface(self.dispSize)

        for chunk in chunkList:
            if chunk[1][0]*self.chunkSize+x+self.chunkSize>0 and chunk[1][1]*self.chunkSize+y+self.chunkSize>0:
                if chunk[1][0]*self.chunkSize+x+self.dispSize[0]>0 and chunk[1][1]*self.chunkSize+y+self.dispSize[1]>0:
                    result.blit(chunk[0],(chunk[1][0]*self.chunkSize+x,chunk[1][1]*self.chunkSize+y))
        return result

    ticks = 0

    def dropItem(self,pos,iType):
        surface = pg.Surface((int(self.blockSize/2),int(self.blockSize/2)))

        if iType == 'HEALTH':
            surface = pg.transform.scale(pg.transform.rotozoom(self.healthImg, 0,1),(int(self.blockSize/2),int(self.blockSize/2)))
        elif iType == 'SHIELD':
            surface = pg.transform.scale(pg.transform.rotozoom(self.shieldImg, 0,1),(int(self.blockSize/2),int(self.blockSize/2)))

        self.items.append([pos,surface,0])

        
        
    
    def tick(self):
        self.ticks+=1
        blocksOnScreen = (self.dispSize[0]/self.blockSize,self.dispSize[1]/self.blockSize)

        offset = 3
        if self.ticks%3==0:
            for hb in self.hitboxes:
                if (hb.pos[0]              >self.camPos[0] - blocksOnScreen[0]/2 - offset and
                    hb.pos[0] + hb.size[0] <self.camPos[0] + blocksOnScreen[0]/2 + offset and
                    hb.pos[1]              >self.camPos[1] - blocksOnScreen[1]/2 - offset and
                    hb.pos[1] + hb.size[1] <self.camPos[1] + blocksOnScreen[1]/2 + offset):
                    if hb not in self.relevantHitBoxes:
                        self.relevantHitBoxes.append(hb)
                elif hb in self.relevantHitBoxes:
                    self.relevantHitBoxes.remove(hb)

        offset = 1
        for e in self.relevantEnemys:
            if not e in self.enemys:
                self.relevantEnemys.remove(e)
                
        if self.ticks%3==0:
            for e in self.enemys:
                if (e.pos[0]>self.camPos[0]-blocksOnScreen[0]/2 - offset and
                    e.pos[0]<self.camPos[0]+blocksOnScreen[0]/2 + offset and
                    e.pos[1]>self.camPos[1]-blocksOnScreen[1]/2 - offset and
                    e.pos[1]<self.camPos[1]+blocksOnScreen[1]/2 + offset):
                    if e not in self.relevantEnemys:
                        self.relevantEnemys.append(e)
                elif e in self.relevantEnemys:
                    self.relevantEnemys.remove(e)
                
        self.tickPlayer()

        for chest in self.chests:
            if chest[1]>0and chest[1]<3:
                chest[1]+=0.5
            elif chest[1]>=3:
                chest[1]=3

            if chest[1]==0:
                chest[2]=self.chestImgs[0]
            elif chest[1]<1:
                chest[2]=self.chestImgs[1]
            elif chest[1]<2:
                chest[2]=self.chestImgs[2]
            elif chest[1]<3:
                chest[2]=self.chestImgs[3]
        
        for enemy in self.relevantEnemys:
            if self.dist(enemy.pos,self.playerPos)< enemyAttackrange:
                enemy.seePlayer()
            elif enemy.target:
                enemy.forgetPlayer()
                
            #ENEMY ATTACKS PLAYER
            if self.dist(enemy.pos,self.playerPos)< enemy.size*0.8:
                enemy.attackPlayer(self)
                enemy.stopped = True
                
            else:
                enemy.stopped = False
                
            enemy.tick()

        for item in self.items:
            item[2]+=3

            if item[2]>=40:
                self.items.remove(item)
                        

            
        for p in self.particles:
            p[0] = (p[0][0]+p[1][0],p[0][1]+p[1][1])
            p[3]-=1
            if p[3] <=0:
                self.worldSurface.blit(p[2],(p[0][0] * self.blockSize-p[2].get_size()[0]/2+0.5*self.blockSize,
                                             p[0][1] * self.blockSize-p[2].get_size()[1]/2+0.5*self.blockSize))
                self.particles.remove(p)
        
    
    def tickPlayer(self):
        if self.healTicks > 0:
            self.healTicks -=0.2
            if self.playerHealth <100:
                self.playerHealth +=0.2
            else:
                self.playerHealth = 100
        else:
            self.healTicks = 0
        
        if self.playerState >0:
            self.playerState-=1
        else:
            self.playerState = 0

        playerX = 0
        playerY = 0

        if self.playerUp:
            playerY = -self.playerSpeed
        if self.playerDown:
            playerY = self.playerSpeed
        if self.playerRight:
            playerX = self.playerSpeed
        if self.playerLeft:
            playerX = -self.playerSpeed

        if playerX != 0 and playerY != 0:
            playerX = playerX/math.sqrt(2)
            playerY = playerY/math.sqrt(2)

        if playerX != 0 or playerY != 0:
            self.movePlayer((self.playerPos[0]+playerX,self.playerPos[1]+playerY))

    def renderPlayer(self):
        surface = pg.Surface((0,0))
        if self.playerState > 3:
            surface = pg.transform.rotozoom(self.charImgs[1], self.playerDir,1)
        elif self.playerState > 2:
            surface = pg.transform.rotozoom(self.charImgs[2], self.playerDir,1)
        elif self.playerState > 1:
            surface = pg.transform.rotozoom(self.charImgs[3], self.playerDir,1)
        elif self.playerState > 0:
            surface = pg.transform.rotozoom(self.charImgs[4], self.playerDir,1)
        elif self.playerState <= 0:
            surface = pg.transform.rotozoom(self.charImgs[0], self.playerDir,1)
               
        screen.blit(surface,(self.playerPos[0]*self.blockSize-surface.get_size()[0]/2+self.dispSize[0]/2-self.camPos[0]*self.blockSize,
                             self.playerPos[1]*self.blockSize-surface.get_size()[1]/2+self.dispSize[1]/2-self.camPos[1]*self.blockSize))

    def popPotion(self):
        if self.healthSlot > 0:
            self.healthSlot -=1

            self.healTicks += 33
    
    def splashBlood(self,point):
        for _ in range(3):
            choice = rnd.choice(self.bloodList)
            choice = pg.transform.rotozoom(rnd.choice(self.bloodList),rnd.randrange(360),(rnd.random()+0.5)*0.4)

            p = ((point[0]-(rnd.random()+0.5)*0.2)*self.blockSize,
                 (point[1]-(rnd.random()+0.5)*0.2)*self.blockSize)
            
            self.worldSurface.blit(choice,(p[0]+choice.get_size()[0]/2,p[1]+choice.get_size()[1]/2))

        for _ in range(15):
            particleSize = 0.4
            choice = self.bloodList[1]
            choice = pg.transform.rotozoom(choice,rnd.randrange(360),(rnd.random()+0.5)*particleSize)

            particleSpeed = 0.5
            self.particles.append([point,((rnd.random()-0.5)*particleSpeed,
                                          (rnd.random()-0.5)*particleSpeed),
                                   choice,3])
        
    def playerHit(self):
        self.playerState = 4
        e= self.getAllHittedEnemys()
        c= self.getAllHittedChests()

        for enemy in e:
            self.splashBlood(enemy.pos)
            enemy.health -= self.playerDmg
            if enemy.health<=0:
                enemy.atDeath(self)
                enemy.img = enemy.imgList[3]
                surface = enemy.get_Surface()
                self.worldSurface.blit(surface,(enemy.pos[0]*self.blockSize-surface.get_size()[0]/2+0.5*self.blockSize,
                                                enemy.pos[1]*self.blockSize-surface.get_size()[1]/2+0.5*self.blockSize))
                self.enemys.remove(enemy)
                print(len (self.enemys))

        for chest in c:
            if chest[1]==0:
                r = rnd.randrange(5)
                if r == 0:
                    self.playerArmor+=20
                    if self.playerArmor >100:
                        self.playerArmor = 100

                    self.dropItem(chest[0],"SHIELD")
                elif r == 1:
                    self.healthSlot +=1
                    self.dropItem(chest[0],"HEALTH")
                else:
                    self.spawnMinisAtChest(chest[0])
                chest[1]+=0.1
                
        

    def spawnMinisAtChest(self,pos):
        for _ in range(5):
            s = rnd.choice(range(4))
            r = (rnd.random()-0.5)*0.8
            
            if s == 0:
                self.createEnemy(self.scorpion,(pos[0]+r,pos[1]-0.4),rnd.randrange(360),0.07,30,0.4,0,0,self.relevantHitBoxes,Map.MINI)
            elif s == 1:
                self.createEnemy(self.scorpion,(pos[0]+r,pos[1]+0.4),rnd.randrange(360),0.07,30,0.4,0,0,self.relevantHitBoxes,Map.MINI)
            elif s == 2:
                self.createEnemy(self.scorpion,(pos[0]-0.4,pos[1]+r),rnd.randrange(360),0.07,30,0.4,0,0,self.relevantHitBoxes,Map.MINI)
            elif s == 3:
                self.createEnemy(self.scorpion,(pos[0]+0.4,pos[1]+r),rnd.randrange(360),0.07,30,0.4,0,0,self.relevantHitBoxes,Map.MINI)

    def getAllHittedEnemys(self):
        result = []
        dist = 0.5
        a = -math.radians(self.playerDir)
        hitpoint = ((self.playerPos[0]+dist*math.cos(a),self.playerPos[1]+dist*math.sin(a)))
        for enemy in self.relevantEnemys:
            if self.dist(hitpoint,enemy.pos) < dist+enemy.size*0.4:
                result.append(enemy)

        return result

    def getAllHittedChests(self):
        result = []
        dist = 0.8
        a = -math.radians(self.playerDir)
        hitpoint = (self.playerPos[0]+dist*math.cos(a),self.playerPos[1]+dist*math.sin(a))
        for chest in self.chests:
            if self.dist(hitpoint,chest[0]) < dist:
                result.append(chest)

        return result
                

            
    def dist(self,p1,p2):
        if (p1[0]-p2[0] !=0 or p1[1]-p2[1] != 0):
            return math.sqrt(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))
        else:
            return 0

    def renderWorldMap(self):
        self.lightMap = pg.Surface((self.worldSize[0]*self.blockSize,self.worldSize[0]*self.blockSize))

        
        
        self.worldSurface = pg.Surface((self.worldSize[0]*self.blockSize,self.worldSize[0]*self.blockSize))
        self.worldSurface.unlock()
        for i in range(self.worldSize[0]):
            for k in range(self.worldSize[1]):
                surface = pg.transform.scale(self.groundImg,(self.blockSize,self.blockSize))
                self.worldSurface.blit(surface,(i*self.blockSize,k*self.blockSize))

        for _ in range(int(self.worldSize[0]*self.worldSize[1]/50)):
            surface = rnd.choice(self.groundVariance)
            surface = pg.transform.rotozoom(surface,rnd.randrange(360),(rnd.random())+0.5)

            self.worldSurface.blit(surface,(rnd.randrange(self.worldSurface.get_size()[0]-surface.get_size()[0]),
                                            rnd.randrange(self.worldSurface.get_size()[1]-surface.get_size()[1])))

        
            
        for block in self.blocks:
            surface = pg.transform.scale(self.shadow,(int(self.blockSize*1.5),int(self.blockSize*1.5)))
            self.worldSurface.blit(surface,(int((block[0][0])*self.blockSize-0.25*self.blockSize),int((block[0][1])*self.blockSize-0.25*self.blockSize)))

        for i in range(int(len(self.blocks)/3)):
            b = rnd.choice(self.blocks)

            surface = pg.transform.scale(rnd.choice(self.varianceImgs),(int(self.blockSize*2),int(self.blockSize*2)))
            self.worldSurface.blit(surface,(int((b[0][0])*self.blockSize-self.blockSize*0.5),int((b[0][1])*self.blockSize-self.blockSize*0.5)))
        
        for block in self.blocks:
            surface = pg.transform.scale(block[1],(self.blockSize,self.blockSize))
            self.worldSurface.blit(surface,((block[0][0])*self.blockSize,(block[0][1])*self.blockSize))
        self.worldSurface=self.worldSurface.convert()
        #self.chunks = self.splitInToChunks(self.worldSurface)
        
        
    def splitInToChunks(self,surface):
        result = []
        chunksX = int(surface.get_size()[0]/self.chunkSize)
        if chunksX*self.chunkSize < surface.get_size()[0]:
            chunksX+=1
        chunksY = int(surface.get_size()[1]/self.chunkSize)
        if chunksY*self.chunkSize < surface.get_size()[1]:
            chunksY+=1

        for x in range(chunksX):
            for y in range(chunksY):
                chunk = pg.Surface((self.chunkSize,self.chunkSize))
                chunk.blit(surface,(-x*self.chunkSize,-y*self.chunkSize))
                result.append((chunk.convert(),(x,y)))
        return result
                

    def renderLightMap(self):
        self.lightMap = pg.Surface((self.worldSize[0]*self.blockSize,self.worldSize[0]*self.blockSize))
        self.lightMap.fill((60,60,60))

        lightSize = 500
        for light in self.lights:
            self.lightMap.blit(pg.transform.scale(self.lightImg,(lightSize,lightSize)),(light[0]*self.blockSize-lightSize/2,light[1]*self.blockSize-lightSize/2))
        self.lightMap=self.lightMap.convert_alpha()
        #self.lightChunks = self.splitInToChunks(self.lightMap)
        
        

    def renderBlock(self,block):
        surface = pg.transform.scale(block[1],(self.blockSize,self.blockSize))
        renderCenter = self.onScreenPoint(block[0])
        screen.blit(surface,(renderCenter[0]-blockSize/2,renderCenter[1]-blockSize/2))

    def checkBlockOnScreen(self,point):
        centerBlocksOnScreen = (self.dispSize[0]/blockSize/2,self.dispSize[1]/blockSize/2)
        p = self.onScreenPoint(point)
        if p[0]>-self.blockSize/2 and p[1]>-self.blockSize/2 and p[0]<self.dispSize[0]+self.blockSize/2 and p[1]<self.dispSize[1]+self.blockSize/2:
            return True
        return False
        

    def onScreenPoint(self,point):
        centerBlocksOnScreen = (self.dispSize[0]/blockSize/2,self.dispSize[1]/blockSize/2)
        p = (point[0]-self.camPos[0],point[1]-self.camPos[1])
        p = (p[0]+centerBlocksOnScreen[0],p[1]+centerBlocksOnScreen[1])
        p = (p[0]*self.blockSize,p[1]*self.blockSize)
        return p

    def createEnemy(self,imgList,pos,angle,speed,health,size,dmg,attackSpeed,hitBoxes,args):
        self.enemys.append(self.Enemy(imgList,pos,angle,speed,health,size,dmg,attackSpeed,hitBoxes,args,self))

    class Enemy:

        
        def __init__(self,imgList,pos,angle,speed,health,size,dmg,attackSpeed,hitBoxes,args,myMap):
            self.imgList = imgList
            self.pos = pos
            self.angle = angle
            self.health = health
            self.dmg = dmg
            self.attackSpeed  =attackSpeed
            self.walking = False
            self.walkState = 0
            self.img = imgList[0]
            self.size  = size
            self.speed = speed
            self.stdSpeed = speed
            self.hitBoxes = hitBoxes
            self.rndCooldown = 0
            self.args = args
            self.waiting = False
            self.target = False
            self.attackCooldown = attackSpeed
            self.myMap = myMap
            self.stopped = False
            if args == Map.BOSS:
                self.waiting = True

            for img in self.imgList:
                pg.transform.scale(img,(int(self.size*blockSize),int(self.size*blockSize)))

        def placeAt(self,pos):
            self.pos = pos

        def attackPlayer(self,mymap):
            
            if(self.attackCooldown <= 0 and self.args != Map.MINI):
                
                self.dmgPlayer(mymap,self.dmg)
                self.attackCooldown = self.attackSpeed
                

        def dmgPlayer(self,mymap,dmg):
            if mymap.playerArmor >= dmg:
                mymap.playerArmor-=dmg
            elif mymap.playerArmor < dmg:
                mymap.splashBlood(mymap.playerPos)
                mymap.playerHealth -= (dmg-mymap.playerArmor)
                mymap.playerArmor = 0

        def seePlayer(self):
            self.target = True
            self.speed= self.stdSpeed*1.5
            self.waiting = False

        def forgetPlayer(self):
            self.target = False
            self.speed = self.stdSpeed
            
            

        def tick(self):
            if not self.waiting:
                sensorThread = Thread(target=self.useSensor(), args=[])
                sensorThread.start()
                
                if self.attackCooldown > 0:
                    self.attackCooldown -=1

                if self.attackCooldown>self.attackSpeed*0.9:
                    self.img = self.imgList[4]
                else:
                    self.img = self.imgList[0]

                    
                if self.walking and not self.stopped:
                    self.walk()
                    if self.walkState < 1:
                        self.img = self.imgList[0]
                    elif self.walkState < 2:
                        self.img = self.imgList[1]
                    elif self.walkState < 3:
                        self.img = self.imgList[0]
                    elif self.walkState < 4:
                        self.img = self.imgList[2]
                    
                    
                    
                    self.walkState +=0.5
                    
                    if self.walkState >= 4 :
                        self.walkState = 0
                

                
                self.randomDir()
                sensorThread.join()
                self.angle = self.angle%360
                self.pointToPlayer()

        def atDeath(self,mapObj):
            if self.args == Map.BOSS:
                for _ in range(15):
                    mapObj.createEnemy(mapObj.scorpion,self.pos,rnd.randrange(360),0.07,30,0.4,0,0,self.hitBoxes,Map.MINI)

        def pointToPlayer(self):
            if self.target and self.args != Map.MINI:
                t = math.degrees(math.atan2(self.pos[0]-self.myMap.playerPos[0], self.pos[1]-self.myMap.playerPos[1]))-90

                t = t % 360

                at = (t - self.angle)%360
                if abs(at) > 6:
                    if at > 180:
                        self.angle +=6
                    else:
                        self.angle -=6
      
        def randomDir(self):
                self.angle =self.angle + rnd.randrange(5)-2.5
                self.rndCooldown = frameRate

        def useSensor(self):
            dir1 = -math.radians(self.angle - 30)
            dir2 = -math.radians(self.angle + 30)
            
            dist = self.size/3
            sensor1 = self.checkPos((self.pos[0]+dist*math.cos(dir1),self.pos[1]+dist*math.sin(dir1)))
            sensor2 = self.checkPos((self.pos[0]+dist*math.cos(dir2),self.pos[1]+dist*math.sin(dir2)))

            if  not sensor1 and sensor2:
                self.walking  = True
                self.angle +=6
            elif sensor1 and not sensor2:
                self.walking  = True
                self.angle -=6
            elif not sensor1 and not sensor2:
                self.walking  = False
                self.angle +=7
            else:
                self.walking = True

            
                
        
        def walk(self):
            a = -math.radians( self.angle)
            pos = (self.pos[0]+self.speed*math.cos(a),self.pos[1]+self.speed*math.sin(a))
            if self.checkPos(pos):
                self.pos = pos
            elif self.checkPos((pos[0],self.pos[1])) and self.pos[0] != pos[0]:
                self.pos = (pos[0],self.pos[1])
            elif self.checkPos((self.pos[0],pos[1])) and self.pos[1] != pos[1]:
                self.pos = (self.pos[0],pos[1])

        def get_Surface(self):
            #surface = pg.Surface((self.size*blockSize,self.size*blockSize))
            
            surface = pg.transform.rotozoom(self.img, self.angle,self.size)
            return surface
                
            
        def checkPos(self,pos):
            for hb in self.hitBoxes:
                if hb.checkColl(pos,self.size/4):
                    return False
            return True

    class Hitbox:
        def __init__(self,pos,size):
            self.pos = pos
            self.size = size
            

        def checkColl(self,point,radius):

            if abs(self.pos[0]+self.size[0]/2-point[0]) < radius + self.size[0]/2 or abs(self.pos[1]+self.size[1]/2-point[1]) < radius+ self.size[1]/2:
            
                result = ((point[0]>self.pos[0]-radius and
                        point[0]<self.pos[0]+self.size[0]+radius and
                        point[1]>self.pos[1]-radius and
                        point[1]<self.pos[1]+self.size[1]+radius) or
                        (point[1]>self.pos[1]-radius and
                        point[1]<self.pos[1]+self.size[1]+radius and
                        point[0]>self.pos[0] and
                        point[0]<self.pos[0]+self.size[0]))# or
                        #(self.dist(self.pos,point)<radius) or
                        #(self.dist((self.pos[0]+self.size[0],self.pos[1]),point) < radius) or
                        #(self.dist((self.pos[0],self.pos[1]+self.size[1]),point) < radius) or
                        #(self.dist((self.pos[0]+self.size[0],self.pos[1]+self.size[1]),point) < radius))
                return result
            return False
                
            

        def dist(self,p1,p2):
            if (p1[0]-p2[0] !=0 or p1[1]-p2[1] != 0):
                return math.sqrt(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))
            else:
                return 0
    
    class worldBuilder:
        def __init__(self):
            self.roomArray = []

        def genRoomArray(self,x,y):
            self.mapSize = (x,y)
            
            for i in range(x):
                spalte = []
                for k in range(y):
                    self.roomArray.append([(i,k),False,False,False,False,False])#[(X,Y),TopOpen,RightOpen,Used,Boss,EndOfWay]

            self.genBigRoom(rnd.randrange(y-4)+1,rnd.randrange(x-4)+1)
            self.genBigRoom(rnd.randrange(y-4)+1,rnd.randrange(x-4)+1)

               
            finished = False
            stack = [self.roomArray[0]]
            self.roomArray[0][3]=True
            self.roomArray[0][4]=False
            self.roomArray[0][5]=False
            while not finished:
                if len(stack)!=0:
                    neighbors = self.getFreeNeighbors(stack[-1])
                    popStack = len(neighbors) == 0
                    if popStack:
                        stack[-1][5]=True
                    while popStack and len(stack) > 1:
                        del(stack[-1])
                        neighbors = self.getFreeNeighbors(stack[-1])
                        popStack = len(neighbors) == 0
                        if len(stack) == 1:
                            finished = True   
                    if not finished:
                        
                        sel = rnd.choice(neighbors)
                        
                        if self.getX(sel)-1==self.getX(stack[-1]):
                            stack[-1][2]=True
                        if self.getX(sel)+1==self.getX(stack[-1]):
                            sel[2]=True
                        if self.getY(sel)-1==self.getY(stack[-1]):
                            sel[1]=True
                        if self.getY(sel)+1==self.getY(stack[-1]):
                            stack[-1][1]=True
                        stack.append(sel)
                    
                        stack[-1][3]=True
            for i in range(int(len(self.roomArray)/5)):
                self.delRandomWall()
            
            return self.roomArray

        
        def getRoom(self,x,y):
            for r in self.roomArray:
                if self.getX(r) == x and self.getY(r)==y:
                    return r
            return False

        def delRandomWall(self):
            r=self.getRoom(rnd.randrange(self.mapSize[0]-1),rnd.randrange(self.mapSize[1]-1)+1)
            if(rnd.randrange(2)==1):
                r[1]=True
            else:
                r[2]=True
        
        def genBigRoom(self,x,y):
            if x > 0 and x+3<self.mapSize[0] and y > 0 and y+3<self.mapSize[1]:
                self.openRoom(self.getRoom(x,y),False,True,True)
                self.openRoom(self.getRoom(x+1,y),True,True,True)
                self.openRoom(self.getRoom(x+2,y),False,False,True)

                self.openRoom(self.getRoom(x,y+1),True,True,True)
                self.openRoom(self.getRoom(x+1,y+1),True,True,True)
                self.getRoom(x+1,y+1)[4]=True
                self.openRoom(self.getRoom(x+2,y+1),True,True,True)

                self.openRoom(self.getRoom(x,y+2),True,True,True)
                self.openRoom(self.getRoom(x+1,y+2),True,True,True)
                self.openRoom(self.getRoom(x+2,y+2),True,False,True)

                self.openRoom(self.getRoom(x-1,y+1),False,True,False)
                self.openRoom(self.getRoom(x+1,y+3),True,False,False)
                

        def openRoom(self,room,top,right,used):
            room[1]=top
            room[2]=right
            room[3]=used
            
        
        def getX(self,room):
            return room[0][0]

        def getY(self,room):
            return room[0][1]

        def getFreeNeighbors(self,room):
            result = []
            for r in self.roomArray:
                addR = False
                if r[0][0]-1 == room [0][0] and r[0][1] == room [0][1] and r[3] == False:
                    addR = True
                if r[0][0]+1 == room [0][0] and r[0][1] == room [0][1] and r[3] == False:
                    addR = True
                if r[0][1]-1 == room [0][1] and r[0][0] == room [0][0] and r[3] == False:
                    addR = True
                if r[0][1]+1 == room [0][1] and r[0][0] == room [0][0] and r[3] == False:
                    addR = True

                if addR:
                    result.append(r)

            return result
                    

              




def drawObject(img,pos,size,angle):
    surface = pg.transform.rotate(pg.transform.scale(img,size), angle)
    screen.blit(surface,(pos[0]*blockSize-(surface.get_size()[0]/2),pos[1]*blockSize-(surface.get_size()[1]/2)))

def mouseDown(pos):
    myMap.playerHit()

def mouseMove(pos):
    from math import atan2, degrees, pi
    dx = pos[0] - dispSize[0]/2
    dy = pos[1] - dispSize[1]/2
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    myMap.playerDir=degs

def showGameOverScreen():
    print("gameOver")

def restartGame():
    myMap.renderNearbyWorld()
    print("restarting...")
    screen.blit(gameover,(0,0))
    pg.display.update((0,0,dispSize[0],dispSize[1]))
    
    global  paused
    paused = False

    myMap.reGenWorld(worldSize,roomArray)

    myMap.renderWorldMap()
    myMap.renderLightMap()

    global  gameRunning
    gameRunning = True

    global  quitted
    quitted = False

    myMap.createPlayer((2,2))
    myMap.spawnRandomEnemysOffScreen(int(myMap.worldSize[0]*myMap.worldSize[1]/25))
    
def startGame():
    screen.blit(loading,(0,0))
    pg.display.update((0,0,dispSize[0],dispSize[1]))
    
    global  paused
    paused = False

    global roomArray
    
    roomArray = myMap.genWorld(worldSize)

    myMap.renderWorldMap()
    myMap.renderLightMap()

    global  gameRunning
    gameRunning = True

    global  quitted
    quitted = False

    myMap.createPlayer((2,2))
    myMap.spawnRandomEnemysOffScreen(int(myMap.worldSize[0]*myMap.worldSize[1]/25))
    

charSize = 4


paused = False
gameRunning = False
quitted = False

clock = pg.time.Clock()
myMap=Map(dispSize,blockSize)

startGame()


while not quitted:
    #Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitted = True
        
        if event.type == pg.KEYDOWN:
            if not paused:
                if event.key == pg.K_w:
                    myMap.playerUp = True
                    myMap.playerDown = False
                if event.key == pg.K_s:
                    myMap.playerUp = False
                    myMap.playerDown = True
                if event.key == pg.K_a:
                    myMap.playerLeft = True
                    myMap.playerRight = False
                if event.key == pg.K_d:
                    myMap.playerLeft = False
                    myMap.playerRight = True
                if event.key == pg.K_1:
                    myMap.popPotion()
            if event.key == pg.K_ESCAPE:
                paused = not paused

        if event.type == pg.KEYUP:
            if not paused:
                if event.key == pg.K_w:
                    myMap.playerUp = False
                if event.key == pg.K_s:
                    myMap.playerDown = False
                if event.key == pg.K_a:
                    myMap.playerLeft = False
                if event.key == pg.K_d:
                    myMap.playerRight = False

        if not paused:
            if event.type == pg.MOUSEMOTION:
                mouseMove(event.pos)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                myMap.playerHit()
        
        '''
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            event.pos
        '''
    
    if not paused:
        if myMap.playerHealth <=0:
            paused = True
            restartGame()
        myMap.focusPlayer()
        myMap.renderNearbyWorld()
        myMap.tick()
        
        clock.tick(frameRate)
        
        

pg.quit()
                
