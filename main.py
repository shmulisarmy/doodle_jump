import sys
import pygame as p
import random as r

def onplat():
    for plat in game.platforms:
        if game.player.bottom == plat.top:
            if plat.x-20 <= game.player.x <= plat.x + game.platwidth:
                return True
            
    print('not on platform')
    return False

def scroll(jumpspeed):
    for plat in game.platforms: 
        plat.y += jumpspeed
        if plat.y >= game.height:
            #reset position 
            plat.y -= game.height
            plat.x = r.randint(0, game.width-game.platwidth)
            if game.platforms.index(plat) == game.n: game.n+= 1 if game.n < 22 else -21

def fallscroll():
    for plat in game.platforms: 
        plat.y -= game.speed
        

class Game:
    def __init__(self):
        self.width, self.height = 400, 800
        if len(sys.argv) > 1:
            self.width = int(sys.argv[-1])
        self.platwidth, platheight = 60, 10
        self.speed = 8
        self.jumpspeed = self.speed
        self.window = p.display.set_mode((self.width, self.height))
        self.clock = p.time.Clock()
        self.player = p.Rect(self.width/2, (self.height//(self.speed*2))*self.speed, 20, 40)
        self.platforms = [p.Rect(r.randint(0, (self.width-platheight)//self.speed)*self.speed, r.randint(0, (self.height-self.platwidth)//self.speed)*self.speed, self.platwidth, platheight)for plat in range(self.width//18)]
        self.jump = 0
        self.n = 0
        self.superjumpspeed = self.speed*3
        p.display.set_caption('doodle jump')
        p.init()

    def jump_and_gravity(self):
        self.jumpspeed = self.speed
        if self.jump == 0:
            self.jumpspeed = self.speed
            if onplat(): self.jump = 20
            else: 
                if self.player.y < self.height - self.height/3: self.player.y += self.speed
                else: fallscroll()
        else:
            if self.player.y > self.height/3: 
                self.player.y -= self.jumpspeed 
            else: scroll(self.jumpspeed)
            self.jump -= 1

    def moving_platforms(self):
        for i in range(self.width//100):
            self.platforms[i*4].x -= .7
            self.platforms[(i*3)+1].x += .7
        try: spring = p.Rect(self.platforms[game.n%22].x+17, self.platforms[game.n%22].y-15, 15, 15)
        except: 
            self.n = 0
            return p.Rect(self.platforms[game.n%22].x+17, self.platforms[game.n%22].y-15, 15, 15)

        return spring
    
    def controls(self):
        for event in p.event.get():
            if (event.type == p.QUIT):
                p.quit()

        key = p.key.get_pressed()
        if key[p.K_RIGHT]: 
            self.player.x += self.speed
            if self.player.x >= self.width: self.player.x = 0
        elif key[p.K_LEFT]: 
            self.player.x -= self.speed
        if self.player.x < 0: self.player.x = self.width

    def render(self, spring):
        self.window.fill((100, 200, 255))
        for i, plat in enumerate(self.platforms):
            if (i%4 == 0 or i%3 == 1) and i != 4:
                p.draw.rect(self.window, (100, 100, 100), plat)
            else: p.draw.rect(self.window, (200, 50, 50), plat)
        p.draw.rect(self.window, (200, 100, 100), spring)    
        p.draw.rect(self.window, (100, 100, 200), self.player)
        p.display.update()

    def super_jump(self, spring):
        if self.player.colliderect(spring): self.jumpspeed = self.superjumpspeed

    def run(self):
        self.jump_and_gravity()
        spring = self.moving_platforms()
        self.super_jump(spring)
        self.controls()
        self.render(spring)


game = Game()
while True:
    game.clock.tick(45)
    game.run()