import pygame
import sys,os
from pygame.locals import *
import random
import math

vect = pygame.Vector2
class Gun(pygame.sprite.Sprite):
    def __init__(self,owner,drict_pos):
        pygame.sprite.Sprite.__init__(self)
        self.owner=owner
        self.rect=self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        #self.x=owner.rect.centerx
        #self.y=owner.rect.centery
        self.drict_pos=drict_pos
        self.angle=0
        self.time=0
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
    def update(self,drict_pos):
        self.drict_pos=drict_pos        
        self.rect= self.image.get_rect(center=(self.owner.rect.centerx,self.owner.rect.centery))
        if self.owner.isen:
            self.f_enrotate()
        else:
            self.f_rotate()
        self.chk_shoot()
        screen.blit(self.image,self.rect)
class Dirt(pygame.sprite.Sprite):
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life =120
    def update(self):
        
        self.life = self.life - 1
        screen.blit(self.image,self.rect)
        if self.life <=0:
            self.kill()
class Magnum(Gun):
    MINTIME=200
    MINSPEED=80
    def __init__(self,owner,drict_pos):
        super(Magnum,self).__init__(owner,drict_pos)    
        self.maxtime=500
        self.blspeed=60
        self.ispre=False
        self.r=50
    def shoot(self):
        Bomb(self)
        self.time=0

class Bomb(pygame.sprite.Sprite):
    def __init__(self,owner):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.live=120
        
        self.power=9999
        self.owner=owner
        self.speed=self.owner.blspeed
        self.angle=self.owner.angle
        self.radangle=self.owner.angle*math.pi/180
        self.center=(self.owner.rect.centerx+self.owner.r*math.cos(self.radangle),self.owner.rect.centery+self.owner.r*math.sin(self.radangle))
        self.original = self.image
        self.image= pygame.transform.rotate(self.original, -self.owner.angle)         
        self.rect=self.image.get_rect(center=self.center)
    def move(self):
        self.rect.move_ip(self.speed*math.cos(self.radangle),self.speed*math.sin(self.radangle))
        smallDirt(self)
        if self.rect.left <=0:
            self.kill()
        elif self.rect.right >= 1200:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        elif self.rect.bottom >= 700:
            self.kill()
        
    def explose(self):
        bigExplosion(self)
        self.kill()
    def update(self):
        
        self.move()
        
        screen.blit(self.image,self.rect)
        
class Meltgun(Gun):
    MINTIME=5
    MINSPEED=45
    def __init__(self,owner,drict_pos):
        super(Meltgun,self).__init__(owner,drict_pos)
        self.ispre=False
        if self.owner.isen:
            self.maxtime=self.owner.maxshootime
        else:
            self.maxtime=20        
        self.r=51
        self.angle0=11.5
        self.turn=1
        self.blspeed=8
    def shoot(self):
        if type(self.owner)==Enemytank0:
            enShortlight(self)
        else:
            Shortlight(self)        
        if self.turn==1:
            self.turn=2
        else:
            self.turn=1
        self.time=0



        
class Shortlight(pygame.sprite.Sprite):
    def __init__(self,owner):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.live=120
        self.power=owner.owner.shortltpor
        self.owner=owner
        self.speed=self.owner.blspeed
        if self.owner.turn==1:
            self.angle0=self.owner.angle+self.owner.angle0
        elif self.owner.turn==2:
            self.angle0=self.owner.angle-self.owner.angle0
        self.radangle0=self.angle0*math.pi/180
        self.radangle=self.owner.angle*math.pi/180
        self.center=(self.owner.rect.centerx+self.owner.r*math.cos(self.radangle0),self.owner.rect.centery+self.owner.r*math.sin(self.radangle0))
        self.image=random.choice(self.images)
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
    def explose(self):
        self.kill()
class enShortlight(Shortlight):
    def __init__(self,owner):
        super(enShortlight,self).__init__(owner)
        pygame.sprite.Sprite.__init__(self, self.containers)
        
class Railgun(Gun):
    MINTIME=180
    MINSPEED=60
    def __init__(self,owner,drict_pos):
        super(Railgun,self).__init__(owner,drict_pos)
        self.maxtime=300
        self.ispre=False
        self.starlist=[]
        self.r=10
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
                self.time=0
                if type(self.owner)==Enemytank1:
                    enLight(self)
                else:
                    Light(self)
                self.ispre=False
                
        #self.prepare()                
    def shoot(self):
        
        self.pre_time=0
        self.ispre=True
        self.star=Star(self)
class Light(pygame.sprite.Sprite):
    def __init__(self,owner):
        pygame.sprite.Sprite.__init__(self, self.containers)              
        self.owner=owner
        self.image=random.choice(self.images)
        self.power=self.owner.owner.ltpor
        #self.live=self.owner.maxtime/2
        self.speed=64
        self.target=None
        self.angle=self.owner.angle
        self.radangle=self.owner.angle*math.pi/180
        self.center=(self.owner.rect.centerx+self.owner.r*math.cos(self.radangle),self.owner.rect.centery+self.owner.r*math.sin(self.radangle))
        self.original = self.image
        self.image= pygame.transform.rotate(self.original, -self.angle)         
        self.rect=self.image.get_rect(center=self.center)
    def explose(self):
        pass
    def move(self):
        self.rect.move_ip(self.speed*math.cos(self.radangle),self.speed*math.sin(self.radangle))
        lightDirt(self,self.rect.centerx,self.rect.centery)
        self.oldcenter=self.rect.center
        self.rect.move_ip(32*math.cos(self.radangle),32*math.sin(self.radangle))
        lightDirt(self,self.rect.centerx,self.rect.centery)
        self.rect=self.image.get_rect(center=self.oldcenter)
        if self.rect.left <=-100:
            self.kill()
        elif self.rect.right >= 1300:
            self.kill()
        if self.rect.top <= -100:
            self.kill()
        elif self.rect.bottom >= 800:
            self.kill()
    def update(self):        
        self.move()       
        screen.blit(self.image,self.rect)
class lightDirt(Dirt):
    def __init__(self,owner,x,y):
        super(lightDirt,self).__init__(owner)
        self.owner=owner
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
        
    def update(self):
        self.live-=1
        if self.live<0:
            self.kill()
        self.center=(self.owner.rect.centerx+self.star_r*math.cos(self.owner.angle*math.pi/180),self.owner.rect.centery+self.star_r*math.sin(self.owner.angle*math.pi/180))
        self.rect=self.image.get_rect(center=self.center)
        self.starindex=self.owner.pre_time//4
        self.image=self.images[self.starindex]
        screen.blit(self.image,self.rect)
class Lightold(pygame.sprite.Sprite):
    def __init__(self,owner):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        
        self.owner=owner
        self.power=self.owner.owner.ltpor
        self.live=self.owner.maxtime/2
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
        if type(self.owner)==Player:
            self.txtlist=['GOOD!!','Well done!!','Super killer!']
            self.list=pygame.sprite.spritecollide(self,game.enemies,False, pygame.sprite.collide_mask)
            lenth=len(self.list)
            if lenth>=2:
                index=lenth-2
                if index>2:
                    index=2
                txt=self.txtlist[index]#random.choice(['Well done!!','GOOD!!','Super killer!'])
                Damage(txt,(255,255,0),40,(600,200))
            player.railgun.time+=len(self.list)*20
            for one in self.list:
                one.hurt(self.power)
        else:
            self.list=pygame.sprite.spritecollide(self,game.playerlist,False, pygame.sprite.collide_mask)
            for one in self.list:
                one.hurt(self.power)
    def update(self):
        
        self.live-=1
        self.num=self.live//2
        
        if self.num%2!=0:
           screen.blit(self.image,self.rect)
        else:
            screen.blit(self.image1,self.rect)
            
        #screen.blit(self.image,self.rect)
        if self.live<=0:
            self.kill()

class enLight(Light):
    def __init__(self,owner):
        super(enLight,self).__init__(owner)
        pygame.sprite.Sprite.__init__(self,self.containers)
    def explose(self):
        self.power=0
class Explosion(pygame.sprite.Sprite):
    
    animcycle = 2
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #pygame.sprite.Sprite.__init__(self, self.containers),,pygame.transform.scale(load_image('fire1.png'),(90,90))
        self.image = self.images[0]
        self.actor=actor
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        self.life = 0
        self.maxindx=4
        self.maxliv=30
    def update1(self,ifdirt):
        
        self.life = self.life + 1
        self.index=self.life//self.animcycle
        if self.index>=self.maxindx:
            self.index=self.maxindx
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.actor.rect.center)
        
        screen.blit(self.image,self.rect)
        if self.life >= self.maxliv:
            if type(player.gun)!=Railgun and ifdirt:
                Dirt(self.actor)            
            self.kill()
    def update(self):
        self.update1(True)
class bigExplosion(Explosion):
    def __init__(self, actor):
        super(bigExplosion,self).__init__(actor)
        self.maxindx=7
        self.maxliv=16
        self.txtlist=['GOOD!!','Well done!!','Super killer!']
    def cheek(self):
        self.list=pygame.sprite.spritecollide(self,game.enemies,False)
        lenth=len(self.list)
        if lenth>=1:
            index=lenth-1
            if index>2:
                index=2
            txt=self.txtlist[index]#random.choice(['Well done!!','GOOD!!','Super killer!'])
            Damage(txt,(255,255,0),40,(600,200))
        for one in self.list:
            one.hurt(self.actor.power)
        player.magnum.time+=len(self.list)*20
    def update(self):
        self.cheek()
        self.update1(False)
        

class smallDirt(Dirt):
    def __init__(self,owner):
        super(smallDirt,self).__init__(owner)
        self.owner=owner
        self.life =60  
        self.rect=self.image.get_rect(center=self.owner.rect.center)
        
class Enemy(pygame.sprite.Sprite):
    maxshootime=360
    live=100
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.isen=True
        self.x=random.randint(0,1200)
        self.y=random.randint(0,700)        
                
        self.shootime=0
    def move(self):
        pass
        #self.rect = self.image.get_rect()
    def display(self):
        screen.blit(self.image,self.rect)
    def hurt(self,power):
        self.live-=power        
        if self.live<=0:
            Damage(power,(0,0,255),30,self.rect.center)
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
        Explosion(self)
        self.kill()
    def shoot(self):
        pass        
    def update(self):
        if self.maxshootime<=60:
            self.maxshootime=60
        if self.shootime<self.maxshootime:
            self.shootime+=1
        elif len(game.enBulletgroup)<50:
            self.shoot()
            self.shootime=0        
        self.display()
        self.move()
        
class Enemy0(Enemy):
    maxshootime=200
    live=100
    def __init__(self):
        super(Enemy0,self).__init__()
        self.iplist=[(0,-1),(0,1),(-1,0),(1,0)]
        self.enname=random.randint(0,3)
        self.image=self.images[self.enname]
        self.rect = self.image.get_rect(center=(self.x,self.y))
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
        self.live-=power        
        if self.live<=0:
            Damage(power,(0,0,255),30,self.rect.center)
            if player.iscrazy:
                self.distory(1,1,0,2)
            else:
                self.distory(1,1,2,2)
        else:
            Damage(power,(180,180,180),25,self.rect.center)
    def shoot(self):
        BulletCoordinate(self.rect.centerx,self.rect.centery,self.enname)
class Enemy1(Enemy0):
    maxshootime=300
    live=150
    def __init__(self):
        super(Enemy1,self).__init__()
    def shoot(self):
         for i in range(4):
            BulletCoordinate(self.rect.centerx,self.rect.centery,i)
    def hurt(self,power):
        self.live-=power        
        if self.live<=0:
            Damage(power,(0,0,255),30,self.rect.center)
            if player.iscrazy:
                self.distory(2,1,0,2)
            else:
                self.distory(2,1,2,2)
        else:
            Damage(power,(180,180,180),25,self.rect.center)
class Enemytank0(Enemy):
    maxshootime=40
    live=100
    def __init__(self):
        super(Enemytank0,self).__init__()
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.angle=random.randint(0,360)
        self.speed=4
        self.maxlive=100
        self.rotate = False
        self.rotspeed=1        
        self.gun=Meltgun(self,player.rect.center)
        self.shortltpor=5
        self.turntime=0
        self.iscrazy=False
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

    def moveL(self):
        self.rotateit(2)
    def moveR(self):
        self.rotateit(-2)
    def moveU(self):
        self.rect.move_ip(self.speed*math.sin((self.angle/180)*math.pi),self.speed*math.cos((self.angle/180)*math.pi))
    def moveD(self):
        self.rect.move_ip(-self.speed*math.sin((self.angle/180)*math.pi),-self.speed*math.cos((self.angle/180)*math.pi))
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
        if random.choice([True,False]):
            self.moveU()
        self.turn()
        if self.rect.left <=0:
            self.rect.left=0
            self.rotateit(60)
            self.moveU()
        elif self.rect.right >= 1200:
            self.rect.right = 1200
            self.rotateit(-60)
            self.moveU()
        if self.rect.top <= 0:
            self.rect.top = 0
            self.rotateit(60)
            self.moveU()
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.rotateit(-60)
            self.moveU()
    def shoot(self):
        self.gun.shoot()
    def update(self):
        if self.gun.time>=self.gun.maxtime and (not self.gun.ispre):
            self.gun.shoot()
        self.move()
        self.display()
        self.gun.update(player.rect.center)
        self.gun.encold()
class Enemytank1(Enemytank0):
    maxshootime=200
    live=180
    def __init__(self):
        super(Enemytank1,self).__init__()
        self.gun=Railgun(self,player.rect.center)
        self.gun.maxtime=200
        self.isen=True
        self.ltpor=30
    
class BulletCoordinate(pygame.sprite.Sprite):
    power=10
    def __init__(self,x,y,plname):
        pygame.sprite.Sprite.__init__(self, self.containers)
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
        #self.rect=self.image.get_rect()
    def display(self):
        screen.blit(self.image,self.rect)
    def explose(self):
        self.kill()
    def update(self):
        self.move()
        self.display()
    
#class Tank
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.plane=0
        self.image = self.images[self.plane]
        self.angle=0
        self.speed=6
        self.level=0
        self.maxlive=100
        self.rotspeed=5
        #self.image = pygame.image.load(self.plane).convert()
        self.rect = self.image.get_rect()
        self.israilgun=True
        self.isen=False
        self.rotate = False
        self.gunnum=1
        self.railgun=Railgun(self,pygame.mouse.get_pos())
        self.meltgun=Meltgun(self,pygame.mouse.get_pos())
        self.magnum=Magnum(self,pygame.mouse.get_pos())
        self.gunlist=[self.magnum,self.meltgun,self.railgun]
        self.gun=self.gunlist[self.gunnum]
        self.goldtime=0
        self.defendtime=0
        self.subnum=1
        self.crazyeg=0
        self.iscrazy=False
        self.oldscore=0
        self.shortltpor=20
        self.ltpor=500
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
        self.gun.update(pygame.mouse.get_pos())
        for gun1 in self.gunlist:
            gun1.encold()
    def ifgrow(self):
        self.addscore=game.score-self.oldscore
        if self.addscore>=10:
            for i in range(self.addscore//10):
                self.level+=1
                Damage('LEVEL UP!',(0,255,0),33,self.rect.center)
                self.oldscore=game.score
                self.maxlive+=5
                self.shortltpor+=2
                self.ltpor+=10
                self.addlive(30)
                for guni in self.gunlist:                
                    guni.maxtime=guni.maxtime*0.95
                    guni.blspeed=guni.blspeed*1.05
                if not self.iscrazy:
                    self.gun.old_maxtime=self.gun.maxtime
                    self.gun.oldblspeed=self.gun.blspeed
    def changegun(self,n):
        if not self.iscrazy:
            '''
            #if game.pressed_keys[K_q]:                
            if self.gunnum<2:
                self.gunnum+=1
            else:
                =0
            '''
            if self.gunnum==n:
                self.gunnum=1
                self.gun=self.gunlist[self.gunnum]
            else:
                self.gunnum=n
                self.gun=self.gunlist[self.gunnum]
            self.gun.old_maxtime=self.gun.maxtime
            self.gun.oldblspeed=self.gun.blspeed
    def addlive(self,liv1):
        liv1=int(liv1)
        game.live+=liv1
        
        if game.live>self.maxlive:
            game.live=self.maxlive
        else:
            Damage(liv1,(0,255,0),30,self.rect.center)
    def defend(self):
        self.isdefend=True
        self.subnum=0.5
        self.defendtime+=500
        game.energy-=10
    def repair(self):
        self.addlive(self.maxlive-game.live)
        game.energy-=20
    def cheek(self):
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
        if not self.iscrazy:
            if (self.magnum.time<self.magnum.maxtime) or (self.railgun.time<self.railgun.maxtime):
                self.gunnum=1
                self.gun=self.gunlist[self.gunnum]
        #self.if_changegun()
    def hurt(self,power):
        
        self.power=int(power)
        game.live-=self.power*self.subnum
        Damage(self.power*self.subnum,(255,0,0),25,self.rect.center)
    def distory(self):
       
        if game.live<=0:            
            self.kill()
            game.running=False
    def crazy(self):
        self.gun.blspeed=self.gun.blspeed*2  
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
    Explosion.images = [pygame.transform.scale(img,(i,i)) for i in [15,45,75,90,120]]
    bigExplosion.images = [pygame.transform.scale(img,(i,i)) for i in [50,90,120,150,180,210,240,270]]
    #Missle.images=[pygame.transform.scale(load_image('bigmissle.png'),(60,20)),pygame.transform.scale(load_image('dronemissle.png'),(40,15))]
    Player.images=[pygame.transform.smoothscale(load_image('ground2.png'),(60,80))]
    BulletCoordinate.images=load_images('bulletU.png','bulletD.png','bulletL.png','bulletR.png')
    Player.star=pygame.transform.smoothscale(load_image('star2.png'),(60,60))
    Player.dfnimg=pygame.transform.smoothscale(load_image('defendimg.png'),(120,120))
    enemyimage0=pygame.transform.smoothscale(load_image('enemy0.png'),(80,60))
    enemyimage1=pygame.transform.smoothscale(load_image('enemy1.png'),(100,75))
    Enemy0.images=[pygame.transform.rotate(enemyimage0,90),pygame.transform.rotate(enemyimage0,270),enemyimage0,pygame.transform.rotate(enemyimage0,180)]
    Enemytank0.image=pygame.transform.smoothscale(load_image('ground2.png'),(60,80))
    Enemytank1.image=pygame.transform.smoothscale(load_image('ground2.png'),(60,80))
    Enemy1.images=[pygame.transform.rotate(enemyimage1,90),pygame.transform.rotate(enemyimage1,270),enemyimage1,pygame.transform.rotate(enemyimage1,180)]
    Enemytank1.image=pygame.transform.smoothscale(load_image('ground2.png'),(60,80))
    Railgun.image=pygame.transform.smoothscale(load_image('gun.png'),(100,30))
    Railgun.star=load_image('gunstar1.png')
    Meltgun.image=pygame.transform.smoothscale(load_image('gun2.png'),(100,40))
    Magnum.image=pygame.transform.smoothscale(load_image('magnum.png'),(130,40))
    Star.images=[]
    for scale in range(1,21):
        Star.images.append(pygame.transform.scale(load_image('gunstar1.png'),(scale,scale)))
    Dirt.image=pygame.transform.smoothscale(load_image('BlastMark2.png'),(100,100))
    smallDirt.image=pygame.transform.smoothscale(load_image('defendimg.png'),(20,20))
    #lightDirt.image=pygame.transform.smoothscale(load_image('lit.png'),(32,15))
    Light.images=[pygame.transform.smoothscale(load_image('lit.png'),(32,15)),pygame.transform.smoothscale(load_image('lit1.png'),(32,15))]
    enLight.images=[pygame.transform.smoothscale(load_image('lit2.png'),(32,15))]
    Shortlight.images=[]
    for i in range(1,5):
        Shortlight.images.append(pygame.transform.scale(load_image('shortlight'+str(i)+'.png'),(32,10)))
    enShortlight.images=[pygame.transform.smoothscale(load_image('shortlight1.png'),(30,10))]
    Bomb.image=pygame.transform.smoothscale(load_image('dronemissle.png'),(40,15))
def cheekp():
        
        get_dic=pygame.sprite.groupcollide(game.enemies,game.Bulletgroup,False,False)                                    
        lost_list=pygame.sprite.spritecollide(player,game.enBulletgroup,False)        
        for one_en in get_dic:
            power=0
            if get_dic[one_en] is not None:
                for one_bl in get_dic[one_en]:
                    power+=one_bl.power
                    one_bl.explose()
                
                one_en.hurt(power)
                get_dic[one_en]=None
        
        if player.goldbody is not True:        
            for one2 in lost_list:
                player.hurt(one2.power)
                one2.explose()
                player.distory()
        else:
            dist_list=pygame.sprite.spritecollide(player,game.enemies,False)
            for one3 in dist_list:
                one3.distory(1,0,1,0)

def showscore():
    
    textfont=pygame.font.SysFont('arial',30) #创建文本对象，大小30
    t1=textfont.render('score:'+str(game.score)+' level:'+str(player.level)+' Gun energy:'+str(int(player.gun.time))+' energy:'+str(game.energy),True,(255,0,0))
    t2=textfont.render('Your energy is more than 20 ,press C to use a special power or key SHIFT for repair!!!',True,(128,0,255))#生成平滑的红色字符串
    t3=textfont.render('Your energy is more than 10 ,press key F to use double!!!',True,(128,0,255))
    screen.blit(t1,[50,20]) #在窗口显示
    if game.energy>=20:
        screen.blit(t2,[50,80])
    if game.energy>=10:
        screen.blit(t3,[50,50])
class Game():
    allsp = pygame.sprite.RenderUpdates()#pygame.sprite.Group()
    score=0
    time=0
    live=100
    energy=20
    RUN=True
    running = 'r'
    pressed_keys = None
    pressed_mouse =None
    allEnemy=[Enemy0,Enemy1,Enemytank0,Enemytank1]
    enemies = pygame.sprite.Group()
    grounds=pygame.sprite.Group()
    Bulletgroup=pygame.sprite.Group()
    playerlist=pygame.sprite.Group()
    enBulletgroup=pygame.sprite.Group()
    Player.containers = allsp,playerlist
    Damage.containers = allsp
    Enemy.containers = enemies,allsp
    BulletCoordinate.containers = enBulletgroup,allsp
    Light.containers = allsp,Bulletgroup
    enLight.containers = allsp,enBulletgroup
    Star.containers = allsp
    Bomb.containers = Bulletgroup,allsp
    maxenum=10
    Explosion.containers = allsp
    Shortlight.containers = Bulletgroup,allsp
    enShortlight.containers = enBulletgroup,allsp
    Dirt.containers = grounds
    smallDirt.containers = allsp
    lightDirt.containers = allsp
    oldaddtime=0
    addentime=150
    oldfasttime=0
    getfastime=450
    #Bombgroup=pygame.sprite.Group()
    #Toolsgroup=pygame.sprite.Group()
    def update(self):
        self.time+=1
        self.addtime=self.time//self.addentime-self.oldaddtime
        if self.addtime>0:
            self.oldaddtime=self.time//self.addentime
            for i in range(self.addtime):
                if len(self.enemies)<self.maxenum:
                    self.addenemy()
                    #print(self.time)
        self.addtime1=self.time//self.getfastime-self.oldfasttime            
        if self.addtime1>0:
            self.oldfasttime=self.time//self.getfastime
            for i in range(self.addtime1):
                self.addentime-=3
                
                BulletCoordinate.power+=0.1
                for e in self.allEnemy:                    
                    e.live+=5
                    e.maxshootime=e.maxshootime*0.95
                    if e.maxshootime<20:
                        e.maxshootime=20
        if self.addentime<=80:
                self.addentime=80
        if self.time>=2000:
            self.time=0
            self.oldaddtime=0
            self.oldfasttime=0
    def addenemy(self):
        enemy=random.choice(self.allEnemy)
        enemy()
pygame.init()
FPS=60
FPSClock=pygame.time.Clock()
game=Game()
'''
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

'''
Player.goldbody=False
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
                
                
                if event.key == K_q:
                    player.changegun(0)
                if event.key == K_e:
                    player.changegun(2)    
                if (event.key == K_c) and game.energy>=20:
                    player.crazy()
                if (event.key == K_LSHIFT or event.key == K_RSHIFT) and game.energy>=20:
                    player.repair()    
            if event.type == QUIT:
                game.running = False
            '''
            if event.type == pygame.MOUSEBUTTONDOWN and player.gun.time>=player.gun.maxtime and  (not player.railgun.ispre):
                player.gun.prepare()

            if event.type==ADDENEMY:
                if len(game.enemies)<20:
                    Enemy()
            if event.type==SHOOT:                
                for en1 in game.enemies:
                    en1.shoot()

            if event.type==GET_FASTER:
                addtime-=50
                if addtime<=300:
                    addtime=300
                pygame.time.set_timer(ADDENEMY,addtime)
                
                #pygame.time.set_timer(SHOOT,shoottime)
    
            if player.goldbody:    
                if event.type==GOLDBODY:
                    player.goldbody=False
            '''
        
        game.update()
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

        
