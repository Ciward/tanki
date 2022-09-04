import math
import os
import random
import sys

import pygame
from pygame.locals import *
import win32api
import win32con

for t in ['开发者：曦微(QQ2273805191)'+
            '\n你想体验新风格的“坦克”吗？'+
            '\n开发者不辞辛苦，不舍昼夜，'+
            '\n牺牲宝贵的学习（娱乐）时间完成此项目q(≧▽≦q)，'+
            '\n请尊重开发者的劳动成果，侵权必究！！'+
            '\n偶尔BUG请谅解',
          '以为这样就结束了?',
          '你想白嫖吗？','不可能的呵呵呵','请给我一个吻进行解锁(●ˇ∀ˇ●)'+'\n没关系，隔着屏幕我也能感受到(❁´◡`❁)']:
    re=win32api.MessageBox(0, t, "关于软件", win32con.MB_YESNO)
if re!=6:
    win32api.MessageBox(0,'你不想。那么白白了＞︿＜', "关于软件", win32con.MB_YESNO)
    sys.exit()
else:
    win32api.MessageBox(0, '我相信你是个诚实的孩子', "关于软件", win32con.MB_YESNO)
win32api.MessageBox(0, "爱你哦(≧∇≦)ﾉ", "关于开发者", win32con.MB_HELP)

f=open('readme.txt')
tex=f.read()
win32api.MessageBox(0, tex, "操作方式", win32con.MB_ICONASTERISK)

vect = pygame.Vector2
class Gun(pygame.sprite.Sprite):
    def __init__(self,owner,drict_pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxtime = None
        self.owner=owner
        self.rect=self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        #self.x=owner.rect.centerx
        #self.y=owner.rect.centery
        self.drict_pos=drict_pos
        self.angle=0
        self.star=None
        self.time=0
        self.energy=1
        self.maxengy=1
        self.blspeed=0
        self.ornangle=0
        self.rotate = False
        self.punched()
    def punched(self):
        self.pos0 = vect(0, 0)
        self.pos1 = vect(self.rect.centerx, self.rect.centery)
        self.pos2=vect(self.drict_pos[0],self.drict_pos[1])
        self.arch = self.pos2 - self.pos1
        self.angle = self.pos0.angle_to(self.arch)
    def encold(self):
        if not self.owner.iscrazy:
            if self.maxtime<self.MINTIME:
                self.maxtime=self.MINTIME
            if self.blspeed>self.MINSPEED:
                self.blspeed=self.MINSPEED
        if self.energy<self.maxengy:
            self.energy+=1
        if self.time<self.maxtime:
            self.time+=1
        else:
            self.time=self.maxtime
    def shoot(self):
        pass
    def change(self):
        pass
    def f_rotate(self):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            self.punched()
            self.center = self.rect.center
            self.image = pygame.transform.rotate(self.original, -self.angle )
            self.rect = self.image.get_rect(center=self.center)
    def f_enrotate(self):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate and (not self.ispre):
            self.punched()
            self.angle=(self.angle+360)%360
            self.center = self.rect.center
            self.chagangle=self.angle-self.ornangle
            if abs(self.chagangle)>self.owner.rotspeed:
                if self.chagangle>0:
                    if self.chagangle<180:
                        self.angle=self.ornangle+self.owner.rotspeed
                    else:
                        self.angle=self.ornangle-self.owner.rotspeed
                else:
                    if self.chagangle>-180:
                        self.angle=self.ornangle-self.owner.rotspeed
                    else:
                        self.angle=self.ornangle+self.owner.rotspeed

            self.image = pygame.transform.rotate(self.original,-self.angle)
            self.ornangle=self.angle%360
            self.rect = self.image.get_rect(center=self.center)
    def chk_shoot(self):
        pass
    def cheek(self):
        pass

    def rand(self, power, range):
        damage=random.randint(-range,range)
        return power+damage
    def update(self,drict_pos,selfpos):
        if self.owner.still<=0:
            self.drict_pos=drict_pos
            self.rect= self.image.get_rect(center=selfpos)
            if self.owner.isen:
                self.f_enrotate()
            else:
                self.f_rotate()
            self.chk_shoot()
        screen.blit(self.image,self.rect)
        self.cheek()
class Bullet(pygame.sprite.Sprite):
    power=0
    def __init__(self,owner,x,y,angle,live,power,speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.live=live
        self.owner=owner
        self.power=power
        self.speed=speed
        self.angle=angle
        self.radangle=self.angle*math.pi/180
        self.center=(x,y)
        self.original = self.image
        self.image= pygame.transform.rotate(self.original, -self.angle)
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
    def dirt(self):
        pass
    def explode(self):
        pass
    def distory(self):
        bullteExplosion(self)
    def update(self):
        if self.live<0:
            self.kill()
        else:
            self.live-=1
        self.dirt()
        self.move()
        screen.blit(self.image,self.rect)
class Missle(Bullet):
    tarR=40
    speed=12
    rotspeed=5
    def __init__(self,owner,x,y,angle,live,power,speed,target):
        super(Missle,self).__init__(owner,x,y,angle,live,power,speed)
        self.target=target
        self.ornangle = angle
        self.randomangle=random.randint(1,359)
        self.radangle1=self.randomangle*math.pi/180
    def punched(self):
        self.pos0 = vect(0, 0)
        self.pos1 = vect(self.rect.centerx, self.rect.centery)
        self.pos2=vect(self.drict_pos[0],self.drict_pos[1])
        self.arch = self.pos2 - self.pos1
        self.angle = self.pos0.angle_to(self.arch)
        self.angle = (self.angle + 360) % 360
        self.chagangle = self.angle - self.ornangle
        if abs(self.chagangle) > self.rotspeed:
            if self.chagangle > 0:
                if self.chagangle < 180:
                    self.angle = self.ornangle + self.rotspeed
                else:
                    self.angle = self.ornangle - self.rotspeed
            else:
                if self.chagangle > -180:
                    self.angle = self.ornangle - self.rotspeed
                else:
                    self.angle = self.ornangle + self.rotspeed

        self.image = pygame.transform.rotate(self.original, -self.angle)
        self.ornangle = self.angle % 360
        self.rect = self.image.get_rect(center=self.rect.center)

    def explode(self):
        exp=Explosion(self)
        exp.isdirt=False
        self.kill()
    def dirt(self):
        mydirt=smallDirt(self)
        mydirt.life=20
        self.drict_pos=(self.target.rect.centerx+self.tarR*math.cos(self.radangle1),
                        self.target.rect.centery+self.tarR*math.sin(self.radangle1))
        if self.target.alive():
            self.punched()
        self.radangle = self.angle * math.pi / 180
class Dirt(pygame.sprite.Sprite):
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life =60
    def update(self):

        self.life = self.life - 1
        screen.blit(self.image,self.rect)
        if self.life <=0:
            self.kill()

class Misslegun(Gun):
    MINTIME=120
    MINSPEED=40
    Angles=[-18,18,-10,-10,0]
    r=55
    def __init__(self,owner,drict_pos):
        super(Misslegun,self).__init__(owner,drict_pos)
        self.ispre=False
        self.pretime=0
        self.maxtime = 300
        self.target=None
    def shoot(self):
        for e in game.enemies:
            if vect.length(vect(pygame.mouse.get_pos()) - vect(e.rect.center)) < 150:
                self.target=e
        if self.target is not None:
            #self.ispre=True
            self.pretime=40
            self.shootindex=0
            self.time=0
    def chk_shoot(self):
        if self.pretime>0:
            if self.pretime%8==0:
                self.realshoot(self.shootindex)
                self.shootindex += 1
            self.pretime -= 1
    def realshoot(self,index):
        self.radangle0 = (self.angle+self.Angles[index]) * math.pi / 180
        x = self.rect.centerx + self.r * math.cos(self.radangle0)
        y = self.rect.centery + self.r * math.sin(self.radangle0)
        power=self.owner.bombpower*0.5
        Missle(self, x, y, self.angle, 300, self.rand(int(power),int(power*0.5)),
               Missle.speed,self.target)
        game.missle_sound.play()
class Gauss(Gun):
    MINTIME=200
    MINSPEED=80
    def __init__(self,owner,drict_pos):
        super(Gauss,self).__init__(owner,drict_pos)
        self.maxtime=200
        self.time=200
        self.blspeed=60
        self.ispre=False
        self.r=50
        self.maxpre_time=180
        self.pre_time=0
        self.stime=50
        self.p=self.pre_time/self.maxpre_time
        self.wing0=Wing(self,True)
        self.wing1=Wing(self,False)
    def shoot(self):
        if self.owner.iscrazy:
            self.realshoot()
            self.pre_time=100
        else:
            self.pre_time=0
            self.ispre=True
            #self.star=Star(self)
    def chk_shoot(self):
        self.maxpre_time=180
        if self.ispre:
            self.stime+=1
            if self.stime>=50:
                game.chargesnd.play()
                self.stime=0
            self.p=self.pre_time/self.maxpre_time
            if game.pressed_mouse[0]==1:
                if self.pre_time<self.maxpre_time:
                    self.pre_time+=1
            else:
                self.realshoot()
    def cheek(self):
        self.wing0.update()
        self.wing1.update()
    def realshoot(self):
        self.ispre=False
        self.radangle=self.angle*math.pi/180
        x=self.rect.centerx+self.r*math.cos(self.radangle)
        y=self.rect.centery+self.r*math.sin(self.radangle)
        pow=self.owner.bombpower*(0.25+0.75*self.p)
        Ebomb(self,x,y,self.angle,500,self.rand(pow,int(pow*0.5)),self.blspeed)
        self.time=0
        self.pre_time=0
        self.p=self.pre_time/self.maxpre_time
class Wing(pygame.sprite.Sprite):
    def __init__(self,owner,n):
        pygame.sprite.Sprite.__init__(self)
        self.owner=owner
        self.n=n
        self.r=20
        if self.n:
            self.image=self.images[0]
        else:
            self.image=self.images[1]
        self.original = self.image
    def update(self):
        if self.n:
            self.angle=self.owner.angle-self.owner.p*80
            self.center=(self.owner.rect.centerx+self.r*math.cos((self.owner.angle+100)*math.pi/180),
                         self.owner.rect.centery+self.r*math.sin((self.owner.angle+100)*math.pi/180))
        else:
            self.angle=self.owner.angle+self.owner.p*80
            self.center=(self.owner.rect.centerx+self.r*math.cos((self.owner.angle-100)*math.pi/180),
                         self.owner.rect.centery+self.r*math.sin((self.owner.angle-100)*math.pi/180))
        self.image= pygame.transform.rotate(self.original,-self.angle)
        self.rect=self.image.get_rect(center=self.center)
        screen.blit(self.image,self.rect)
class Ebomb(Bullet):
    def __init__(self,owner,x,y,angle,live,power,speed):
        self.realpower=power
        super(Ebomb,self).__init__(owner,x,y,angle,live,power,speed)
        self.p=self.owner.p
        self.R=200+400*self.p
        self.power=0
    def explode(self):
        self.pos1 = vect(self.rect.centerx, self.rect.centery)
        Eexplosion(self)
        for e in game.enemies:
            pos2=vect(e.rect.centerx, e.rect.centery)
            vec=pos2-self.pos1
            length=vec.length()
            if length<=self.R:
                e.hurt(self.realpower)
                e.shock(60+200*self.p)
                if length>1:
                    angle = vect(0,0).angle_to(vec)
                    #print(angle)
                    Electric(self,((self.rect.centerx+e.rect.centerx)/2,(self.rect.centery+e.rect.centery)/2),
                             length,angle)
        self.kill()
    def dirt(self):
        birdDirt(self)
class birdDirt(Dirt):
    def __init__(self,owner):
        super(birdDirt,self).__init__(owner)
        self.owner=owner
        self.angle=self.owner.angle
        self.life=20
        self.original = self.image
        self.image= pygame.transform.rotate(self.original,-self.angle)
        self.rect=self.image.get_rect(center=self.owner.rect.center)
class Electric(Dirt):
    def __init__(self,owner,pos,len,angle):
        super(Electric,self).__init__(owner)
        self.owner=owner
        self.angle=angle
        self.images=[]
        if len<=300:
            self.life=80
        elif len>300 and len<=800:
            self.life=40
        elif len>=1000:
            self.life=20
        self.index=1
        for img in self.originalimages:
            #original = img
            a=pygame.transform.smoothscale(img,(int(len),18))

            self.images.append(pygame.transform.rotate(a,-self.angle))

        self.image=self.images[self.index]
        self.rect=self.image.get_rect(center=pos)
    def update(self):
        self.index=self.life%3
        self.image=self.images[self.index]
        self.life = self.life - 1
        screen.blit(self.image,self.rect)
        if self.life <=0:
            self.kill()

class Firegun(Gun):
    MINTIME=1
    MINSPEED=40
    def __init__(self,owner,drict_pos):
        self.image=self.images[0]
        super(Firegun,self).__init__(owner,drict_pos)
        self.maxtime=1
        self.speed=15
        self.oldspeed=self.speed
        self.ispre=False
        self.r=50
        self.star_r=70
        self.firelive=10
        self.starimage=self.images[1]
        self.originalstar=self.starimage
        self.energy=200
        self.angle0=10
    def cheek(self):
        if self.owner.iscrazy:
            self.speed=40
            self.time=200
        else:
            self.speed=self.oldspeed
            self.oldspeed=self.speed
    def encold(self):
        if not self.owner.iscrazy:
            if self.maxtime<self.MINTIME:
                self.maxtime=self.MINTIME
            if self.speed>self.MINSPEED:
                self.speed=self.MINSPEED
        if self.time<self.energy:
            self.time+=1
        else:
            self.time=self.energy
    def shoot(self):
        self.time-=4
        #print(self.power)

        self.anglelist=[i+self.angle for i in range(-self.angle0,self.angle0+2,2)]
        self.radangle=self.angle*math.pi/180
        x=self.rect.centerx+self.r*math.cos(self.radangle)
        y=self.rect.centery+self.r*math.sin(self.radangle)

        for i in self.anglelist:
            if self.owner.iscrazy:
                Fire(self,x,y,i,self.firelive,self.rand(self.owner.firepower*2,int(self.owner.firepower*2*0.5)),self.speed)
            else:
                Fire(self,x,y,i,self.firelive,self.rand(self.owner.firepower*2,int(self.owner.firepower*0.5)),self.speed)
        self.starcenter=(self.rect.centerx+self.star_r*math.cos(self.radangle),self.rect.centery+self.star_r*math.sin(self.radangle))
        self.starimage= pygame.transform.rotate(self.originalstar, -self.angle)
        self.starrect=self.starimage.get_rect(center=self.starcenter)
        screen.blit(self.starimage,self.starrect)
class Fire(Bullet):
    def __init__(self,owner,x,y,angle,live,power,speed):
        self.image=random.choice(self.images)
        super(Fire,self).__init__(owner,x,y,angle,live,power,speed)
    def explode(self):
        self.power=0

class Magnum(Gun):
    MINTIME=200
    MINSPEED=80
    def __init__(self,owner,drict_pos):
        super(Magnum,self).__init__(owner,drict_pos)
        self.maxtime=400
        self.blspeed=40
        self.ispre=False
        self.r=50
    def shoot(self):
        self.radangle=self.angle*math.pi/180
        x=self.rect.centerx+self.r*math.cos(self.radangle)
        y=self.rect.centery+self.r*math.sin(self.radangle)
        Bomb(self,x,y,self.angle,500,self.rand(self.owner.bombpower,int(self.owner.bombpower*0.5)),self.blspeed)
        self.time=0
class Bomb(Bullet):
    def __init__(self,owner,x,y,angle,live,power,speed):
        super(Bomb,self).__init__(owner,x,y,angle,live,power,speed)

    def explode(self):
        bigExplosion(self)
        self.kill()
    def dirt(self):
        smallDirt(self)

class Meltgun(Gun):
    MINTIME=6
    MINSPEED=40
    angle0 = 8
    def __init__(self,owner,drict_pos):
        super(Meltgun,self).__init__(owner,drict_pos)
        self.ispre=False
        #self.average=sle.power
        if self.owner.isen:
            self.maxtime=self.owner.maxshootime
        else:
            self.maxtime=15
        self.r=51
        self.bllive=100
        self.turn=1
        self.blspeed=18
    def shoot(self):
        if self.turn==1:
            self.turn=2
            self.angle1=self.angle+self.angle0
        else:
            self.turn=1
            self.angle1=self.angle-self.angle0
        self.radangle0=self.angle1*math.pi/180

        x=self.rect.centerx+self.r*math.cos(self.radangle0)
        y=self.rect.centery+self.r*math.sin(self.radangle0)
        if self.owner.isen:
            enShortlight(self,x,y,self.angle,self.bllive,self.rand(enShortlight.enpower,int(enShortlight.enpower*0.5)),self.blspeed)
        else:
            Shortlight(self,x,y,self.angle,self.bllive,self.rand(self.owner.shortltpor,int(self.owner.shortltpor*0.5)),self.blspeed)
        self.time=0
        game.shoot_sound.play()
class Shortlight(Bullet):
    def __init__(self,owner,x,y,angle,live,power,speed):
        self.image=random.choice(self.images)
        super(Shortlight,self).__init__(owner,x,y,angle,live,power,speed)

    def explode(self):
        self.distory()
        self.kill()
class enShortlight(Shortlight):
    enpower=5
    def __init__(self,owner,x,y,angle,live,power,speed):
        super(enShortlight,self).__init__(owner,x,y,angle,live,power,speed)
        self.power=self.enpower
        self.speed=10

class Railgun(Gun):
    MINTIME=120
    MINSPEED=60
    def __init__(self,owner,drict_pos):
        super(Railgun,self).__init__(owner,drict_pos)
        self.maxtime=300
        self.ispre=False
        self.starlist=[]
        self.r=10
        self.stime=20
        self.speed=64
        if self.owner.isen==True:
            self.maxpre_time=self.maxtime*0.35
        else:
            self.maxpre_time=self.maxtime*0.15
    def showstar(self):
        self.star_center=(self.rect.centerx+self.star_r*math.cos(self.angle*math.pi/180),self.rect.centery+self.star_r*math.sin(self.angle*math.pi/180))
        self.star_rect=self.star.get_rect(center=self.star_center)
        #self.star=pygame.transform.scale(load_image('gunstar2.png'),(self.starscale,self.starscale))
        screen.blit(self.star,self.star_rect)
    def chk_shoot(self):
        if self.owner.isen==True:
            self.maxpre_time=self.maxtime*0.35
        else:
            self.maxpre_time=self.maxtime*0.15
        if self.ispre:
            if self.pre_time<self.maxpre_time:
                self.pre_time+=1
            else:
                self.realshoot()


        #self.prepare()
    def realshoot(self):
        self.time=0
        game.litsound.play()
        self.radangle=self.angle*math.pi/180
        x=self.rect.centerx+self.r*math.cos(self.radangle)
        y=self.rect.centery+self.r*math.sin(self.radangle)
        if type(self.owner)==Enemytank1:
            enLight(self,x,y,self.angle,500,enLight.enpower,self.speed)
        else:
            Light(self,x,y,self.angle,500,self.owner.ltpor,self.speed)
        self.ispre=False
    def shoot(self):
        if self.owner.iscrazy:
            self.realshoot()
        else:
            game.chargesnd.play()
            self.pre_time=0
            self.ispre=True
            self.star=Star(self)
class Light(Bullet):
    lightspeed=60
    def __init__(self,owner,x,y,angle,live,power,speed):
        self.image=random.choice(self.images)
        super(Light,self).__init__(owner,x,y,angle,live,power,speed)
        self.target=None
        self.speed=self.lightspeed
        self.power1=self.owner.rand(power,int(power*0.5))
        self.power=0
    def explode(self):
        self.list=pygame.sprite.spritecollide(self,game.enemies,False)
        for i in self.list:
            if i.lightmark!=self:
                i.lightmark=self
                i.hurt(self.power1)


    def dirt(self):
        lightDirt(self,self.rect.centerx,self.rect.centery)
        self.oldcenter=self.rect.center
        self.rect.move_ip(30*math.cos(self.radangle),30*math.sin(self.radangle))
        lightDirt(self,self.rect.centerx,self.rect.centery)
        self.rect=self.image.get_rect(center=self.oldcenter)
class enLight(Light):
    enpower=30
    def __init__(self,owner,x,y,angle,live,power,speed):
        super(enLight,self).__init__(owner,x,y,angle,live,power,speed)
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.power=self.enpower
    def explode(self):
        self.power=0
class lightDirt(Dirt):
    def __init__(self,owner,x,y):
        super(lightDirt,self).__init__(owner)
        self.owner=owner
        self.life=60
        self.image=self.owner.image
        self.angle=self.owner.angle
        self.live=self.owner.owner.maxtime/2
        self.rect=self.image.get_rect(center=(x,y))
class Star(pygame.sprite.Sprite):
    def __init__(self,owner):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.owner=owner
        self.live=self.owner.maxpre_time
        self.star_r=45
        self.image=self.images[1]
        self.center=(self.owner.rect.centerx+self.star_r*math.cos(self.owner.angle*math.pi/180),self.owner.rect.centery+self.star_r*math.sin(self.owner.angle*math.pi/180))
        self.rect=self.image.get_rect(center=self.center)
    def sub(self):
        self.live-=1
        if self.live<0:
            self.kill()
    def update(self):
        self.sub()
        self.center=(self.owner.rect.centerx+self.star_r*math.cos(self.owner.angle*math.pi/180),self.owner.rect.centery+self.star_r*math.sin(self.owner.angle*math.pi/180))
        self.rect=self.image.get_rect(center=self.center)
        self.starindex=self.owner.pre_time//4
        self.image=self.images[self.starindex]
        screen.blit(self.image,self.rect)
'''
class Cross(Gun):
    MINTIME=120
    MINSPEED=40
    def __init__(self,owner,drict_pos):
        super(Cross,self).__init__(owner,drict_pos)
'''
class Explosion(pygame.sprite.Sprite):
    play=True
    animcycle = 2
    isdirt=True
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #pygame.sprite.Sprite.__init__(self, self.containers),,pygame.transform.scale(load_image('fire1.png'),(90,90))
        self.image = self.images[0]
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life = 0
        self.maxindx=4
        self.maxliv=30
        if self.play:
            self.sound.play()
    def cheek(self):
        pass
    def update(self):
        self.cheek()
        self.life = self.life + 1
        self.index=self.life//self.animcycle
        if self.index>=self.maxindx:
            self.index=self.maxindx
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.actor.rect.center)

        screen.blit(self.image,self.rect)
        if self.life >= self.maxliv:
            if self.isdirt:
                Dirt(self.actor)
            self.kill()
class bullteExplosion(Explosion):
    defaultlife = 12
    animcycle = 3
    images = []
    play=False
    def __init__(self, actor):
        super(bullteExplosion,self).__init__(actor)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife
    def update(self):
        self.life = self.life - 1
        self.image = self.images[self.life//self.animcycle%2]
        screen.blit(self.image,self.rect)
        if self.life <= 0: self.kill()
class bigExplosion(Explosion):
    play=True
    isdirt = False
    def __init__(self, actor):
        super(bigExplosion,self).__init__(actor)
        self.maxindx=7
        self.maxliv=12
        self.txtlist=['GOOD!!','Well done!!','Super killer!']
        self.power1=player.bombpower
    def cheek(self):
        self.list=pygame.sprite.spritecollide(self,game.enemies,False)
        for one in self.list:
            if one.expmark!=self:
                one.expmark=self
                one.hurt(self.power1)
class Eexplosion(Explosion):
    play=True
    isdirt=False
    def __init__(self, actor):
        super(Eexplosion,self).__init__(actor)

class smallDirt(Dirt):
    def __init__(self,owner):
        super(smallDirt,self).__init__(owner)
        self.owner=owner
        self.life =60
        self.rect=self.image.get_rect(center=self.owner.rect.center)

class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed=6
        self.level=0
        self.maxlive=100
        self.rotspeed=5
        self.rect = self.image.get_rect()
        self.isen=False
        self.rotate = False
        self.goldtime=0
        self.defendtime=0
        self.subnum=1
        self.temprynum=0
        self.crazyeg=0
        self.iscrazy=False
        self.oldscore=0
        self.shortltpor=20
        self.ltpor=500
        self.bombpower=300
        self.still=0
    def move(self):
        pass
    def update(self):
        pass
class Enemy(Tank):
    maxshootime=160
    def __init__(self):
        super(Enemy,self).__init__()
        self.isen=True
        self.rect.x=random.randint(0,1200)
        self.rect.y=random.randint(0,700)
        self.lightmark=None
        self.expmark=None
        self.still=0
        self.shootime=0
    def addlive(self,liv1):
        liv1=int(liv1)
        self.live+=liv1
        Text(liv1,(0,255,0),20,self.rect.center)
    def display(self):
        screen.blit(self.image,self.rect)

    def distory(self,a,b,c,d):
        game.score+=a
        game.energy+=c
        player.addlive(d)
        Explosion(self)
        game.iskill()
        self.kill()
    def shoot(self):
        pass
    def shock(self,t):
        self.still=t
    def cheek(self):
        if self.still>0:
            self.still-=1
        else:
            self.move()
    def update(self):
        if not self.still>0:
            if self.maxshootime<=60:
                self.maxshootime=60
            if self.shootime<self.maxshootime:
                self.shootime+=1
            elif len(game.enBulletgroup)<100 and not pygame.sprite.collide_rect(self,player):
                self.shoot()
                self.shootime=0
        self.cheek()
        self.display()
class Enemy0(Enemy):
    maxshootime=200
    maxlive=100
    def __init__(self):
        self.live=self.maxlive
        self.enname=random.randint(0,3)
        self.anglelist=[0,90,180,270]
        self.angle=self.anglelist[self.enname]
        self.image=self.images[self.enname]
        super(Enemy0,self).__init__()

        self.iplist=[(1,0),(0,1),(-1,0),(0,-1)]
    def move(self):
        self.enip=self.iplist[self.enname]
        self.rect.move_ip(self.enip[0],self.enip[1])
        if self.rect.x <0:
            self.kill()
        elif self.rect.x+60 > 1200:
            self.kill()
        if self.rect.y < 0:
            self.kill()
        elif self.rect.y+60 > 700:
            self.kill()
    def hurt(self,power):
        if power>0:
            self.live-=power
            if self.live<=0:
                Damage(self,int(power))
                if player.iscrazy:
                    self.distory(1,1,0,2)
                else:
                    self.distory(1,1,2,2)
            else:
                Damage(self,int(power))
    def shoot(self):
        BulletCoordinate(self,self.rect.centerx,self.rect.centery,self.angle,50,10,15)
class BulletCoordinate(Bullet):
    realpower=10
    def __init__(self,owner,x,y,angle,live,power,speed):
        self.power=self.realpower
        super(BulletCoordinate,self).__init__(owner,x,y,angle,live,power,speed)
        self.power=self.realpower
    def explode(self):
        self.kill()
class Enemy1(Enemy0):
    maxshootime=300
    maxlive=150
    def __init__(self):
        self.live=self.maxlive
        super(Enemy1,self).__init__()

    def shoot(self):
         for i in self.anglelist:
            BulletCoordinate(self,self.rect.centerx,self.rect.centery,i,80,10,10)
class crazyEnemy(Enemy0):
    maxshootime=60
    maxlive=60
    def __init__(self):
        self.live=self.maxlive
        super(crazyEnemy,self).__init__()
        self.anglelist=[i for i in range(0,360,30)]
    def shoot(self):
         for i in self.anglelist:
            BulletCoordinate(self,self.rect.centerx,self.rect.centery,i,80,10,10)
class Enemytank0(Enemy):
    maxshootime=40
    maxlive=100
    def __init__(self):
        self.live=self.maxlive
        super(Enemytank0,self).__init__()
        self.angle=random.randint(0,360)
        self.speed=4
        self.rotate = False
        self.rotspeed=1
        self.gun=Meltgun(self,player.rect.center)
        self.shortltpor=5
        self.turntime=0
        self.iscrazy=False
    def rotateit(self,ang):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            self.angle+=ang
            self.angle=self.angle%360
            self.center = self.rect.center
            self.image = pygame.transform.rotate(self.original, -self.angle)
            self.rect = self.image.get_rect(center=self.center)
    def hurt(self,power):
        if power>0:
            self.live-=power
            if self.live <= 0:
                if player.iscrazy:
                    self.distory(1,1,0,2)
                else:
                    self.distory(1,1,1,2)
            Damage(self, int(power))
    def moveL(self):
        self.rotateit(-2)
    def moveR(self):
        self.rotateit(2)
    def moveU(self):
        self.rect.move_ip(self.x_speed,self.y_speed)
    def moveD(self):
        self.rect.move_ip(-self.x_speed,-self.y_speed)
    def turn(self):
        if self.turntime<40:
            self.turntime+=1
            if random.choice([True,False]):
                self.moveL()
        elif self.turntime>=40 and self.turntime<80:
            self.turntime+=1
            if random.choice([True,False]):
                self.moveR()
        else:
            self.turntime=0
    def move(self):
        self.radangle = self.angle * math.pi / 180
        self.x_speed = self.speed * math.cos(self.radangle)
        self.y_speed = self.speed * math.sin(self.radangle)
        if random.choice([True,False]):
            self.moveU()
        self.turn()
        if self.rect.left <=0:
            self.rect.left=0
            self.rotateit(90)
            self.moveU()
        elif self.rect.right >= 1200:
            self.rect.right = 1200
            self.rotateit(90)
            self.moveU()
        if self.rect.top <= 0:
            self.rect.top = 0
            self.rotateit(90)
            self.moveU()
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.rotateit(90)
            self.moveU()
    def shoot(self):
        self.gun.shoot()
    def update(self):
        self.cheek()
        self.display()
        if not self.still>0:
            if self.gun.time>=self.gun.maxtime and (not self.gun.ispre):
                self.gun.shoot()
            self.move()
            self.gun.encold()
        self.gun.update(player.rect.center,self.rect.center)
class Enemytank1(Enemytank0):
    maxshootime=200
    maxlive=180
    def __init__(self):
        self.live=self.maxlive
        super(Enemytank1,self).__init__()

        self.gun=Railgun(self,player.rect.center)
        self.gun.maxtime=150
        self.isen=True
        self.ltpor=15
class Boss(Enemytank0):
    maxshootime=30
    maxlive=1000
    def __init__(self):
        self.live=self.maxlive
        super(Boss,self).__init__()

        self.speed=3
        self.gunr=20
        self.angle0=30
        self.call()
        self.cure()
        self.guns=[Meltgun(self,player.rect.center),Meltgun(self,player.rect.center),Meltgun(self,player.rect.center),Meltgun(self,player.rect.center)]
    def shoot(self):
        for g in self.guns:
            g.shoot()
    def call(self):
        game.addenemy()
        game.addenemy()
    def cure(self):
        for e in game.enemies:
           e.addlive(e.live)
    def showlive(self):
        if game.live>0:
            textfont=pygame.font.SysFont('arial',30)
            self.text=textfont.render('Live:'+str(int(self.live)),True,(255,0,0))
            self.textrect=self.text.get_rect(center=(self.rect.centerx,self.rect.centery-120))
            screen.blit(self.text,self.textrect)
    def update(self):
        self.cheek()
        self.display()
        self.showlive()
        if not self.still>0:
            if self.guns[0].time>=self.guns[0].maxtime and (not self.guns[0].ispre):
                self.shoot()
        self.gunanglelist=[self.angle+self.angle0,
                           self.angle-self.angle0,
                           self.angle+self.angle0+180,
                           self.angle-self.angle0+180]
        for i in range(4):
            self.guns[i].update(player.rect.center,
                                (self.rect.centerx+self.gunr*math.cos(self.gunanglelist[i]*math.pi/180),
                                 self.rect.centery+self.gunr*math.sin(self.gunanglelist[i]*math.pi/180)))

            self.guns[i].encold()
    def hurt(self,power):
        self.live-=power
        if self.live<=0:
            Damage(self,int(power))
            self.distory(10,1,2,2)
            game.winsound.play()
        else:
            Damage(self,int(power))
class crazyBoss(Boss):
    maxshootime=40
    maxlive=1200
    def __init__(self):
        self.live=self.maxlive
        super(crazyBoss,self).__init__()
        self.anglelist=[i for i in range(0,360,20)]
    def shoot(self):
         for i in self.anglelist:
            BulletCoordinate(self,self.rect.centerx,self.rect.centery,i,80,10,15)
    def update(self):
        self.cheek()
        self.display()
        self.showlive()
        if not self.still>0:
            if self.maxshootime<=60:
                self.maxshootime=60
            if self.shootime<self.maxshootime:
                self.shootime+=1
            elif len(game.enBulletgroup)<120 and not pygame.sprite.collide_rect(self,player):
                self.shoot()
                self.shootime=0


class Player(Tank):
    def __init__(self):
        self.num=3
        self.image = self.images[self.num]
        super(Player,self).__init__()
        self.gunnum=1
        self.firepower=1
        self.birdpower=1
        self.angle=0
        self.railgun=Railgun(self,pygame.mouse.get_pos())
        self.meltgun=Meltgun(self,pygame.mouse.get_pos())
        self.magnum=Magnum(self,pygame.mouse.get_pos())
        self.firegun=Firegun(self,pygame.mouse.get_pos())
        self.gauss=Gauss(self,pygame.mouse.get_pos())
        self.misslegun=Misslegun(self,pygame.mouse.get_pos())
        self.gunlist=[self.misslegun,self.meltgun,self.railgun,self.firegun,self.gauss]
        self.gun=self.gunlist[self.gunnum]
    def rotateit(self,ang):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            self.angle+=ang
            self.angle=self.angle%360
            self.center = self.rect.center
            self.image = pygame.transform.rotate(self.original,-self.angle)
            self.rect = self.image.get_rect(center=self.center)
    def move(self):

        self.radangle = self.angle * math.pi/180
        self.x_speed = self.speed * math.cos(self.radangle)
        self.y_speed = self.speed * math.sin(self.radangle)
        if game.pressed_keys[K_UP] or game.pressed_keys[K_w]:
            self.rect.move_ip(self.x_speed,self.y_speed)
        if game.pressed_keys[K_DOWN] or game.pressed_keys[K_s]:
            self.rect.move_ip(-self.x_speed,-self.y_speed)
        if game.pressed_keys[K_LEFT] or game.pressed_keys[K_a]:
            self.rotateit(-2)
        if game.pressed_keys[K_RIGHT] or game.pressed_keys[K_d]:
            self.rotateit(2)
        if self.rect.left <=0:
            self.rect.left = 0
        elif self.rect.right >= 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
    def move0(self):
        if game.pressed_keys[K_UP] or game.pressed_keys[K_w]:
            self.num=0
            self.center=self.rect.center
            self.image = self.images[self.num]
            self.rect = self.image.get_rect(center=self.center)
            self.rect.move_ip(0,-5)
        if game.pressed_keys[K_DOWN] or game.pressed_keys[K_s]:
            self.num=1
            self.center=self.rect.center
            self.image = self.images[self.num]
            self.rect = self.image.get_rect(center=self.center)
            self.rect.move_ip(0,5)
        if game.pressed_keys[K_LEFT] or game.pressed_keys[K_a]:
            self.num=2
            self.center=self.rect.center
            self.image = self.images[self.num]
            self.rect = self.image.get_rect(center=self.center)
            self.rect.move_ip(-5,0)
        if game.pressed_keys[K_RIGHT] or game.pressed_keys[K_d]:
            self.num=3
            self.center=self.rect.center
            self.image = self.images[self.num]
            self.rect = self.image.get_rect(center=self.center)
            self.rect.move_ip(5,0)
        if self.rect.left <=0:
            self.rect.left = 0
        elif self.rect.right >= 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
    def showlive(self):
        if game.live>0:
            self.rate=game.live/self.maxlive
            self.B=int(255*self.rate)
            self.R=255-self.B
            textfont=pygame.font.SysFont('arial',30)
            self.text=textfont.render('Live:'+str(game.live),True,(self.R,0,self.B))
            self.textrect=self.text.get_rect(center=(self.rect.centerx,self.rect.centery-70))
            screen.blit(self.text,self.textrect)
    def update(self):
        self.move()
        self.cheek()
        self.display()
        self.showlive()
        self.gun.update(pygame.mouse.get_pos(),self.rect.center)
        for gun1 in self.gunlist:
            gun1.encold()
    def ifgrow(self):
        self.addscore=game.score-self.oldscore
        if self.addscore>=10:
            for i in range(self.addscore//10):
                self.level+=1
                Text('LEVEL UP!',(0,255,0),33,self.rect.center)
                self.oldscore=game.score
                self.maxlive+=5
                self.shortltpor+=1
                self.firepower=self.firepower*1.08
                self.ltpor=self.ltpor*1.04
                self.bombpower=self.bombpower*1.06
                self.birdpower+=0.1
                self.addlive(30)
                for guni in self.gunlist:
                    guni.maxtime=guni.maxtime*0.95
                    guni.blspeed=guni.blspeed*1.05
                '''    
                if not self.iscrazy:
                    self.gun.old_maxtime=self.gun.maxtime
                    self.gun.oldblspeed=self.gun.blspeed
                '''
    def changegun(self,n):
            '''
            #if game.pressed_keys[K_q]:                
            if self.gunnum<2:
                self.gunnum+=1
            else:
                =0
            '''
            game.changesound.play()
            if self.gunnum==n:
                self.gunnum=1
                self.gun=self.gunlist[self.gunnum]
            else:
                self.gunnum=n
                self.gun=self.gunlist[self.gunnum]
            self.gun.update(pygame.mouse.get_pos(),self.rect.center)
    def addlive(self,liv1):
        liv1=int(liv1)
        game.live+=liv1

        if game.live>self.maxlive:
            game.live=self.maxlive
        else:
             Text(liv1,(0,255,0),30,self.rect.center)
    def defend(self):
        self.isdefend=True
        self.subnum=self.subnum*0.5
        self.defendtime=600
        game.energy-=10
    def elcshock(self):
        game.energy-=10
        self.pos1 = vect(self.rect.centerx, self.rect.centery)
        Eexplosion(self)
        for e in game.enemies:
            pos2=vect(e.rect.centerx, e.rect.centery)
            vec=pos2-self.pos1
            length=vec.length()
            #e.hurt(self.power)
            e.shock(600)
            if length>1:
                angle = vect(0,0).angle_to(vec)
                #print(angle)
                Electric(self,((self.rect.centerx+e.rect.centerx)/2,(self.rect.centery+e.rect.centery)/2),
                             length,angle)
    def repair(self):
        self.addlive(self.maxlive-game.live)
    def cheek(self):
        #if game.pressed_keys[K_f] and (game.energy>=10) and self.isdefend==False:
            #self.defend()
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
        self.ifgrow()
        if not self.iscrazy:

            if (self.railgun.time<self.railgun.maxtime) and self.gunnum==2:
                self.gunnum=1
                self.gun=self.gunlist[self.gunnum]
            if (self.gauss.time<self.gauss.maxtime) and self.gunnum==4:
                self.gunnum=1
                self.gun=self.gunlist[self.gunnum]
        else:
            for i in range(10):
                self.gun.encold()
                if self.gun.star is not None:
                   self.gun.star.sub()
        #self.if_changegun()
    def hurt(self,power):

        self.power=int(power)
        game.live-=self.power*self.subnum
        Damage(self,int(power))
    def distory(self):

        if game.live<=0:
            self.kill()
            game.running=False
    def crazy(self):
        '''
        self.gun.blspeed=self.gun.blspeed*2  
        self.gun.maxtime=self.gun.maxtime*0.2
        '''
        #self.railgun.maxpre_time=0 self.railgun.maxpre_time*0.2
        self.crazyeg+=360
        self.iscrazy=True
        game.energy-=20
        self.repair()
    def display(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        if self.isdefend:
            self.rect1=self.dfnimg.get_rect(center=self.rect.center)
            screen.blit(self.dfnimg,self.rect1)
        if self.iscrazy:
            self.starrect=self.star.get_rect(center=self.rect.center)
            screen.blit(self.star,self.starrect)


class Text(pygame.sprite.Sprite):
    live=90
    name='SimHei'
    def __init__(self,num,color,size,center):
        pygame.sprite.Sprite.__init__(self, self.containers)
        textfont=pygame.font.SysFont(self.name,size) #创建文本对象，大小30
        self.image=textfont.render(str(num),True,color)
        self.rect = self.image.get_rect(center=center)
    def change(self):
        pass
    def update(self):
        self.rect.move_ip(0,-2)
        self.change()
        screen.blit(self.image,self.rect)
        if self.live>0:
            self.live-=1
        else:
            self.kill()
class Damage(Text):
    live=60
    name='arial'
    def __init__(self,owner,num):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #super(Damage,self).__init__(owner,num)
        self.index=0
        maxmsize=80
        self.msize=maxmsize*num/owner.maxlive
        if self.msize >maxmsize:
            self.msize=maxmsize
        elif self.msize<maxmsize*0.4:
            self.msize=maxmsize*0.4
        rate=self.msize/maxmsize
        r=random.randint(0,255)
        b=random.randint(0,255)
        g=random.randint(0,255)
        self.fontlist = [pygame.font.SysFont(self.name, i).render(str(num),True,(r,g,b))
                        for i in range(int(self.msize),int(self.msize*0.3),-1)]
        self.image = self.fontlist[self.index]
        self.rect = self.image.get_rect(center=owner.rect.center)
    def change(self):
        if self.live%3==0:self.index+=1
        if self.index>=len(self.fontlist)-1:self.index=len(self.fontlist)-1
        self.image=self.fontlist[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)



#pygame.mixer.init()

if hasattr(sys,'_MEIPASS'):
# PyInstaller会创建临时文件夹temp
# 并把路径存储在_MEIPASS中sys._MEIPASS
    main_dir = os.path.dirname(os.path.realpath(sys.executable))
else:
    main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file):
    """ because pygame can be be compiled without mixer.
    """
    if not pygame.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print("Warning, unable to load, %s" % file)
    return None
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
    Explosion.images = [pygame.transform.scale(img,(i,i)) for i in [15,45,75,90,120]]
    Explosion.sound=load_sound("boom.wav")
    bigExplosion.images = [pygame.transform.scale(img,(i,i)) for i in [50,90,120,150,180,210,240,270]]
    bigExplosion.sound=load_sound("boom.wav")
    Eexplosion.images = [pygame.transform.scale(load_image('electric.png'),(i,i)) for i in [50,90,120,150,180,210,240,270]]
    Eexplosion.sound=load_sound("electric.wav")
    img=pygame.transform.scale(load_image('explosion.png'),(20,20))
    bullteExplosion.images = [img, pygame.transform.flip(img, 1, 0)]
    #Missle.images=[pygame.transform.scale(load_image('bigmissle.png'),(60,20)),pygame.transform.scale(load_image('dronemissle.png'),(40,15))]
    img=pygame.transform.smoothscale(load_image('ground1.png'),(60,80))
    Player.images=[pygame.transform.rotate(img,i) for i in [0,180,90,270]]
    BulletCoordinate.image=pygame.transform.smoothscale(load_image('missle1.png'),(40,20))
    Player.star=pygame.transform.smoothscale(load_image('star2.png'),(60,60))
    Player.dfnimg=pygame.transform.smoothscale(load_image('defendimg.png'),(120,120))
    enemyimage0=pygame.transform.smoothscale(load_image('enemy0.png'),(80,60))
    enemyimage1=pygame.transform.smoothscale(load_image('enemy1.png'),(100,75))
    crazyenimg=pygame.transform.smoothscale(load_image('enemycrazy.png'),(100,75))
    Enemy0.images=[pygame.transform.rotate(enemyimage0,-i) for i in [0,90,180,270]]
    crazyEnemy.images=[pygame.transform.rotate(crazyenimg,-i) for i in [0,90,180,270]]
    Enemytank0.image=pygame.transform.smoothscale(load_image('ground2.png'),(80,60))
    Enemytank1.image=pygame.transform.smoothscale(load_image('ground2.png'),(80,60))
    Enemy1.images=[pygame.transform.rotate(enemyimage1,-i) for i in [0,90,180,270]]
    Boss.image=pygame.transform.smoothscale(load_image('ground2.png'),(120,90))
    crazyBoss.image=pygame.transform.smoothscale(load_image('enemycrazy.png'),(120,90))
    Railgun.image=pygame.transform.smoothscale(load_image('gun.png'),(100,30))
    Railgun.star=load_image('gunstar1.png')
    Meltgun.image=pygame.transform.smoothscale(load_image('gun2.png'),(100,40))
    Magnum.image=pygame.transform.smoothscale(load_image('magnum.png'),(130,40))
    Firegun.images=[pygame.transform.smoothscale(load_image('firegun.png'),(130,40)),
                    pygame.transform.smoothscale(load_image('firebase.png'),(120,25))]
    Misslegun.image=pygame.transform.smoothscale(load_image('misslegun.png'),(150,90))
    Fire.images=[pygame.transform.smoothscale(load_image('fire'+str(i)+'.png'),(12,12)) for i in range(5)]
    Gauss.image=pygame.transform.smoothscale(load_image('birdgun1.png'),(130,50))
    birdDirt.image=pygame.transform.smoothscale(load_image('Ebombdirt.png'),(40,8))
    Star.images=[]
    for scale in range(1,42,2):
        Star.images.append(pygame.transform.scale(load_image('gunstar1.png'),(scale,scale)))
    Dirt.image=pygame.transform.smoothscale(load_image('BlastMark.png'),(100,100))
    smallDirt.image=pygame.transform.smoothscale(load_image('defendimg.png'),(20,20))
    #lightDirt.image=pygame.transform.smoothscale(load_image('lit.png'),(32,15))
    Light.images=[pygame.transform.smoothscale(load_image('lit.png'),(32,15)),pygame.transform.smoothscale(load_image('lit1.png'),(30,15))]
    enLight.images=[pygame.transform.smoothscale(load_image('lit2.png'),(32,15))]
    Shortlight.images=[]
    for i in range(1,5):
        Shortlight.images.append(pygame.transform.scale(load_image('shortlight'+str(i)+'.png'),(32,10)))
    enShortlight.images=[pygame.transform.smoothscale(load_image('shortlight1.png'),(30,10))]
    Bomb.image=pygame.transform.smoothscale(load_image('dronemissle.png'),(40,15))
    Ebomb.image=pygame.transform.smoothscale(load_image('Ebomb.png'),(40,15))
    Missle.image = pygame.transform.smoothscale(load_image('dronemissle.png'), (40, 15))
    Electric.originalimages=[load_image('electric'+str(i)+'.png') for i in range(3)]
    img=pygame.transform.scale(load_image('wing0.png'),(130,50))
    Wing.images = [img, pygame.transform.flip(img,0,1)]
    Game.winsound=load_sound("win_boss.wav")
    Game.changesound=load_sound("mine.wav")
    Game.shoot_sound = load_sound("car_door.wav")
    Game.shoot_sound.set_volume(0.7)
    Game.missle_sound= load_sound("misslesound.mp3")
    Game.litsound=load_sound("shortlight.wav")
    Game.litsound.set_volume(1.5)
    Game.chargesnd=load_sound("charge.wav")
    Game.chargesnd.set_volume(2)
    Game.killsounds=[load_sound(str(i)+".mp3") for i in range(2,6)]
    for i in Game.killsounds:
        i.set_volume(8)
    #Game.chargesnd.set_volume(5)
def cheekp():

        get_dic=pygame.sprite.groupcollide(game.enemies,game.Bulletgroup,False,False)
        lost_list=pygame.sprite.spritecollide(player,game.enBulletgroup,False)
        dic2=pygame.sprite.groupcollide(game.enBulletgroup,game.birdgroup,True,False)
        for b in dic2:
            b.distory()
        for one_en in get_dic:
            power=0
            if get_dic[one_en] is not None:
                for one_bl in get_dic[one_en]:
                    power+=one_bl.power
                    one_bl.explode()

                one_en.hurt(power)
                get_dic[one_en]=None

        if player.goldbody is not True:
            for one2 in lost_list:
                player.hurt(one2.power)
                one2.explode()
                player.distory()
        else:
            dist_list=pygame.sprite.spritecollide(player,game.enemies,False)
            for one3 in dist_list:
                one3.distory(1,0,1,0)

def showscore():

    textfont=pygame.font.SysFont('SimHei',30) #创建文本对象，大小30
    t1=textfont.render('得分:'+str(game.score)
                       +' 等级:'+str(player.level)
                       +' 武器能量:'+str(int(player.gun.time))
                       +' 坦克能量:'+str(game.energy),True,(255,0,0))
    t2=textfont.render('按SHFIT开启大招(20能量)!!!',True,(128,0,255))#生成平滑的红色字符串
    t3=textfont.render('按F开启双倍防护(10能量)!!!',True,(128,0,255))
    t4=textfont.render('防护：'+str(int(math.log(player.subnum,0.5)))+'级',True,(230,120,16))
    trailgun=textfont.render('激光炮已就位！',True,(0,255,0))
    tmugnum=textfont.render('天蝎已就位!',True,(0,255,0))
    twinggun=textfont.render('电磁炮已就位!',True,(0,255,0))
    screen.blit(t1,[50,20]) #在窗口显示
    screen.blit(t4,[500,45])
    if game.energy>=20:
        screen.blit(t2,[50,70])
    if game.energy>=10:
        screen.blit(t3,[50,45])

    if player.railgun.time>=player.railgun.maxtime:
        screen.blit(trailgun,[800,20])
    if player.misslegun.time>=player.misslegun.maxtime:
        screen.blit(tmugnum,[800,45])
    if player.gauss.time>=player.gauss.maxtime:
        screen.blit(twinggun,[800,70])

class Game():
    allsp = pygame.sprite.RenderUpdates()#pygame.sprite.Group()
    score=0
    time=0
    live=100
    energy=40
    RUN=True
    running = 'r'
    pressed_keys = None
    pressed_mouse =None
    allEnemy=[Enemy0,Enemy1,Enemytank0,Enemytank1,crazyEnemy]
    Bosses=[Boss,crazyBoss]
    enemies = pygame.sprite.Group()
    tanks=pygame.sprite.Group()
    grounds=pygame.sprite.Group()
    Bulletgroup=pygame.sprite.Group()
    playerlist=pygame.sprite.Group()
    enBulletgroup=pygame.sprite.Group()
    birdgroup=pygame.sprite.Group()
    Player.containers = allsp,playerlist,tanks

    Text.containers = allsp
    Enemy.containers = enemies,allsp,tanks
    BulletCoordinate.containers = enBulletgroup,allsp
    Light.containers = allsp,Bulletgroup
    enLight.containers = allsp,enBulletgroup
    Star.containers = allsp
    Bomb.containers = Bulletgroup,allsp
    Ebomb.containers = Bulletgroup,allsp
    Missle.containers = Bulletgroup,allsp
    birdDirt.containers = allsp
    maxenum=10
    Explosion.containers = allsp
    Shortlight.containers = Bulletgroup,allsp
    Fire.containers = allsp,Bulletgroup
    enShortlight.containers = enBulletgroup,allsp
    Dirt.containers = grounds
    smallDirt.containers = allsp
    lightDirt.containers = allsp
    oldaddtime=0
    oldaddbosstime=0
    addentime=200
    oldfasttime=0
    getfastime=450
    bosstime=2600
    kill_n=0
    kill_t=0
    #Bombgroup=pygame.sprite.Group()
    #Toolsgroup=pygame.sprite.Group()
    texts=['Double Kill','Triple Kill','Quadra Kill','Penta Kill']
    #elcsound=load_sound("electric.wav")
    def update(self):
        self.checkkill()
        self.time+=1
        self.addtime=self.time//self.addentime-self.oldaddtime
        if self.addtime>0:
            self.oldaddtime=self.time//self.addentime
            for i in range(self.addtime):
                if len(self.enemies)<self.maxenum:
                    self.addenemy()
        self.addbosstime=self.time//self.bosstime-self.oldaddbosstime
        if self.addbosstime>0:
            self.oldaddbosstime=self.time//self.bosstime
            self.addboss()
        self.addtime1=self.time//self.getfastime-self.oldfasttime
        if self.addtime1>0:
            self.oldfasttime=self.time//self.getfastime
            for i in range(self.addtime1):
                self.addentime-=2
                self.addbosstime-=3
                enLight.enpower+=1
                enShortlight.enpower+=0.1
                BulletCoordinate.realpower+=0.3
                for e in self.allEnemy:
                    e.maxlive=e.maxlive*1.06
                    e.maxshootime=e.maxshootime*0.95
                    if e.maxshootime<10:
                        e.maxshootime=10
                for e in self.Bosses:
                    e.maxlive=e.maxlive*1.05
                    e.maxshootime=e.maxshootime*0.95
                    if e.maxshootime<5:
                        e.maxshootime=5
        if self.addentime<=60:
                self.addentime=60
        if self.addbosstime<=300:
                self.addbosstime=300
        if self.time>=5000:
            self.time=0
            self.oldaddtime=0
            self.oldfasttime=0
            self.oldaddbosstime=0
    def addenemy(self):
        enemy=random.choice(self.allEnemy)
        enemy()
    def addboss(self):
        e=random.choice(self.Bosses)
        e()
    def iskill(self):
        #if self.kill_n==0:
        self.kill_t=1
        self.kill_n+=1
        #print("iskill")
    def numberkill(self,n):
        if n<=5 and n>=2:
            self.killsounds[n-2].play()
            Text(self.texts[n-2],(128,0,255),50,(650,250))
        elif n>5:
            self.killsounds[3].play()
            Text(self.texts[3],(128,0,255),50,(650,250))
    def checkkill(self):
        if self.kill_t>=1:
            self.kill_t+=1
            #print(self.kill_t)
        if self.kill_t>25:
            self.kill_t=0
        #elif self.kill_t==11:
            self.numberkill(self.kill_n)
            self.kill_n=0

pygame.init()
load()

while 1:
    FPS=60
    FPSClock=pygame.time.Clock()
    game=Game()
    Player.goldbody=False
    Damage.containers = game.allsp
    screen = pygame.display.set_mode((1200,700))
    player = Player()
    cheek=False
    icon = pygame.transform.smoothscale(load_image('icon.png'),(32,32)).convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('NEW TANK!')
    #Boss()
    if pygame.mixer:
        music = os.path.join(main_dir, "data", "epic.mp3")
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    while game.RUN:
        if game.running=='r':
            FPSClock.tick(FPS)
            #screen.blit(background,(0,0))
            screen.fill((192,192,192))
            game.pressed_keys = pygame.key.get_pressed()
            game.pressed_mouse = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game.running = False
                    if event.key == K_p:
                        game.running = 'p'
                    if event.key == K_q:
                        player.changegun(0)
                    if event.key == K_e:
                        player.changegun(2)
                    if event.key == K_r:
                        player.changegun(3)
                    if event.key == K_c:
                        player.changegun(4)
                    if event.key == K_f and game.energy>=10 and player.subnum>0.25:
                        player.defend()
                    if (event.key == K_LSHIFT or event.key == K_RSHIFT) and game.energy>=20:
                        player.crazy()
                    if event.key == K_TAB and game.energy>=10:
                        player.elcshock()
                if event.type == QUIT:
                    game.running = False

            game.update()
            game.grounds.update()
            game.allsp.update()
            cheekp()
            showscore()
            pygame.display.update()
        elif game.running == 'p':
            screen.fill((135,206,250))
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game.RUN = False
                        sys.exit()
                    if event.key == K_SPACE:
                        game.running = 'r'
                        pygame.mixer.music.unpause()
                elif event.type == QUIT:
                    game.RUN = False
                    sys.exit()
            ptextfon=pygame.font.SysFont('SimHei',60)
            ptext=ptextfon.render('暂停中，按空格键继续',True,(128,0,255))
            screen.blit(ptext,[100,300])
            pygame.display.update()
            FPSClock.tick(FPS)
        elif game.running == False:
            screen.fill((255,255,255))
            pygame.mixer.music.stop()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game.RUN = False
                        sys.exit()
                    if event.key == K_SPACE:
                        game.RUN = False
                        game.running='r'
                elif event.type == QUIT:
                    game.RUN = False
                    sys.exit()
            textfon=pygame.font.SysFont('SimHei',60)
            text=textfon.render('GAME OVER!'+'总得分: '+str(game.score),True,(255,0,0))
            screen.blit(text,[0,300])
            pygame.display.update()
            FPSClock.tick(FPS)


