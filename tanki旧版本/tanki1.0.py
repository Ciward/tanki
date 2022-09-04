import pygame
import sys,os
from pygame.locals import *
import random
import math

vect = pygame.Vector2

class Railgun(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Railgun,self).__init__()
        self.owner=owner
        self.rect=self.image.get_rect(center=(owner.rect.centerx,owner.rect.centery))
        #self.x=owner.rect.centerx
        #self.y=owner.rect.centery
        self.drict_pos=pygame.mouse.get_pos()
        self.angle=0
        self.time=0
        self.maxtime=200
        self.maxpre_time=70
        self.rotate = False
        self.star_r=55
        self.ispre=False
        self.star=self.star.convert()
    def showstar(self):
        self.star_center=(self.rect.centerx+self.star_r*math.cos(self.angle*math.pi/180),self.rect.centery+self.star_r*math.sin(self.angle*math.pi/180))
        self.star_rect=self.star.get_rect(center=self.star_center)
        screen.blit(self.star,self.star_rect)
    def chk_shoot(self):
        #Bulletgroup
        if self.ispre:
            if self.pre_time<self.maxpre_time:
                self.pre_time+=1
                self.starap=self.pre_time*3
                self.star.set_alpha(self.starap)
                self.showstar()
            else:
                self.time=0
                light=Light(self)
                player.Toolsgroup.add(light)
                self.ispre=False
                
        #self.prepare()
    def encold(self):
        if self.time<self.maxtime:
            self.time+=1
        else:
            self.time=self.maxtime                
    def prepare(self):
        self.pre_time=0
        self.ispre=True
    def punched(self):
        self.pos0 = vect(0, 0)
        self.pos1 = vect(self.rect.centerx, self.rect.centery)   
        self.pos2=vect(self.drict_pos[0],self.drict_pos[1])
        self.arch = self.pos2 - self.pos1
        self.angle = self.pos0.angle_to(self.arch)
    def f_rotate(self):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            self.center = self.rect.center
            
            self.image = pygame.transform.rotate(self.original, -self.angle )
            self.rect = self.image.get_rect(center=self.center)
    def update(self):
        self.drict_pos=pygame.mouse.get_pos()        
        self.rect= self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        self.punched()
        self.f_rotate()
        self.chk_shoot()
        self.encold()
        if self.owner.israilgun:
            screen.blit(self.image,self.rect)
        

class Light(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Light,self).__init__()
        self.live=200
        self.power=500
        self.owner=owner
        self.angle=self.owner.angle
        self.image=self.images[0]
        self.image1=self.images[1]
        self.r=800
        self.centerx=self.owner.rect.centerx+self.r*math.cos(self.angle*math.pi/180)
        self.centery=self.owner.rect.centery+self.r*math.sin(self.angle*math.pi/180)
        self.rect=self.image.get_rect(center=(self.centerx,self.centery))
        self.original0 = self.image
        self.original1 = self.image1
        self.center = self.rect.center            
        self.image= pygame.transform.rotate(self.original0, -self.angle )
        self.image1= pygame.transform.rotate(self.original1, -self.angle )
        self.rect = self.image.get_rect(center=self.center)
        #self.image=self.image.convert()
        self.list=pygame.sprite.spritecollide(self,enemies,False, pygame.sprite.collide_mask)
        player.railgun.time+=len(self.list)*50
        for one in self.list:
            one.hurt(self.power)
        
    def update(self):
        global enemies
        self.live-=1
        
        if self.live%2!=0:
           screen.blit(self.image,self.rect)
        else:
            screen.blit(self.image1,self.rect)
        if self.live<=0:
            self.kill()
class Missle(pygame.sprite.Sprite):
    def __init__(self,x,y,isdrone):
        super(Missle,self).__init__()
        #pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        if isdrone:
            self.image = self.images[1]
            self.power=20
        else:
            self.image = self.images[0]
            self.power=25
        # colorkey = self.image.get_at((0, 1))
        # self.image.set_colorkey(colorkey, RLEACCEL)
        
        self.angle = 0
        self.x_speed = 2
        self.y_speed = 2
        self.speed = 3
        self.target=None
        self.rotate = False
        self.choose()
    def move(self):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            self.center = self.rect.center
            
            self.image = pygame.transform.rotate(self.original, -self.angle )
            self.rect = self.image.get_rect(center=self.center)
            #print(self.rect)
        #print(self.rotate)
        self.radangle = self.angle * math.pi / 180
        self.x_speed = self.speed * math.cos(self.radangle)
        self.y_speed = self.speed * math.sin(self.radangle)
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
    def choose(self):
        global enemies
        enemieslist=enemies
        #self.lenlist=[]
        self.min=100000
        #for self.one1 in enemies:
            #self.enemieslist.append(self.one1)
        for self.chen in enemieslist:
            if self.chen is not None:
                self.p1=vect(self.chen.rect.centerx,self.chen.rect.centery)
                self.p2=vect(self.rect.centerx,self.rect.centery)
                self.vect=self.p1-self.p2
                self.length=vect.length(self.vect)
                if self.min>self.length:
                    self.min=self.length
                    self.target=self.chen
                    self.arch=self.vect
        '''
        for self.index in range(len(self.enemieslist)):
            if self.lenlist[self.minindex]>self.lenlist[self.index]:
                self.minindex=self.index
                #print(self.minindex)
        try:
            self.target=self.enemieslist[self.minindex]
        except:
            pass
        '''
    
    def punched(self):
        self.pos0 = vect(0, 0)
        self.pos1 = vect(self.rect.centerx, self.rect.centery)   
        self.pos2=vect(self.target.rect.centerx,self.target.rect.centery)
        self.arch = self.pos2 - self.pos1
        self.angle = self.pos0.angle_to(self.arch)
    
    def display(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def update(self):
        if self.target==None:
            self.kill()
        else:
            if self.target.alive():                
                self.punched()
            else:                
                self.choose()    
        self.move()
        
        self.display()
class Explosion(pygame.sprite.Sprite):
    
    animcycle = 2
    def __init__(self, actor):
        super(Explosion,self).__init__()
        #pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life = 0

    def update(self):
        self.life = self.life + 1
        self.index=self.life//self.animcycle
        if self.index>=5:
            self.index=5
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        screen.blit(self.image,(self.rect.x,self.rect.y))
        if self.life >= 25: self.kill()
class Enemy(pygame.sprite.Sprite):
    shootime=360
    def __init__(self):
        super(Enemy,self).__init__()
        #self.lis=['enemy U.png','enemy D.png','enemy L.png','enemy R.png']        
        self.iplist=[(0,-1),(0,1),(-1,0),(1,0)]
        self.x=random.randint(0,1200)
        self.y=random.randint(0,700)
        self.live=50        
        self.enname=random.randint(0,3)
        self.image=self.images[self.enname]
        #self.image=pygame.image.load(self.ename).convert()
        screen.blit(self.image,(self.x,self.y))
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        
        self.shootime=360
    def move(self):
        self.enip=self.iplist[self.enname]
        self.x+=self.enip[0]
        self.y+=self.enip[1]
        self.rect = self.image.get_rect()
        if self.x <0:
            self.kill()
        elif self.x+60 > 1200:
            self.kill() 
        if self.y < 0:
            self.kill() 
        elif self.y+60 > 700:
            self.kill()
        self.rect.x=self.x
        self.rect.y=self.y
    def display(self):
        screen.blit(self.image,(self.x,self.y))
        self.rect = self.image.get_rect()        
    def hurt(self,power):
        self.power=power
        self.live-=self.power
        if self.live<=0:
            if player.iscrazy:
                self.distory(1,1,0,2)
            else:
                self.distory(1,1,2,2)
    def distory(self,a,b,c,d):
        global score,energy,misslenum,Bombgroup
        score+=a
        misslenum+=b
        energy+=c
        player.addlive(d)
        boo=Explosion(self)
        Bombgroup.add(boo)
        self.kill()          
    def shoot(self):
        global enBulletgroup
        self.bullet1=BulletCoordinate(self.x,self.y,0,True)
        self.bullet2=BulletCoordinate(self.x,self.y,1,True)
        self.bullet3=BulletCoordinate(self.x,self.y,2,True)
        self.bullet4=BulletCoordinate(self.x,self.y,3,True)
        enBulletgroup.add(self.bullet1)
        enBulletgroup.add(self.bullet2)
        enBulletgroup.add(self.bullet3)
        enBulletgroup.add(self.bullet4)
    def update(self):
        if self.shootime>0:
            self.shootime-=1
        else:
            self.shoot()
            self.shootime=Enemy.shootime
        self.display()
        self.move()
class BulletCoordinate(pygame.sprite.Sprite):
    def __init__(self,x,y,plname,ifen):
        super(BulletCoordinate,self).__init__()
        self.plname=plname
        self.mi= self.images[self.plname]
        #self.dic3={'enemy U.png','enemy D.png','enemy L.png':'enemyL.png','enemy R.png':'enemyR.png'}
        #self.dic1={'plane U.png':'enemyU.png','plane D.png':'enemyD.png','plane L.png':'enemyL.png','plane R.png':'enemyR.png'}
        self.iplist=[(0,-5),(0,5),(-5,0),(5,0)]        
        self.x=x+15
        self.power=5
        self.y = y+15        
        if ifen:
            self.power=10                        
        else:
            self.power=5
        #self.mi=pygame.image.load(self.miname).convert()
        self.rect=self.mi.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def move(self):
        self.mip=self.iplist[self.plname]        
        self.x+=self.mip[0]
        self.y+=self.mip[1]
        self.rect=self.mi.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        if (self.x <=0) or (self.x+30 >= 1200) or (self.y <= 0) or (self.y+30 >= 700):            
            self.kill()            
    def display(self):
        screen.blit(self.mi,(self.x,self.y))
    def update(self):
        self.move()
        self.display()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.plane=0
        self.surf = self.images[self.plane]
        self.angle=0
        self.speed=4
        self.Misslegroup=Misslegroup
        self.Bulletgroup=Bulletgroup
        self.Toolsgroup=Toolsgroup
        #self.surf = pygame.image.load(self.plane).convert()
        self.rect = self.surf.get_rect()
        self.israilgun=True
        self.rotate = False
        self.railgun=Railgun(self)
        self.Toolsgroup.add(self.railgun)
        self.crazyeg=0
        self.iscrazy=False
    def rotateit(self,ang):
        if not self.rotate:
                self.original = self.surf
                self.rotate = True
        if self.rotate:
            self.angle+=ang
            self.angle=self.angle%360
            self.center = self.rect.center            
            self.surf = pygame.transform.rotate(self.original, self.angle)            
            self.rect = self.surf.get_rect(center=self.center)
    def update(self, pressed_keys):
        global score,live,energy,goldbody,GOLDBODY
        if pressed_keys[K_UP] or pressed_keys[K_w]:            
            self.rect.move_ip(self.speed*math.sin((self.angle/180)*math.pi),self.speed*math.cos((self.angle/180)*math.pi))
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(-self.speed*math.sin((self.angle/180)*math.pi),-self.speed*math.cos((self.angle/180)*math.pi))
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:            
            self.rotateit(2)            
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:            
            self.rotateit(-2)
        if self.rect.left <=0:
            self.rect.left = 0
        elif self.rect.right >= 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
        if pressed_keys[K_SPACE]:
            self.shoot()
        if pressed_keys[K_f] and (energy>=10) and self.goldbody==False:
            self.golden()
        if pressed_keys[K_c] and (energy>=20):            
            self.killall()
        if self.crazyeg >0:
            self.crazyeg-=1
        else:
            self.iscrazy=False
            self.railgun.maxtime=200
            self.railgun.maxpre_time=70
        #if self.israilgun:
            
            
                
        #if pressed_keys[K_k] and misslenum>0:
             
        
    def golden(self):
        global live,energy,goldbody,GOLDBODY
        energy-=10
        self.addlive(20)
        self.goldbody=True
        pygame.time.set_timer(GOLDBODY,5000)
        
    def addlive(self,liv1):
        global live
        live+=liv1
        if live>=100:
            live=100    
        
    def hurt(self,power):
        global live
        self.power=power
        live-=self.power
    def killall(self):
        global enBulletgroup,enemies,score,energy,live,misslenum
        screen.blit(self.bangbackground,(0,0))
        #screen.fill((255,255,255))
        energy-=20
        live=100
        misslenum+=10
        pygame.display.update()
        pygame.time.delay(1000)
        for en2 in enemies:           
            en2.distory(1,0,1,0)
        for eb2 in enBulletgroup:
            eb2.kill()
    def distory(self):
        global live,running
        if live<=0:            
            self.kill()
            running=False
    def shootmissle(self):
        global misslenum
        misslenum-=1
        newMissle=Missle(self.rect.centerx,self.rect.centery,False)
        self.Bulletgroup.add(newMissle)
    def crazy(self):
        global energy
        self.railgun.maxtime=self.railgun.maxtime*0.2
        self.railgun.maxpre_time=0 #self.railgun.maxpre_time*0.2
        self.crazyeg=360
        self.iscrazy=True
        energy-=20
    def display(self):
        screen.blit(self.surf,(self.rect.x,self.rect.y))
        if self.goldbody:
            self.starrect=self.star.get_rect(center=self.rect.center)
            screen.blit(self.star,self.starrect)
        

main_dir = os.path.split(os.path.abspath(__file__))[0]
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs
def load():
    #img = load_image('explosion1.png')
    #Explosion.images = [img,pygame.transform.flip(img, 1, 1)]
    img = load_image('fire.png')
    Explosion.images = [pygame.transform.scale(img,(15,15)),pygame.transform.scale(img,(45,45)),pygame.transform.scale(img,(75,75)),pygame.transform.scale(img,(90,90)),pygame.transform.scale(img,(120,120)),pygame.transform.scale(img,(90,90))]
    Missle.images=[pygame.transform.scale(load_image('bigmissle.png'),(60,20)),pygame.transform.scale(load_image('dronemissle.png'),(40,15))]
    Player.images=[pygame.transform.smoothscale(load_image('ground.png'),(60,80))]
    BulletCoordinate.images=load_images('bulletU.png','bulletD.png','bulletL.png','bulletR.png')
    Player.star=pygame.transform.smoothscale(load_image('star2.png'),(60,60))
    enemyimage=pygame.transform.smoothscale(load_image('enemy.png'),(100,75))
    Enemy.images=[pygame.transform.rotate(enemyimage,90),pygame.transform.rotate(enemyimage,270),enemyimage,pygame.transform.rotate(enemyimage,180)]
    Railgun.image=pygame.transform.smoothscale(load_image('gun.png'),(100,30))
    Railgun.star=pygame.transform.smoothscale(load_image('gunstar3.png'),(15,15))
    Player.bangbackground=load_image('bang.jpg')
    
    Light.images=[pygame.transform.smoothscale(load_image('2.jpg').convert_alpha(),(1500,10)),pygame.transform.smoothscale(load_image('3.png').convert_alpha(),(1500,10))]


def cheekp():
        global goldbody,score,energy
        get_dic=pygame.sprite.groupcollide(enemies,Bulletgroup,False,False)                                    
        lost_list=pygame.sprite.spritecollide(player,enBulletgroup,True)
        for one_en in get_dic:
            power=0
            if get_dic[one_en] is not None:
                for one_bl in get_dic[one_en]:
                    power+=one_bl.power
                one_en.hurt(power)
                get_dic[one_en]=None
        if player.goldbody is not True:        
            for one2 in lost_list:
                player.hurt(10)
                player.distory()
        else:
            dist_list=pygame.sprite.spritecollide(player,enemies,False)
            for one3 in dist_list:
                one3.distory(1,0,1,0)

def showscore(live,score,energy,misslenum):
    textfont=pygame.font.SysFont('arial',30) #创建文本对象，大小30
    t1=textfont.render('LIVE:'+str(live)+' score:'+str(score)+' Gun energy:'+str(player.railgun.time)+' Missle(press K):'+str(misslenum)+' Energy:'+str(energy),True,(255,0,0))
    t2=textfont.render('Your energy is more than 20 ,press SHIFT to use a special power or key C for a super BOOM!!!',True,(128,0,255))#生成平滑的红色字符串
    t3=textfont.render('Your energy is more than 10 ,press key F to use GOLDBODY!!!',True,(128,0,255))
    screen.blit(t1,[50,20]) #在窗口显示
    if energy>=20:
        screen.blit(t2,[50,80])
    if energy>=10:
        screen.blit(t3,[50,50])

            
pygame.init()
FPS=60
FPSClock=pygame.time.Clock()
E1=pygame.USEREVENT
pygame.time.set_timer(E1,1000)
addtime=2000
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,addtime)
#SHOOT=pygame.USEREVENT + 2
#pygame.time.set_timer(SHOOT,shoottime)
GET_FASTER=pygame.USEREVENT + 2
pygame.time.set_timer(GET_FASTER,5000)
GOLDBODY=pygame.USEREVENT + 3 
enemies = pygame.sprite.Group()
Bulletgroup=pygame.sprite.Group()
Misslegroup=pygame.sprite.Group()
enBulletgroup=pygame.sprite.Group()
Bombgroup=pygame.sprite.Group()
Toolsgroup=pygame.sprite.Group()
Player.goldbody=False
misslenum=40
score=0
live=100
energy=0
screen = pygame.display.set_mode((1200, 700))
#screen.fill((0,0,0))
load()
player = Player()
cheek=False
running = 'r'
RUN=True
background=pygame.transform.smoothscale(load_image('grass.jpg'),(1200,700))
pygame.display.set_caption('PLANE WAR!')

while RUN:
    if running=='r':
        #screen.blit(background,(0,0))
        screen.fill((0,0,0))
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:                    
                    running = False
                if event.key == K_p:
                    running = 'p'
                '''
                if event.key == K_l:
                    if player.israilgun:
                        player.israilgun=False
                    else:
                        player.israilgun=True
                '''
                if event.key == K_q and misslenum>0:
                    player.shootmissle()
                    
                if (event.key == K_RSHIFT or event.key == K_LSHIFT) and energy>=20:
                    player.crazy()
                    
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player.railgun.time>=player.railgun.maxtime and  (not player.railgun.ispre):
                player.railgun.prepare()
            if event.type==ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                '''
            if event.type==SHOOT:                
                for en1 in enemies:
                    en1.shoot()
                '''
            if event.type==GET_FASTER:
                addtime-=100
                if addtime<=500:
                    addtime=500
                pygame.time.set_timer(ADDENEMY,addtime)
                Enemy.shootime-=20
                if Enemy.shootime<=40:
                    Enemy.shootime=40
                #pygame.time.set_timer(SHOOT,shoottime)
                
            if player.goldbody:    
                if event.type==GOLDBODY:
                    player.goldbody=False
        cheekp()                
        player.display()
        Bulletgroup.update()
        enBulletgroup.update()
        enemies.update()
        Toolsgroup.update()
        Bombgroup.update()
        showscore(live,score,energy,misslenum)        
        pygame.display.update()
        FPSClock.tick(FPS)
    elif running == 'p':
        screen.fill((135,206,250))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    RUN = False
                    sys.exit()
                if event.key == K_r:
                    running = 'r'    
            elif event.type == QUIT:
                RUN = False
                sys.exit()
        ptextfon=pygame.font.SysFont('arial',60)
        ptext=ptextfon.render('Parking,press R to continue',True,(128,0,255))
        screen.blit(ptext,[100,300])
        pygame.display.update()
        FPSClock.tick(FPS)
    elif running == False:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    RUN = False
                    sys.exit()
            elif event.type == QUIT:
                RUN = False
                sys.exit()
        textfon=pygame.font.SysFont('arial',60)
        text=textfon.render('GAME OVER!!! PLAY AGAIN??'+'Your score is: '+str(score),True,(255,0,0))
        screen.blit(text,[100,300])    
        pygame.display.update()
        FPSClock.tick(FPS)

        
