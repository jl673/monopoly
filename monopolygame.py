import time
import pygame
import random
import math
from pygame.locals import *
pygame.init()
Pi=70
def show_text(msg,x,y,color):
        fontobj= pygame.font.SysFont('freesans',32,bold=True)
        msgobj = fontobj.render(msg,False,color)
        screen.blit(msgobj,(x,y))
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Monopoly game")
houses={2: [75, 25],
             4: [125, 45],
             6:[150,55],
             9:[200,65],
##             8:[200,40],
             12: [300,75],
             14:[375,85],
            15:[430,100],
            18:[450,115],
            20:[525,130],
            23:[575,145],
            25:[970,200],
            28:[1500,300],
##            25:[970,185],
            31:[2000,450],
##            31:[2000,400],
            }
giveticket=False
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
pink = (175, 0, 175)
orange = (240, 100, 0)
grey=(64,64,64)
blocks=[]
players=[]
currentplayer=-1
img = pygame.image.load('sqblue.png')
scbd=pygame.image.load('board.png')
pygame.Surface((100,200),pygame.SRCALPHA)
img=pygame.transform.scale(img,(100,100))
bluebutton= pygame.image.load('dice.png')
pygame.Surface((100,200),pygame.SRCALPHA)
bluebutton=pygame.transform.scale(bluebutton,(220,150))
greenhouse= pygame.image.load('greenhouse.png')
greenhouse=pygame.transform.scale(greenhouse,(100,100))
redhouse= pygame.image.load('redhouse.png')
redhouse=pygame.transform.scale(redhouse,(100,100))
buybutton= pygame.image.load('buybutton.png')
buybutton=pygame.transform.scale(buybutton,(200,50))
spinner=pygame.image.load('wheel.png')
##spinner=pygame.transform.scale(spinner,(400,400))
jackpot=1000
bluehouse= pygame.image.load('bluehouse.png')
bluehouse=pygame.transform.scale(bluehouse,(100,100))
spinnerred=pygame.image.load('wheelred.png')
ticket=pygame.image.load('ticket.png')
ticket=pygame.transform.scale(ticket,(200,50))
def jackpotAction(x):
    print('Currentplayer ' + str(currentplayer))
    if x<30:
        print('-250')
        players[currentplayer%10].cash=math.trunc(players[currentplayer%10].cash - 250)
    elif x<60:
        print('error')
        switchplayer(True)
    elif x<90:
        print('+100')
        players[currentplayer%10].cash += 100
    elif x<120:
        print('+125')
        players[currentplayer%10].cash += 125
    elif x<150:
        print('skip')
        players[currentplayer%10].skipTurn()
    elif x<180:
        print('1/4 jackpot')
        global jackpot
        players[currentplayer%10].cash += math.trunc(jackpot/4)
        jackpot -= math.trunc(jackpot/4)
    elif x<210:
        print('20% tax')
        players[currentplayer%10].cash =math.trunc(players[currentplayer%10].cash *.8)
    elif x<240:
        print(' + $150')
        players[currentplayer%10].cash=players[currentplayer%10].cash+ 150
    elif x<270:
        print('-150')
        players[currentplayer%10].cash-=150
    elif x<300:
        print(' go to jail')
        players[currentplayer%10].position=16
        players[currentplayer%10].skipTurn()
    elif x<330:
        print('+125')
        players[currentplayer%10].cash +=125
    elif x<360:
        pass
def switchplayer(x):
    global currentplayer
    #print('Currentplayer ' + str(currentplayer) +  '   ' + str(x))
    if x==True:
        if currentplayer==0 or currentplayer==10:
            currentplayer=10
            return
        elif currentplayer==1 or currentplayer==11:
            currentplayer=11
            return
        else:
            return    #note error contditnonf
    if currentplayer==0 or currentplayer==10:
        currentplayer=1
    else:
        currentplayer=0
    if players[currentplayer%10].skip>0:
        players[currentplayer%10].skip=players[currentplayer%10].skip-1
        if currentplayer==0 or currentplayer==10:
            currentplayer=1
        else:
            currentplayer=0
    

class Player:
    def __init__(self,position,color,x,y,money):
        self.position=position
        self.color=color
        self.x=x
        self.y=y
        self.r=15
        self.skip=0
        self.cash=money
        self.applycounter=0
    def move(self,steps):
        self.applycounter=1
        self.position=self.position+steps
        if self.position>=32:
            self.position=self.position-32
            self.cash=self.cash+200
        if isinstance(blocks[self.position],House)  \
        and blocks[self.position].ownership != players.index(self)  \
        and blocks[self.position].ownership>=0: 
            self.cash=self.cash-blocks[self.position].rent
            players[blocks[self.position].ownership].cash=players[blocks[self.position].ownership].cash+blocks[self.position].rent
    def skipTurn(self):
        self.skip=self.skip+1
    def gameover(self):
        if players[currentplayer%10].cash<0:
            fontobj= pygame.font.SysFont('freesans',50,bold=True)
            msgobj = fontobj.render('Player' + str(currentplayer)+'has been defeated and is weeping',False,pink)
            screen.blit(msgobj,(100,250))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            exit()
        

def tiledescription(i):
    if i in houses.keys():
        return ' '  + str(blocks[i].price) + " / " + str(blocks[i].rent)
    switcher={
            0:'GO',
            1:'Find Wallet',
            2:'',
            3:'Spinner',
            4:'',
            5:'Railroad',
            7:'tax:15%',
            8:'Spinner',
            10:'advance  4',
            11:'donate 100',
            13:'Subway',
            16:'Jail',
            17:'Spinner',
            19:'Give 125',
            21:'Railroad',
            22:'go back 2',
            24:'Subway',
            26:'Go to Jail',
            27:'Spinner',
            29:'drop to 23',
            30:'Lost Wallet'
        
         }
    return switcher.get(i,"")

def tileaction(p):
    if p.position==26:
        p.position=16
        p.skipTurn()
    elif p.position==10:
        p.position=p.position+4
    elif p.position==22:
        p.position=p.position-2
    elif p.position==7:
        if p.applycounter>0:
            p.cash=math.trunc(p.cash*0.85)
            p.applycounter=0
    elif p.position==11:
         if p.applycounter>0:
            p.cash=math.trunc(p.cash-100)
            global jackpot
            jackpot +=100
            p.applycounter=0
    elif p.position==29:
        p.position=23

    elif p.position in [5,21]:
        global giveticket
        if giveticket==True:
            if p.applycounter>0:
                if p.position==5:
                    p.position=21
                    p.cash -= 75
                elif p.position==21:
                    p.position=5
                    p.cash -= 75
                p.applycounter=0
                giveticket=False
    elif p.position in [13,24]:
##        global giveticket
        if giveticket==True:
            if p.applycounter>0:
                if p.position==13:
                    p.position=24
                    p.cash -= 50
                elif p.position==24:
                    p.position=13
                    p.cash -= 50
                p.applycounter=0
                giveticket=False
    elif p.position==1:
        if p.applycounter>0:
            p.cash=math.trunc(p.cash+50)
            p.applycounter=0
    elif p.position==19:
        if p.applycounter>0:
            p.cash=math.trunc(p.cash-125)
            p.applycounter=0
            if players.index(p)==0:
                players[1].cash=players[1].cash+125
            else:
                players[0].cash=players[0].cash+125
    elif p.position==30:
        if p.applycounter>0:
            p.cash=p.cash-100
            p.applycounter=0
##    elif p.position==27 or p.position==3 or p.position==17:
##        if p.applycounter>0:
##            switchplayer(True)
##            p.applycounter=0
##            return
        
class Tiles:
    def __init__(self,index,x,y,img):
        self.index=index
        self.x=x
        self.y=y
        self.image=img
        self.surface=pygame.Surface((100,100),pygame.SRCALPHA)
    def draw(self):
        "drawiing onto itself"
        self.surface.fill((0,0,0))
        self.surface.blit(self.image,(0,0))
        fontobj= pygame.font.SysFont('freesans',32)
        msgobj = fontobj.render(str(self.index),False,orange)
        self.surface.blit(msgobj,(15,5))
        desc = tiledescription(self.index)
        if len(desc)>0:
            fontobj= pygame.font.SysFont('freesans',20)
            msgobj = fontobj.render(desc,False,orange)
            self.surface.blit(msgobj,(15,40))
        for p in players:
            if p.position==self.index:
                pygame.draw.circle(self.surface,p.color,(p.x,p.y),p.r,p.r)
                if players.index(p) == (currentplayer%10):
                    p.r=20
                else:
                    p.r=15
                tileaction(p)
    def update(self):
        "drawing to global"
        screen.blit(self.surface,(self.x,self.y))
        
class House(Tiles):
    def __init__(self,index,x,y,img, price, rent):
        Tiles.__init__(self,index,x,y,img)
        self.price=price
        self.rent=rent
        self.ownership=-1
    def setOwner(self,ownership):
        if self.ownership !=0 and self.ownership!=1:
            self.ownership=ownership
        else:
            return
        if ownership==0:
            self.image=redhouse
            players[0].cash=players[0].cash-self.price
        elif ownership==1:
            self.image=greenhouse
            players[1].cash=players[1].cash-self.price
        else:
            self.image==bluehouse

class Dice:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.image=img
        self.surface=pygame.Surface((220,150),pygame.SRCALPHA)
        self.ctframe = 0
        self.number=0
    def startRoll(self):
        self.ctframe = 10
    def draw(self):
        self.surface.blit(self.image,(0,0))
        if  self.ctframe > 0:
            self.number=random.randint(1,6)
            self.ctframe=self.ctframe-1
            if (self.ctframe==0):
                players[currentplayer%10].move(self.number)
                if players[currentplayer%10].position in [27,3,17,8]:
                    switchplayer(True)
                else:
                    switchplayer(False)
        if self.number != 0:
            fontobj= pygame.font.SysFont('freesans',64)
            msgobj = fontobj.render(str(self.number),False,orange)
            self.surface.blit(msgobj,(95,5))
    def update(self):
        "drawing to global"
        screen.blit(self.surface,(self.x,self.y))
    def isButtonClicked(self,mx,my):
        if currentplayer>=10:
            return False
        ofx = mx - self.x
        ofy=my-self.y
        if ofx>=0 and ofx<= 220 and ofy>=100 and ofy<=150:
            return True
        else:
            return False            
class Buybutton:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.image=img
        self.surface=pygame.Surface((200,50),pygame.SRCALPHA)
    def draw(self):
        self.surface.blit(self.image,(0,0))
    def update(self):
        "drawing to global"
        screen.blit(self.surface,(self.x,self.y))
    def isButtonClicked(self,mx,my):
        ofx = mx - self.x
        ofy=my-self.y
        if ofx>=0 and ofx<= 200 and ofy>=0 and ofy<=50:
            return True
        else:
            return False
    def buy(self):
        
        if  isinstance(blocks[players[currentplayer%10].position], House):
            if players[currentplayer%10].cash> blocks[players[currentplayer%10].position].price:
                    blocks[players[currentplayer%10].position].setOwner(currentplayer%10)
            
class Board:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.image=img
        self.surface=pygame.Surface((300,164),pygame.SRCALPHA)

    def draw(self):
        self.surface.blit(self.image,(0,0))
        top = 5
        for p in players:
            fontobj= pygame.font.SysFont('freesans',64,bold=True)
            msgobj = fontobj.render(str(p.cash),False,p.color)
            self.surface.blit(msgobj,(95,top))
            top=top+75
    def update(self):
        "drawing to global"
        screen.blit(self.surface,(self.x,self.y))

class Jackpot:
    def __init__(self,x,y,img,img2):
        self.x=x
        self.y=y
        self.surface=pygame.Surface((400,400),pygame.SRCALPHA)
        self.surface1=pygame.Surface((400,400),pygame.SRCALPHA)
        self.surface2=pygame.Surface((400,400),pygame.SRCALPHA)
        self.image=img
        self.image2=img2
        self.spinangle = []
        self.angle = 0
        self.surface1.blit(self.image,(0,0))
        self.surface2.blit(self.image2,(0,0))
        self.red=False
    def spin(self):
        if currentplayer < 10:
            return
        for i in range(0,30,1): 
            e=random.randint(0,360)
            self.spinangle.append(e)
        self.spinangle.sort()
    def draw(self):
        if len(self.spinangle)>0:
            self.angle = (self.angle + self.spinangle[-1]) % 360
            self.spinangle.pop()
            if len(self.spinangle)==0:
                JackpotEvent = pygame.event.Event(pygame.USEREVENT+1, attr1=self.angle)
                pygame.event.post(JackpotEvent)
        if currentplayer>= 10:
                if self.red==False: 
                        self.surface = rot_center(self.surface2, self.angle)
                        self.red=True
                else:
                        self.surface = rot_center(self.surface1, self.angle)
                        self.red=False
        else:
                self.surface = rot_center(self.surface1, self.angle)
                self.red=False   
        pygame.draw.polygon(self.surface, grey, ((190,0),(210,0),(200,25)))
        fontobj= pygame.font.SysFont('freesans',32,bold=True)
        msgobj = fontobj.render('JACKPOT:'+str(jackpot),False,pink)
        screen.blit(msgobj,(175,335))
    def update(self):
        screen.blit(self.surface,(self.x,self.y)) 
    def isButtonClicked(self,mx,my):
        if len(self.spinangle) > 0:
            return False
        ofx = mx - self.x
        ofy=my-self.y
        if (ofx-200) * (ofx-200) + (ofy-200)*(ofy-200) <= 30*30:
            return True
        else:
            return False
class Tickets:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.image=img
        self.surface=pygame.Surface((200,50),pygame.SRCALPHA)
    def draw(self):
        self.surface.blit(self.image,(0,0))
    def update(self):
        screen.blit(self.surface,(self.x,self.y))
    def isButtonClicked(self,mx, my):
        ofx=mx-self.x
        ofy=my-self.y
        if ofx>=0 and ofx<= 200 and ofy>=0 and ofy<=50:
            return True
        else:
            return False  
index=0
for pq in range(0,1100,100):
    if (index in houses.keys()):
        blocks.append(House(index,pq,0,bluehouse,houses[index][0],houses[index][1]))
    else:
        blocks.append(Tiles(index,pq,0,img))
    index=index+1
for qp in range(100,600,100):
    if (index in houses.keys()):
        blocks.append(House(index,1000,qp,bluehouse,houses[index][0],houses[index][1]))
    else:
        blocks.append(Tiles(index,1000,qp,img))
    index=index+1
for pq in range(1000,-100,-100):
    if (index in houses.keys()):
        blocks.append(House(index,pq,600,bluehouse,houses[index][0],houses[index][1]))
    else:
        blocks.append(Tiles(index,pq,600,img))
    index=index+1
for qp in range(500,0,-100):
    if (index in houses.keys()):
        blocks.append(House(index,0,qp,bluehouse,houses[index][0],houses[index][1]))
    else:
        blocks.append(Tiles(index,0,qp,img))
    index=index+1
players.append(Player(0,red,30,65,500))
players.append(Player(0,green,75,65,500))
currentplayer=0
dice=Dice(150,400,bluebutton)
scoreboard=Board(150,150,scbd)
button=Buybutton(400,500,buybutton)
wheel=Jackpot(550,120,spinner, spinnerred)
ticket=Tickets(380,425,ticket)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
##        if event.type==KEYDOWN:
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if dice.isButtonClicked(event.pos[0], event.pos[1]):
                dice.startRoll()
                jackpot=jackpot+25
            elif button.isButtonClicked(event.pos[0],event.pos[1]):
                button.buy()
                jackpot=jackpot+25
            elif wheel.isButtonClicked(event.pos[0],event.pos[1]):
                wheel.spin()
                jackpot=jackpot+25
            elif ticket.isButtonClicked(event.pos[0],event.pos[1]):
                if players[currentplayer].position in [13,24,5,21]:
                    giveticket=True
                jackpot=jackpot+25
        elif event.type == pygame.USEREVENT+1:
            #print(str(event.attr1))
            jackpotAction(event.attr1)
            switchplayer(False)
    players[currentplayer%10].gameover()
    screen.fill((0,0,0))
    button.draw()
    button.update()
##    screen.blit(ticket,(380,425))
    dice.draw()
    dice.update()
    ticket.draw()
    ticket.update()
    scoreboard.draw()
    scoreboard.update()
    wheel.draw()
    wheel.update()
    for tile in blocks:
        tile.draw()
        tile.update()
   
    pygame.display.update()
    time.sleep(.075)
