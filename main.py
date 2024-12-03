import pygame as pg
from sys import exit
from random import randint, choice
import os

pg.init()

#Takes path and return list of all items in tht folder
def import_folder(path):
    surface_list = []
    for _,__,image_files in os.walk(path):
        
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()  
            surface_list.append(image_surf)

    return surface_list

class Player(pg.sprite.Sprite):

    def __init__(self) :
        super().__init__()
        self.player_walk_test = import_folder('graphics\\Player\\run right')
        self.player_index = 0

        self.player_jump = pg.image.load('graphics\\Player\\jump.png').convert_alpha()

        self.image = self.player_walk_test[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,320))
        self.gravity = 0

        self.jump_sound = pg.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)


    
    def player_input (self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20 # how high player can jump
            self.jump_sound.play()

    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom>=320: self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.25
            if self.player_index >= len(self.player_walk_test) : self.player_index = 0
            self.image = self.player_walk_test[int(self.player_index)]
    
    
    def reset_player(self):
        self.rect.midbottom = 0
        self.gravity = 0

    def update(self) :
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacles(pg.sprite.Sprite):

    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
        
            fly_1 = pg.image.load('graphics\Fly\Fly1.png').convert_alpha()
            fly_2 = pg.image.load('graphics\Fly\Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210

        else:
            self.frames = import_folder('graphics\enemy run left')
            #C:\Users\Meshwa\Desktop\Mario Pairate\graphics\enemy run left
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames) : self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self) :
        self.animation_state()
        self.rect.x -= 10     #Speed of enemy
    
        self.destroy()

    
    def destroy(self):
        if self.rect.x <= -100: self.kill()

def display_score():
    curr_time = pg.time.get_ticks() - start_time
    score_surf = test_font.render(f'Score : {int(curr_time/1000)}',False,(64,64,64))   #display score
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)

    return int(curr_time/1000)


def collision_sprite ():
    if pg.sprite.spritecollide(player.sprite,obstacles_group,False):
        obstacles_group.empty()
        return False
    else:
        return True

#variables
# RES = WIDTH,HEIGHT = 1920,1080
RES = WIDTH,HEIGHT = 800,400    #Screen size
FPS = 60
game_active = False
start_time = 0
score = 0

screen = pg.display.set_mode(RES)
pg.display.set_caption("Pirate Mario") # name of game
clock = pg.time.Clock()
test_font = pg.font.Font('font/Pixeltype.ttf',50)  #Font and its size

bg_music = pg.mixer.Sound('audio/music.wav') 
bg_music.play(loops = -1)

#surfaces
sky_surf = pg.image.load('graphics/Sky.png').convert()
ground_surf = pg.image.load('graphics/ground.png').convert()

# player

# player_stand = pg.image.load('graphics\player\player_stand.png').convert_alpha()
player_stand = pg.image.load('graphics\\Player\\idle.png').convert_alpha()
player_stand = pg.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))


#Groups
player = pg.sprite.GroupSingle()
player.add(Player())

obstacles_group = pg.sprite.Group()

#intro
game_name = test_font.render("Pirate Mario",False,(245, 56, 56))  #Game name color
game_name_rect = game_name.get_rect(center = (400,70))

game_msg = test_font.render('Press  Space  to  run' , False , (245, 56, 56)) #color change
game_msg_rect = game_msg.get_rect(center = (400,330))

#timers
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer,1500)


while True:

    for event in pg.event.get():
        # to close the game
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        # for loading screen
        if  not game_active : 
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_active = True
                start_time = pg.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer : 
                obstacles_group.add(Obstacles(choice(['fly','enemy','enemy','enemy'])))  
                


    if game_active :
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))

        #text 
        score = display_score()

        #sprite player
        player.draw(screen)
        player.update()
        
        obstacles_group.draw(screen)
        obstacles_group.update()

        # collision
        game_active = collision_sprite()
        
    else:
        #for back ground color
        screen.fill((54, 55, 56))
        #screen.fill("red")
        screen.blit(player_stand,player_stand_rect)
        
        # for score msg
        score_msg = test_font.render(f'Your Score:{score}',False,(245, 56, 56))  #last score color
        score_msg_rect = score_msg.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0 :
            screen.blit(game_msg,game_msg_rect)
        else:
            screen.blit(score_msg,score_msg_rect)

    pg.display.update()
    clock.tick(FPS)

