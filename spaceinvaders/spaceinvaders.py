'''
Created on Feb 23, 2015

@author: spencerleal
'''

import pygame
import sys
import random
from pygame.locals import *
        
class Animate():
    INDICES = [1, 0]
    @staticmethod
    def switch_index(index):
        return Animate.INDICES[index]
    @staticmethod
    def get_speed(length):
        if length >= 45:
            return 50
        elif length >= 35:
            return 45
        elif length >= 25:
            return 40
        elif length >= 15:
            return 35
        elif length >= 10:
            return 35
        elif length >= 7:
            return 30
        elif length >= 6:
            return 25
        elif length >= 5:
            return 20
        elif length >= 4:
            return 10
        elif length >= 3:
            return 7
        elif length >= 2:
            return 4
        else:
            return 2

class Explosion():
    explosion_sprite = pygame.image.load("sprites/explosion.png")
    def __init__(self, enemy, ticks):
        self.image = Explosion.explosion_sprite
        self.width = 26
        self.x = ((enemy.x+enemy.x+enemy.width)-self.width)/2
        self.y = enemy.y
        self.first_tick = ticks
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def update(self, ticks):
        pass

class Hud():
    def __init__(self):
        self.level = Level()
        self.lives = Lives()
        self.score = Score()
        self.hud = []
        self.hud.append(self.level)
        self.hud.append(self.lives)
        self.hud.append(self.score)
    def reset(self):
        self.level.reset()
        self.lives.reset()
        self.score.reset()
    def adjust_lives(self, num):
        self.lives.adjust(num)
    def adjust_score(self, enemy):
        self.score.adjust(enemy)
    def game_over(self):
        return self.lives.lives==0
    def next_level(self):
        self.level.next_level()
        self.lives.adjust(1)
        

class Invader(pygame.sprite.Sprite):
    invader_sprites = {
        '1' : (pygame.image.load("sprites/invader1a.png"), pygame.image.load("sprites/invader1b.png")),
        '2' : (pygame.image.load("sprites/invader2a.png"), pygame.image.load("sprites/invader2b.png")),
        '3' : (pygame.image.load("sprites/invader3a.png"), pygame.image.load("sprites/invader3b.png"))
    }
    MAX_WIDTH = 24
    WIDTHS = (16, 22, 22, 24, 24)
    SCORES = (40, 20, 20, 10, 10)
    IMAGES = ('1', '2', '2', '3', '3')
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.width = self.WIDTHS[self.row]
        self.x = col*32+(24-self.width/2)
        self.y = (row+1)*30
        self.dict_index = self.IMAGES[self.row] 
        self.tuple_index = 0
        self.image = self.invader_sprites[self.dict_index][self.tuple_index]   
    def get_score(self):
        return Invader.SCORES[self.row]  
    def update(self):
        self.tuple_index = Animate.switch_index(self.tuple_index)
        self.image = Invader.invader_sprites[self.dict_index][self.tuple_index]
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def adjust_projectile(self, projectile):
        projectile.index = 0
        projectile.movement = 7
        projectile.width = 8
        projectile.image = Projectile.invader_projectiles[projectile.index]
        
class Invaders():
    NUM_ROWS = 5
    NUM_COLS = 11
    def __init__(self):
        self.invaders = []
        self.movement_x = 10
        self.movement_y = 15
        for i in range(Invaders.NUM_ROWS):
            for j in range(Invaders.NUM_COLS):
                self.invaders.append(Invader(j, i))         
    def draw(self, screen):
        for invader in self.invaders:
            invader.draw(screen)  
    def update(self, ticks):
        if (ticks%self.get_speed()==0):
            self.move_x()
    def get_speed(self):
        return Animate.get_speed(len(self.invaders))
    def move_x(self):
        for invader in self.invaders:
            if invader.x+self.movement_x*3.5 > Game.SCREEN_WIDTH or invader.x+self.movement_x*2 < 0:
                self.move_y()
                self.movement_x *= -1
                break
        for invader in self.invaders:
            invader.x += self.movement_x
            invader.update()           
    def move_y(self):
        for invader in self.invaders:
            invader.y += self.movement_y

class Level():
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.level = 1
        self.update_level()
    def draw(self, screen):
        screen.blit(self.level_display, (Game.SCREEN_WIDTH/2-20, 0))
    def next_level(self):
        self.level += 1
        self.update_level()
    def reset(self):
        self.level = 1
    def update_level(self):
        self.level_string = "Level: " + str(self.level)
        self.level_display = self.font.render(self.level_string, False, (255, 255, 255))
            
class Lives():
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.lives = 3
        self.update_lives()
    def draw(self, screen):
        screen.blit(self.lives_display, (Game.SCREEN_WIDTH-70, Game.SCREEN_HEIGHT-15))
        for i in range(self.lives):
            screen.blit(Ship.ship_sprite, (Game.SCREEN_WIDTH-100-i*30, Game.SCREEN_HEIGHT-15))
    def adjust(self, num):
        self.lives += num
        self.update_lives()
    def reset(self):
        self.lives = 3
        self.update_lives()
    def update_lives(self):
        self.lives_string = "Lives: " + str(self.lives)
        self.lives_display = self.font.render(self.lives_string, False, (255, 255, 255))
 
class Mothership(pygame.sprite.Sprite):
    mothership_sprite = pygame.image.load("sprites/mothership.png")
    def __init__(self, direction):
        self.image = self.mothership_sprite
        self.movement = 2.5
        self.x = 0
        self.y = 10
        self.width = 30
        if direction < .02:
            self.movement = -2.5
            self.x = Game.SCREEN_WIDTH
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))     
    def update(self, ticks):
        self.x += self.movement    
    def get_score(self):
        rand = random.random()
        if rand > .85:
            add = 250
        elif rand > .65:
            add = 200
        elif rand > .40:
            add = 150
        else:
            add = 100
        return add
         
class Projectile(pygame.sprite.Sprite):
    player_projectile = pygame.image.load("sprites/projectile.png")
    invader_projectiles = (pygame.image.load("sprites/invader_projectile.png"), pygame.image.load("sprites/invader_projectile2.png"))
    def __init__(self, firer):
        self.firer = firer;
        self.x = self.firer.x+self.firer.width/2
        self.y = self.firer.y
        self.firer.adjust_projectile(self)
    def update(self, ticks):
        self.y += self.movement
        if ticks%5==0 and isinstance(self.firer, Invader):
            self.index = Animate.switch_index(self.index)
            self.image = self.invader_projectiles[self.index]
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))    
    def collides_with(self, other):
        return self.x+self.width >= other.x and self.x <= other.x+other.width and abs(other.y-self.y) <= 10
         
class Sounds():
    projectile_sound = None
    def __init__(self):
        Sounds.projectile_sound = pygame.mixer.Sound("sounds/projectile_sound.wav")
        Sounds.ship_explosion_sound = pygame.mixer.Sound("sounds/ship_explosion_sound.wav")
        
class Score():
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.score = 0
        self.high_score = 0
        self.update_score()      
    def draw(self, screen):
        screen.blit(self.score_display, (Game.SCREEN_WIDTH-100, 0))
        screen.blit(self.high_score_display, (0, 0))      
    def adjust(self, enemy):
        self.score += enemy.get_score()
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_score()
    def reset(self):
        self.score = 0
        self.update_score( )
    def update_score(self):
        self.score_string = "Score: " + str(self.score)
        self.score_display = self.font.render(self.score_string, False, (255, 255, 255))
        self.high_score_string = "High Score: " + str(self.high_score)
        self.high_score_display = self.font.render(self.high_score_string, False, (255, 255, 255))
         
class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), DOUBLEBUF)
        self.clear()
    def draw(self, sprites, hud):
        self.clear()
        for sprite in sprites:
            sprite.draw(self.screen)
        for hud_element in hud:
            hud_element.draw(self.screen)
        pygame.display.flip()      
    def clear(self):
        self.screen.fill((0, 0, 0))

class Ship(pygame.sprite.Sprite):
    ship_sprite = pygame.image.load("sprites/ship.png")
    MOVE_RIGHT = 5
    MOVE_LEFT = -5
    def __init__(self):
        self.image = self.ship_sprite
        self.x = Game.SCREEN_WIDTH/2
        self.y = Game.SCREEN_HEIGHT-100
        self.width = 26
        self.movement = 0    
    def adjust_projectile(self, projectile):
        projectile.movement = -15
        projectile.width = 5 
        projectile.image = Projectile.player_projectile
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def move_right(self):
        self.movement = Ship.MOVE_RIGHT   
    def move_left(self):
        self.movement = Ship.MOVE_LEFT
    def stop_movement(self):
        self.movement = 0
        
    def update(self, ticks):
        if self.x + self.movement < 0:
            self.x = 0
        elif self.x + self.width + self.movement > Game.SCREEN_WIDTH:
            self.x = Game.SCREEN_WIDTH - self.width
        else:
            self.x += self.movement
                    
class Timer():
    def __init__(self):
        self.clock = pygame.time.Clock()
    def tick(self):
        return self.clock.tick(Game.FPS)
        
class Game():
    DELAY = 10
    INTERVAL = 10
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 480
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    FPS = 60
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.key.set_repeat(self.DELAY, self.INTERVAL)
        pygame.display.set_caption("Space Invaders")
        self.state = Game.PLAYING
        self.screen = Screen()
        self.timer = Timer()
        self.ship = Ship()
        self.sounds = Sounds()
        self.hud = Hud()
        self.new_game()
    
    def new_game(self):
        self.hud.reset()
        self.ticks = 0
        self.projectile = None
        self.mothership = None
        self.explosion = None
        self.enemy_projectiles = []
        self.actors = []
        self.actors.append(self.ship)
        self.make_invaders()
        
    def game_loop(self):
        while True:
            self.timer.tick()
            self.ticks += 1
            self.screen.draw(self.actors, self.hud.hud)
            self.process_input()
            self.update_actors()
            self.do_tick_based_events()    
            if self.level_cleared():
                self.next_level()
            elif self.game_over():
                self.new_game()
    
    def game_over(self):
        return self.hud.game_over()
    
    def check_enemy_projectiles(self):
        for enemy_projectile in self.enemy_projectiles:
            if enemy_projectile.y > Game.SCREEN_HEIGHT:
                self.remove_enemy_projectile(enemy_projectile)
            elif enemy_projectile.collides_with(self.ship):
                Sounds.ship_explosion_sound.play()
                self.remove_enemy_projectile(enemy_projectile)
                self.hud.adjust_lives(-1)
            elif self.projectile and enemy_projectile.collides_with(self.projectile):
                self.do_explosion(enemy_projectile)
                self.remove_enemy_projectile(enemy_projectile)
                self.remove_projectile()
    
    def check_explosion(self):
        if self.ticks-self.explosion.first_tick >= 10:
            self.remove_explosion()
    
    def check_mothership(self):
        if self.mothership.x+self.mothership.width < 0 or self.mothership.x > Game.SCREEN_WIDTH:
            self.remove_mothership()
    
    def check_projectile(self):
        if self.projectile.y <= 0:
            self.remove_projectile()
            return
        if self.mothership and self.projectile.collides_with(self.mothership):
            self.hud.adjust_score(self.mothership)
            self.do_explosion(self.mothership)
            self.remove_mothership()
            self.remove_projectile()
            return
        for invader in self.invaders.invaders:
            if self.projectile.collides_with(invader):
                self.hud.adjust_score(invader)
                self.do_explosion(invader)
                self.invaders.invaders.remove(invader)
                self.remove_projectile()
                return
            
    def check_invaders(self):
        row_index = 0
        col_index = 0
        firer = None
        for invader in self.invaders.invaders:
            if self.ship.y - invader.y <= 30:
                self.lives.set_lives(0)
                return
            if abs(invader.x+invader.width/2 - self.ship.x+self.ship.width/2) <= 30:
                col_index = invader.col
                row_index = invader.row
            if invader.col == col_index and invader.row >= row_index:
                firer = invader
        if firer:
            enemy_projectile = Projectile(firer)
            self.enemy_projectiles.append(enemy_projectile)
            self.actors.append(enemy_projectile)
    
    def make_invaders(self):
        self.invaders = Invaders()
        self.actors.append(self.invaders)
            
    def do_explosion(self, enemy):
        if self.explosion:
            self.remove_explosion()
        self.explosion = Explosion(enemy, self.ticks)
        self.actors.append(self.explosion)
    
    def do_tick_based_events(self):
        if self.ticks%Game.FPS==0:
            self.random_mothership()
            self.check_invaders()
    
    def fire_projectile(self):
        if self.projectile is None:
            Sounds.projectile_sound.play()
            self.projectile = Projectile(self.ship)
            self.actors.append(self.projectile)
    
    def level_cleared(self):
        return not self.invaders.invaders
    
    def next_level(self):
        self.hud.next_level()
        self.make_invaders()
            
    def process_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            key = pygame.key.get_pressed()
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.ship.move_right()
            elif key[pygame.K_a] or key[pygame.K_LEFT]:
                self.ship.move_left()
            else:
                self.ship.stop_movement()
            if key[pygame.K_SPACE]:
                self.fire_projectile()
                
    def random_mothership(self):
        rand =  random.random()
        if rand <= .04 and self.mothership is None:
            self.mothership = Mothership(rand)
            self.actors.append(self.mothership)
            
    def remove_enemy_projectile(self, enemy_projectile):
        self.actors.remove(enemy_projectile)
        self.enemy_projectiles.remove(enemy_projectile)
        
    def remove_explosion(self):
        self.actors.remove(self.explosion)
        self.explosion = None
            
    def remove_mothership(self):
        self.actors.remove(self.mothership)
        self.mothership = None
    
    def remove_projectile(self):
        self.actors.remove(self.projectile)
        self.projectile = None
        
    def update_actors(self):
        for actor in self.actors:
            actor.update(self.ticks)
        if self.projectile:
            self.check_projectile()
        if self.mothership:
            self.check_mothership()
        if self.enemy_projectiles:
            self.check_enemy_projectiles()
        if self.explosion:
            self.check_explosion()
    
         
if __name__ == '__main__':
    game = Game()
    game.game_loop()