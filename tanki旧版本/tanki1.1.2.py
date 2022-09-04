import pygame
import sys,os
from pygame.locals import *
import random
import math

vect = pygame.Vector2
class Gun(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Gun,self).__init__()
        self.owner=owner
        self.rect=self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        #self.x=owner.rect.centerx
        #self.y=owner.rect.centery
        self.drict_pos=pygame.mouse.get_pos()
        self.angle=0
        self.time=0
        self.blspeed=0
        self.rotate = False
        self.punched()
    def punched(self):
        self.pos0 = vect(0, 0)
        self.pos1 = vect(self.rect.centerx, self.rect.centery)   
        self.pos2=vect(self.drict_pos[0],self.drict_pos[1])
        self.arch = self.pos2 - self.pos1
        self.angle = self.pos0.angle_to(self.arch)
    def encold(self):
        if self.time<self.maxtime:
            self.time+=1
        else:
            self.time=self.maxtime
    def shoot(self):
        pass
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
        self.encold()
        screen.blit(self.image,self.rect)


        
class Meltgun(Gun):
    def __init__(self,owner):
        super(Meltgun,self).__init__(owner)    
        self.ispre=False
        self.maxtime=20
        self.r=51
        self.angle0=11.5
        self.turn=1
        self.blspeed=8
    def shoot(self):
        light1=Shortlight(self)
        game.Bulletgroup.add(light1) 
        game.grounds.add(light1)
        if self.turn==1:
            self.turn=2
        else:
            self.turn=1
        self.time=0
    '''
    def update(self):
        super(Meltgun,self).update()
    '''   

            
class Shortlight(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Shortlight,self).__init__()
        self.live=120
        self.power=20
        self.owner=owner
        self.speed=self.owner.blspeed
        if self.owner.turn==1:
            self.angle0=self.owner.angle+self.owner.angle0
        elif self.owner.turn==2:
            self.angle0=self.owner.angle-self.owner.angle0
        self.radangle0=self.angle0*math.pi/180
        self.radangle=self.owner.angle*math.pi/180
        self.center=(self.owner.rect.centerx+self.owner.r*math.cos(self.radangle0),self.owner.rect.centery+self.owner.r*math.sin(self.radangle0))
        self.original = self.image
        self.image= pygame.transform.rotate(self.original, -self.owner.angle)         
        self.rect=self.image.get_rect(center=self.center)
    def move(self):
        self.rect.move_ip(self.speed*math.cos(self.radangle),self.speed*math.sin(self.radangle))
        if self.rect.left <=0:
            self.kill()
        elif self.rect.right >= 1200:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        elif self.rect.bottom >= 700:
            self.kill()
    def update(self):
        self.move()
        screen.blit(self.image,self.rect)

        
class Railgun(Gun):
    def __init__(self,owner):
        super(Railgun,self).__init__(owner)
        self.maxtime=200
        self.ispre=False
        self.starlist=[]
        
    def showstar(self):
        self.star_center=(self.rect.centerx+self.star_r*math.cos(self.angle*math.pi/180),self.rect.centery+self.star_r*math.sin(self.angle*math.pi/180))
        self.star_rect=self.star.get_rect(center=self.star_center)
        #self.star=pygame.transform.scale(load_image('gunstar2.png'),(self.starscale,self.starscale))
        screen.blit(self.star,self.star_rect)
    def chk_shoot(self):
        self.maxpre_time=self.maxtime*0.39
        if self.ispre:
            if self.pre_time<self.maxpre_time:
                self.pre_time+=1
            else:
                self.time=0
                light=Light(self)
                game.grounds.add(light)
                self.ispre=False
                self.star.kill()
                del self.star
                
        #self.prepare()                
    def shoot(self):
        
        self.pre_time=0
        self.ispre=True
        self.star=Star(self)
        game.allsp.add(self.star)
    def update(self):
        self.drict_pos=pygame.mouse.get_pos()        
        self.rect= self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        self.punched()
        self.f_rotate()
        self.chk_shoot()
        self.encold()
        screen.blit(self.image,self.rect)
class Star(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Star,self).__init__()
        self.owner=owner
        self.star_r=53        
        self.image=self.images[1]
        self.center=(self.owner.rect.centerx+self.star_r*math.cos(self.owner.angle*math.pi/180),self.owner.rect.centery+self.star_r*math.sin(self.owner.angle*math.pi/180))
        self.rect=self.image.get_rect(center=self.center)
        
    def update(self):
        self.center=(self.owner.rect.centerx+self.star_r*math.cos(self.owner.angle*math.pi/180),self.owner.rect.centery+self.star_r*math.sin(self.owner.angle*math.pi/180))
        self.rect=self.image.get_rect(center=self.center)
        self.starindex=self.owner.pre_time//4
        self.image=self.images[self.starindex]
        screen.blit(self.image,self.rect)
class Light(pygame.sprite.Sprite):
    def __init__(self,owner):
        super(Light,self).__init__()
        self.live=120
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
        self.list=pygame.sprite.spritecollide(self,game.enemies,False, pygame.sprite.collide_mask)
        player.railgun.time+=len(self.list)*50
        for one in self.list:
            one.hurt(self.power)
        
    def update(self):
        
        self.live-=1
        self.num=self.live//2
        if self.num%2!=0:
           screen.blit(self.image,self.rect)
        else:
            screen.blit(self.image1,self.rect)
        
        if self.live<=0:
            self.kill()
            del self




        
class Explosion(pygame.sprite.Sprite):
    
    animcycle = 2
    def __init__(self, actor):
        super(Explosion,self).__init__()
        #pygame.sprite.Sprite.__init__(self, self.containers),,pygame.transform.scale(load_image('fire1.png'),(90,90))
        self.image = self.images[0]
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life = 0

    def update(self):
        
        self.life = self.life + 1
        self.index=self.life//self.animcycle
        if self.index>=4:
            self.index=4
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        
        screen.blit(self.image,self.rect)
        if self.life >= 40:
            game.grounds.add(Dirt(self.actor))
            
            self.kill()
            del self.actor,self
class Dirt(pygame.sprite.Sprite):
    def __init__(self, actor):
        super(Dirt,self).__init__()
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life =120
    def update(self):
        
        self.life = self.life - 1
        screen.blit(self.image,self.rect)
        if self.life <=0:
            self.kill()
            del self
class Enemy(pygame.sprite.Sprite):
    maxshootime=360
    live=50
    def __init__(self):
        super(Enemy,self).__init__()
        #self.lis=['enemy U.png','enemy D.png','enemy L.png','enemy R.png']
        self.iplist=[(0,-1),(0,1),(-1,0),(1,0)]
        self.x=random.randint(0,1200)
        self.y=random.randint(0,700)        
        self.enname=random.randint(0,3)
        self.image=self.images[self.enname]
        #self.image=pygame.image.load(self.ename).convert()
        #screen.blit(self.image,(self.x,self.y))
        self.rect = self.image.get_rect(center=(self.x,self.y))        
        self.shootime=0
    def move(self):
        self.enip=self.iplist[self.enname]
        self.rect.move_ip(self.enip[0],self.enip[1])
        #self.x+=self.enip[0]
        #self.y+=self.enip[1]
        
        if self.rect.x <0:
            self.kill()
        elif self.rect.x+60 > 1200:
            self.kill() 
        if self.rect.y < 0:
            self.kill() 
        elif self.rect.y+60 > 700:
            self.kill()
        #self.rect = self.image.get_rect()
    def display(self):
        screen.blit(self.image,self.rect)
    def hurt(self,power):
        self.live-=power
        
        if self.live<=0:
            Damage(power,(64,0,128),30,self.rect.center)
            if player.iscrazy:
                self.distory(1,1,0,2)
            else:
                self.distory(1,1,2,2)
        else:
            Damage(power,(180,180,180),25,self.rect.center)
    def distory(self,a,b,c,d):
        
        game.score+=a
        game.energy+=c
        player.addlive(d)
        game.grounds.add(Explosion(self))
        self.kill()
        del self
    def shoot(self):
        
        for i in range(4):
            self.bullet=BulletCoordinate(self.rect.centerx,self.rect.centery,i)
            game.enBulletgroup.add(self.bullet)
            game.allsp.add(self.bullet)
        
    def update(self):
        if self.shootime<Enemy.maxshootime:
            self.shootime+=1
        else:
            self.shoot()
            self.shootime=0
        self.display()
        self.move()
        
class BulletCoordinate(pygame.sprite.Sprite):
    power=10
    def __init__(self,x,y,plname):
        super(BulletCoordinate,self).__init__()
        self.plname=plname
        self.image= self.images[self.plname]
        #self.dic3={'enemy U.png','enemy D.png','enemy L.png':'enemyL.png','enemy R.png':'enemyR.png'}
        #self.dic1={'plane U.png':'enemyU.png','plane D.png':'enemyD.png','plane L.png':'enemyL.png','plane R.png':'enemyR.png'}
        self.iplist=[(0,-5),(0,5),(-5,0),(5,0)]                
        #self.image=pygame.image.load(self.miname).convert()
        self.rect=self.image.get_rect(center=(x,y))
    def move(self):
        self.mip=self.iplist[self.plname]        
        self.rect.move_ip(self.mip[0],self.mip[1])
        if (self.rect.x <=0) or (self.rect.x+30 >= 1200) or (self.rect.y <= 0) or (self.rect.y+30 >= 700):            
            self.kill()
            del self
        #self.rect=self.image.get_rect()
    def display(self):
        screen.blit(self.image,self.rect)
    def update(self):
        self.move()
        self.display()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.plane=0
        self.image = self.images[self.plane]
        self.angle=0
        self.speed=4
        self.level=0
        self.maxlive=100
        #self.image = pygame.image.load(self.plane).convert()
        self.rect = self.image.get_rect()
        self.israilgun=True
        self.rotate = False
        self.railgun=Railgun(self)
        self.meltgun=Meltgun(self)
        self.gunlist=[self.railgun,self.meltgun]
        self.gun=self.meltgun
        self.goldtime=0
        self.defendtime=0
        self.subnum=1
        self.crazyeg=0
        self.iscrazy=False
        self.oldscore=game.score
        self.gun.old_maxtime=self.gun.maxtime
        self.gun.oldblspeed=self.gun.blspeed
    def rotateit(self,ang):
        if not self.rotate:
                self.original = self.image
                self.rotate = True
        if self.rotate:
            self.angle+=ang
            self.angle=self.angle%360
            self.center = self.rect.center            
            self.image = pygame.transform.rotate(self.original, self.angle)            
            self.rect = self.image.get_rect(center=self.center)
    def move(self):
        if game.pressed_keys[K_UP] or game.pressed_keys[K_w]:            
            self.rect.move_ip(self.speed*math.sin((self.angle/180)*math.pi),self.speed*math.cos((self.angle/180)*math.pi))
        if game.pressed_keys[K_DOWN] or game.pressed_keys[K_s]:
            self.rect.move_ip(-self.speed*math.sin((self.angle/180)*math.pi),-self.speed*math.cos((self.angle/180)*math.pi))
        if game.pressed_keys[K_LEFT] or game.pressed_keys[K_a]:            
            self.rotateit(2)            
        if game.pressed_keys[K_RIGHT] or game.pressed_keys[K_d]:            
            self.rotateit(-2)
        if self.rect.left <=0:
            self.rect.left = 0
        elif self.rect.right >= 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
    def update(self):
        self.move()
        self.cheek()        
        self.display()
        self.gun.update()            
        #self.rect = self.image.get_rect(center=self.rect.center)        
    def ifgrow(self):
        if game.score-self.oldscore>=10:
            self.level+=1
            Damage('LEVEL UP!',(0,255,0),33,self.rect.center)
            self.oldscore=game.score
            self.maxlive+=5
            self.addlive(20)
            for guni in self.gunlist:                
                guni.maxtime=guni.maxtime*(0.95)
                guni.blspeed=guni.blspeed*(1.05)
    
    def if_changegun(self):
        if not self.iscrazy:
            if game.pressed_keys[K_r]:
                self.gun=self.railgun
            elif game.pressed_keys[K_m]:
                self.gun=self.meltgun
            self.gun.old_maxtime=self.gun.maxtime
            self.gun.oldblspeed=self.gun.blspeed
    def addlive(self,liv1):
        
        game.live+=liv1
        
        if game.live>=self.maxlive:
            game.live=self.maxlive
        else:
            Damage(liv1,(0,255,0),30,self.rect.center)
    def defend(self):
        self.isdefend=True
        self.subnum=0.5
        self.defendtime+=500
        game.energy-=10
    def repair(self):
        game.live=self.maxlive
        game.energy-=20
    def cheek(self):
        if game.pressed_keys[K_SPACE]:
            self.shoot()
        if game.pressed_keys[K_f] and (game.energy>=10) and self.isdefend==False:
            self.defend()
        if game.pressed_mouse[0]==1 and self.gun.time>=player.gun.maxtime and (not self.gun.ispre):
            self.gun.shoot()
            
        if self.defendtime>0:
            self.defendtime-=1
        else:
            self.isdefend=False
            self.subnum=1
        if self.crazyeg>0:
            self.crazyeg-=1
        else:
            self.iscrazy=False
            self.gun.blspeed=self.gun.oldblspeed
            self.gun.maxtime=self.gun.old_maxtime
        self.ifgrow()
        self.if_changegun()
    def hurt(self,power):
        
        self.power=power
        game.live-=self.power*self.subnum
        Damage(self.power*self.subnum,(255,0,0),25,self.rect.center)
    def distory(self):
       
        if game.live<=0:            
            self.kill()
            game.running=False
    def crazy(self):
        self.gun.blspeed=self.gun.blspeed*4  
        self.gun.maxtime=self.gun.maxtime*0.2
        #self.railgun.maxpre_time=0 self.railgun.maxpre_time*0.2
        self.crazyeg+=360
        self.iscrazy=True
        game.energy-=20
    def display(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        if self.isdefend:
            self.rect1=self.dfnimg.get_rect(center=self.rect.center)
            screen.blit(self.dfnimg,self.rect1)
        if self.iscrazy:
            self.starrect=self.star.get_rect(center=self.rect.center)
            screen.blit(self.star,self.starrect)
        

class Damage(pygame.sprite.Sprite):
    def __init__(self,num,color,size,center):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.live=60        
        textfont=pygame.font.SysFont('arial',size) #创建文本对象，大小30
        self.image=textfont.render(str(num),True,color)
        self.rect = self.image.get_rect(center=center)
    def update(self):
        self.rect.move_ip(0,-2)
        self.alpha=self.live*6
        self.image.set_alpha(self.alpha)
        screen.blit(self.image,self.rect)
        if self.live>0:
            self.live-=1
        else:
            self.kill()
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
    Explosion.images = [pygame.transform.scale(img,(15,15)),pygame.transform.scale(img,(45,45)),pygame.transform.scale(img,(75,75)),pygame.transform.scale(img,(90,90)),pygame.transform.scale(img,(120,120))]
    #Missle.images=[pygame.transform.scale(load_image('bigmissle.png'),(60,20)),pygame.transform.scale(load_image('dronemissle.png'),(40,15))]
    Player.images=[pygame.transform.smoothscale(load_image('ground2.png'),(60,80))]
    BulletCoordinate.images=load_images('bulletU.png','bulletD.png','bulletL.png','bulletR.png')
    Player.star=pygame.transform.smoothscale(load_image('star2.png'),(60,60))
    Player.dfnimg=pygame.transform.smoothscale(load_image('defendimg.png'),(120,120))
    enemyimage=pygame.transform.smoothscale(load_image('enemy.png'),(100,75))
    Enemy.images=[pygame.transform.rotate(enemyimage,90),pygame.transform.rotate(enemyimage,270),enemyimage,pygame.transform.rotate(enemyimage,180)]
    Railgun.image=pygame.transform.smoothscale(load_image('gun.png'),(100,30))
    Railgun.star=load_image('gunstar2.png')
    Meltgun.image=pygame.transform.smoothscale(load_image('gun2.png'),(100,40))
    Player.bangbackground=load_image('bang.jpg')
    Star.images=[]
    for scale in range(1,21):
        Star.images.append(pygame.transform.scale(load_image('gunstar1.png'),(scale,scale)))
    Dirt.image=pygame.transform.smoothscale(load_image('BlastMark2.png'),(100,100))
    Light.images=[pygame.transform.smoothscale(load_image('2.gif'),(1500,10)),pygame.transform.smoothscale(load_image('3.gif'),(1500,10))]
    Shortlight.image=pygame.transform.smoothscale(load_image('shortlight.png'),(30,10))

def cheekp():
        
        get_dic=pygame.sprite.groupcollide(game.enemies,game.Bulletgroup,False,True)                                    
        lost_list=pygame.sprite.spritecollide(player,game.enBulletgroup,True)        
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
            dist_list=pygame.sprite.spritecollide(player,game.enemies,False)
            for one3 in dist_list:
                one3.distory(1,0,1,0)

def showscore():
    
    textfont=pygame.font.SysFont('arial',30) #创建文本对象，大小30
    t1=textfont.render('live:'+str(game.live)+' score:'+str(game.score)+' level:'+str(player.level)+' Gun energy:'+str(int(player.gun.time))+' energy:'+str(game.energy),True,(255,0,0))
    t2=textfont.render('Your game.energy is more than 20 ,press C to use a special power or key SHIFT for a super BOOM!!!',True,(128,0,255))#生成平滑的红色字符串
    t3=textfont.render('Your game.energy is more than 10 ,press key F to use GOLDBODY!!!',True,(128,0,255))
    screen.blit(t1,[50,20]) #在窗口显示
    if game.energy>=20:
        screen.blit(t2,[50,80])
    if game.energy>=10:
        screen.blit(t3,[50,50])
class game():
    allsp = pygame.sprite.RenderUpdates()#pygame.sprite.Group()
    score=0
    live=100
    energy=10
    RUN=True
    running = 'r'
    pressed_keys = None
    pressed_mouse =None
    enemies = pygame.sprite.Group()
    grounds=pygame.sprite.Group()
    Bulletgroup=pygame.sprite.Group()
    #Misslegroup=pygame.sprite.Group()
    enBulletgroup=pygame.sprite.Group()
    #Bombgroup=pygame.sprite.Group()
    #Toolsgroup=pygame.sprite.Group()

    
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



Player.containers = game.allsp
'''
Enemy.containers = game.enemies,all
Railgun.containers = all
BulletCoordinate.containers = game.enBulletgroup,all
Light.containers = all
Explosion.containers = all
'''
Player.goldbody=False
#misslenum=40
Damage.containers = game.allsp
screen = pygame.display.set_mode((1200, 700))
#screen.fill((0,0,0))
load()
player = Player()
#game.allsp.add(player)
cheek=False

'''
background = pygame.Surface((1200,700))
background.blit(pygame.transform.smoothscale(load_image('grass.jpg'),(1200,700)),(0,0))
screen.blit(background, (0,0))
pygame.display.flip()
'''
icon = pygame.transform.smoothscale(load_image('icon.png'),(32,32)).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption('2D TANK!')

while game.RUN:
    if game.running=='r':
        FPSClock.tick(FPS)
        #screen.blit(background,(0,0))
        screen.fill((0,0,0))
        game.pressed_keys = pygame.key.get_pressed()
        game.pressed_mouse = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:                    
                    game.running = False
                if event.key == K_p:
                    game.running = 'p'
                
                '''
                if event.key == K_q and misslenum>0:
                    player.shootmissle()
                '''    
                if (event.key == K_c) and game.energy>=20:
                    player.crazy()
                if (event.key == K_LSHIFT or event.key == K_RSHIFT) and game.energy>=20:
                    player.repair()    
            if event.type == QUIT:
                game.running = False
            '''
            if event.type == pygame.MOUSEBUTTONDOWN and player.gun.time>=player.gun.maxtime and  (not player.railgun.ispre):
                player.gun.prepare()
            '''
            if event.type==ADDENEMY:
                new_enemy = Enemy()
                game.enemies.add(new_enemy)
                game.allsp.add(new_enemy)
                '''
            if event.type==SHOOT:                
                for en1 in game.enemies:
                    en1.shoot()
                '''
            if event.type==GET_FASTER:
                addtime-=50
                if addtime<=300:
                    addtime=300
                pygame.time.set_timer(ADDENEMY,addtime)
                BulletCoordinate.power+=0.1
                Enemy.live+=1
                Enemy.maxshootime-=15
                if Enemy.maxshootime<=60:
                    Enemy.maxshootime=60
                #pygame.time.set_timer(SHOOT,shoottime)
            '''    
            if player.goldbody:    
                if event.type==GOLDBODY:
                    player.goldbody=False
            '''
        
        
        game.grounds.update()        
        game.allsp.update()
        cheekp()
        #game.enBulletgroup.update()
        #game.enemies.update()
        showscore()
        pygame.display.update()
        
    elif game.running == 'p':
        screen.fill((135,206,250))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.RUN = False
                    sys.exit()
                if event.key == K_r:
                    game.running = 'r'    
            elif event.type == QUIT:
                game.RUN = False
                sys.exit()
        ptextfon=pygame.font.SysFont('arial',60)
        ptext=ptextfon.render('Parking,press R to continue',True,(128,0,255))
        screen.blit(ptext,[100,300])
        pygame.display.update()
        FPSClock.tick(FPS)
    elif game.running == False:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.RUN = False
                    sys.exit()
            elif event.type == QUIT:
                game.RUN = False
                sys.exit()
        textfon=pygame.font.SysFont('arial',60)
        text=textfon.render('GAME OVER!!! PLAY AGAIN??'+'Your score is: '+str(game.score),True,(255,0,0))
        screen.blit(text,[100,300])    
        pygame.display.update()
        FPSClock.tick(FPS)

        
