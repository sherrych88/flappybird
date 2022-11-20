import pygame
import random
from pygame import mixer
import os

# Setup
pygame.init()
clock = pygame.time.Clock()
channel = pygame.mixer.Channel(0)
sprites_folder = "/Users/Test/Desktop/flappybird/assets/sprites"
audio_folder = "/Users/Test/Desktop/flappybird/assets/soundeffects"
font_folder ="/Users/Test/Desktop/flappybird/assets/font"

# set up variables 
#background
screen_length = 649
screen_width = 600
window = pygame.display.set_mode((screen_width, screen_length))
background = pygame.image.load(os.path.join(sprites_folder,"background.png")).convert_alpha()
ground = pygame.image.load(os.path.join(sprites_folder,"ground.png")).convert_alpha()
x_ground = 0

# pipes / points
pipe_opening = 170
pipe_timer = 0
start = False
end = False
restart = False
points = 0
font = pygame.font.Font(os.path.join(font_folder,"flappyfont.ttf"), 30)
passed = False
show_locker = False
locker_disabled = False
option1_clicked = False
option2_clicked = False
option3_clicked = False
crash = False

# buttons
start_button_img = pygame.image.load(os.path.join(sprites_folder,"startbutton.png")).convert_alpha()
show_button = True
restart_button_img = pygame.image.load(os.path.join(sprites_folder,"restart.png")).convert_alpha()
locker_button_img = pygame.image.load(os.path.join(sprites_folder,"locker.png")).convert_alpha()
blue_img = pygame.image.load(os.path.join(sprites_folder,"blue2.png")).convert_alpha()
yellow_img = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"yellow2.png")).convert_alpha(), (60, 45))
black_img = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"black2.png")).convert_alpha(), (67, 47))

hit_sound = False

class BirdAnimation(pygame.sprite.Sprite):
    # creates bird
    def __init__(self, x, y):
        global option1_clicked
        global option2_clicked
        global option3_clicked
        pygame.sprite.Sprite.__init__(self)
        self.birds = []
        if option1_clicked == True:
            option1_clicked = False
            bird_1 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"blue1.png")).convert_alpha(), (50, 50))
            bird_2 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"blue2.png")).convert_alpha(), (50, 50))
            bird_3 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"blue3.png")).convert_alpha(), (50, 50))
        elif option2_clicked == True:
            option2_clicked = False
            bird_1 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"yellow1.png")).convert_alpha(), (60, 45))
            bird_2 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"yellow2.png")).convert_alpha(), (60, 45))
            bird_3 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"yellow3.png")).convert_alpha(), (60, 45))
        elif option3_clicked == True:
            option3_clicked = False
            bird_1 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"black1.png")).convert_alpha(), (67, 47))
            bird_2 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"black2.png")).convert_alpha(), (67, 47))
            bird_3 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"black3.png")).convert_alpha(), (67, 47))
        else:
            bird_1 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"red1.png")).convert_alpha(), (45, 35))
            bird_2 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"red2.png")).convert_alpha(), (45, 35))
            bird_3 = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"red3.png")).convert_alpha(), (45, 35))


        self.birds.append(bird_1)
        self.birds.append(bird_2)
        self.birds.append(bird_3)

        self.counter = 0
        self.image = self.birds[self.counter]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move = 0
        self.grav = 0
        self.up = False

    # runs through list of bird images to give animated effect
    def animation(self):
        animate = True
        if animate == True:
            self.counter += 0.2
            if self.counter >= len(self.birds):
                self.counter = 0
                animate = False
            # needs slower animation so int rounds numbers down, shows new bird every couple frames
            self.image = self.birds[int(self.counter)]

    # rotate the bird as it moves, when game over - bird rotates down
    def rotation(self):                                         # surface, angle
        self.image = pygame.transform.rotate(self.birds[int(self.counter)], -2 * self.move)
        if end == True:
            self.image = pygame.transform.rotate(self.birds[int(self.counter)], -90)

    # bird falls until it hits the ground
    def gravity(self):
        self.move += 0.5
        self.rect.y += int(self.move)
        if self.rect.bottom >= 533:
            self.move = 0
    
    def jump(self):
        #self.up for clicking once, not holding
        # press mouse once to jump
        if pygame.mouse.get_pressed()[0] == 1 and self.up == False:
            self.up = True
            self.move = -10
            # sound
            pygame.mixer.music.load(os.path.join(audio_folder,"flap_sound.wav"))
            pygame.mixer.music.play()
        if pygame.mouse.get_pressed()[0] == 0:
            self.up = False

#Pipe class
class Pipe(pygame.sprite.Sprite):
    # initialize pipes
    def __init__(self, x, y, flipped):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder,"pipe.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 500))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y]
    # scrolls pipes, deletes when off screen
    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (100, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_start(self):
        if show_button == True:
            window.blit(self.image, (self.rect.x, self.rect.y))

    def on_clicked(self, x, y):
        click_return = False
        position = pygame.mouse.get_pos()
        self.x = x
        self.y = y

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                click_return = True
                # button animates down
                self.rect.center = (self.x, y + 7)
            if pygame.mouse.get_pressed()[0] == 0:
                # once lifted mouse, button animates up
                self.rect.center = (self.x, self.y)
        if locker_disabled == True:
            click_return = False
        return click_return

    def draw_button(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Gameover():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"gameover.png")).convert_alpha(), (400, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class ScoreScreen():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"scorescreen.png")).convert_alpha(), (400, 200))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# locker feature for character selection
class Locker():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder,"scorescreen.png")).convert_alpha(), (320, 170))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw_locker(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# character options
class BirdOptions():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.up = False

    def draw_bird_option(self):
        if show_button == True:
            window.blit(self.image, (self.rect.x, self.rect.y))
            
    def bird_on_clicked(self, x, y):
        click_return = False
        position = pygame.mouse.get_pos()
        self.x = x
        self.y = y
        
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.up == False:
                self.up = True
                click_return = True
                # button animates down
                self.rect.center = (self.x, y + 7)
            if pygame.mouse.get_pressed()[0] == 0:
                # once lifted mouse, button animates up
                self.up = False
                self.rect.center = (self.x, self.y)
        return click_return


def show_score(x, y):
    score = font.render(str(points), True, (255, 255, 255))
    window.blit(score, (x, y))
    
def final_score(x, y):
    final_points = font.render(str(points), True, (70, 70, 70))
    window.blit(final_points, (x, y))

def restart():
    pipes_group.empty()
    brd.rect.x = 100
    brd.rect.y = screen_length / 2
    points = 0
    return points

# groups for sprites
moving_birds = pygame.sprite.Group()
brd = BirdAnimation(100, screen_length / 2)
moving_birds.add(brd)
pipes_group = pygame.sprite.Group()

# create instances
start_button = Button(screen_width / 2, 500, start_button_img)
restart_button = Button(screen_width / 2, 500, restart_button_img)
game_over = Gameover(screen_width / 2, 150)
score_screen = ScoreScreen(screen_width / 2, 320)

locker_button = Button(screen_width / 2, 450, locker_button_img)
locker_screen = Locker(screen_width / 2, 320)
option1_button = BirdOptions(screen_width / 3, screen_length / 2, blue_img)
option2_button = BirdOptions(screen_width / 2, screen_length / 2, yellow_img)
option3_button = BirdOptions(screen_width / 1.5, screen_length / 2, black_img)

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # create background
    window.blit(background, (0, 0))

    # draw pipes
    pipes_group.draw(window)

    # create ground, 533 - height of background
    window.blit(ground, (x_ground, 533))
        
    # create and animate flapping bird
    moving_birds.draw(window)

    start_button.draw_start()
    locker_button.draw_start()

    # start / locker button clicking and animation
    if start_button.on_clicked(screen_width / 2, 500) or restart_button.on_clicked(screen_width / 2, 500):
        start = True
    if locker_button.on_clicked(screen_width / 2, 450):
        show_locker = True
    if show_locker == True:
        locker_screen.draw_locker()
        option1_button.draw_bird_option()
        option2_button.draw_bird_option()
        option3_button.draw_bird_option()
        if option1_button.bird_on_clicked(screen_width / 3, screen_length / 2):
            option1_clicked = True
            brd.__init__(100, screen_length / 2)
        elif option2_button.bird_on_clicked(screen_width / 2, screen_length / 2):
            option2_clicked = True
            brd.__init__(100, screen_length / 2)
        elif option3_button.bird_on_clicked(screen_width / 1.5, screen_length / 2):
            option3_clicked = True
            brd.__init__(100, screen_length / 2)

    # creates left scroll, 23 is about the size of overhang of ground image
    if end == False:
        x_ground -= 3
        if abs(x_ground) > 23:
            x_ground = 0
        brd.animation()
    
    # once bird jumps, the button disappears
    if moving_birds.sprites()[0].rect.bottom < screen_length / 2 - 40:
        show_button = False
        show_locker = False

    # start button is clicked, the game starts
    if start == True:
        locker_disabled = True
        brd.gravity()
        brd.rotation()
        # if the bird has not collided with pipes, game has not ended
        if end == False:
            brd.jump()

            # creates and destroys pipes
            if pipe_timer <= 0:
                random_height = random.randint(200, 400)
                pipe_original = Pipe(screen_width, screen_length - random_height, False)
                pipe_flipped = Pipe(screen_width, screen_length - random_height - pipe_opening, True)
                pipes_group.add(pipe_original)
                pipes_group.add(pipe_flipped)
                pipe_timer = 150
            pipe_timer -= 1.5
            pipes_group.update()

            # Adds one point after passing each pipe
            show_score(screen_width / 2, 20)

            if len(pipes_group) > 0:
                if passed == False\
                and moving_birds.sprites()[0].rect.right < pipes_group.sprites()[0].rect.right\
                and moving_birds.sprites()[0].rect.left > pipes_group.sprites()[0].rect.left:
                    passed = True

                if passed == True\
                    and moving_birds.sprites()[0].rect.left > pipes_group.sprites()[0].rect.right:
                        mixer.music.load(os.path.join(audio_folder,"passed_sound.wav"))
                        mixer.music.play()
                        points += 1
                        passed = False

        # Game ends upon crash and hitting the top or bottom of the screen
        if pygame.sprite.groupcollide(moving_birds, pipes_group, False, False) or moving_birds.sprites()[0].rect.bottom >= 533 or moving_birds.sprites()[0].rect.top <= 0:
            end = True
            if not crash:
                pygame.mixer.music.load(os.path.join(audio_folder,"crash_sound.wav"))
                mixer.music.play()
                crash = True
                pygame.mixer.music.queue(os.path.join(audio_folder,"fall_sound.wav"))

        if end == True and moving_birds.sprites()[0].rect.bottom >= 533:
            game_over.show()
            score_screen.show()
            restart_button.draw_button()
    
            final_score(360, 300)
            final_text = font.render("Score: ", True, (70, 70, 70))
            window.blit(final_text, (200, 300))
            locker_disabled = False

            if restart_button.on_clicked(screen_width / 2, 500) == True:
                end = False
                points = restart()
                crash = False

    pygame.display.flip()
    clock.tick(60)