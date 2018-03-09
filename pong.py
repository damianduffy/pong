#! python3

import sys
import os
import random
import math
import pygame
from pygame.locals import *
import config
import text

# Initialize game engine, screen and clock
pygame.init()
if config.FULLSCREEN == False:
    screen = pygame.display.set_mode(config.SCREENSIZE)
else:
    screen = pygame.display.set_mode(config.SCREENSIZE, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption(config.TITLE)
clock = pygame.time.Clock()

# font settings for scores
font = pygame.font.SysFont("monospace", 48)
msg_colour = (255,255,0)
bold = 1

# global variables
player1_score = 0
player2_score = 0

def new_game():
    global player1_score, player2_score, ball

    start = False

    while start == False:

        screen.blit(text.msg_newgame, text.centre_text(text.msg_newgame, config.SCREENSIZE))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # create a new puck
                    ball = puck([(config.SCREENSIZE[0] // 2) - (config.PUCK_SIZE[0] // 2), (config.SCREENSIZE[1] // 2) - (config.PUCK_SIZE[1] // 2)])

                    # reset player scores
                    player1_score = 0
                    player2_score = 0

                    return ball
                if event.key == K_n:
                    pygame.quit()
                    sys.exit()

def new_round():
    global new_round

    ball.new_round()
    new_round = False

    return ball

def exit_game():
    exit = 0
    pygame.mixer.pause()

    while exit == 0:

        screen.blit(text.msg_exit, text.centre_text(text.msg_exit, config.SCREENSIZE))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.quit()
                    sys.exit()
                if event.key == K_n:
                    exit = -1
                if event.key == K_SPACE:
                    exit = -1
                    new_game()

    pygame.mixer.unpause()

def pause_game():
    pause = 0
    pygame.mixer.pause()

    while pause == 0:
        screen.blit(text.msg_pause, text.centre_text(text.msg_pause, config.SCREENSIZE))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = -1

    pygame.mixer.unpause()

def score(position):
    global player1_score, player2_score, new_round

    if position <= 0:
        player2_score += 1
    else:
        player1_score += 1

    new_round = True

def draw_court():
    global player1_score, player2_score

    # screen background colour
    screen.fill(config.BLACK)

    # draw net in middle of court
    for i in range(10, config.SCREENSIZE[1], 40):
        pygame.draw.line(screen, config.WHITE, [(config.SCREENSIZE[0] // 2), i], [(config.SCREENSIZE[0] // 2), (i + 20)], 5)

    # display scores
    p1score = font.render(str(player1_score), bold, config.WHITE, config.BLACK)
    screen.blit(p1score, (config.SCREENSIZE[0] // 4, config.SCREENSIZE[1] // 10))
    p2score = font.render(str(player2_score), bold, config.WHITE, config.BLACK)
    screen.blit(p2score, ((config.SCREENSIZE[0] // 4) * 3, config.SCREENSIZE[1] // 10))

def load_image(name, colorkey = None):
    fullname = os.path.join('/home/damo/Programming/Python/Oh Mummy/data/img/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        print(os.getcwd())
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()

    return image # , image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join('snd/', name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)

    return sound

def key_down(event, player1, player2):
    if event.key == K_ESCAPE:
        exit_game()
    if event.key == K_UP:
        player2.move_up()
    if event.key == K_DOWN:
        player2.move_down()
    if event.key == K_q:
        player1.move_up()
    if event.key == K_a:
        player1.move_down()
    if event.key == K_p:
        pause_game()

def key_up(event, player1, player2):
    if event.key == K_UP:
        player2.stop_up()
    if event.key == K_DOWN:
        player2.stop_down()
    if event.key == K_q:
        player1.stop_up()
    if event.key == K_a:
        player1.stop_down()

def get_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def check_collision(ball, player1, player2):
    # check if the puck has hit player1's paddle
    if (ball.get_centre()[0] - (ball.get_size()[0] // 2)) <= (player1.get_centre()[0] + (player1.get_size()[0] // 2)):
        if ball.get_centre()[1] >= (player1.get_position_top() - (ball.get_size()[1] // 2)) and ball.get_centre()[1] <= (player1.get_position_bottom() + (ball.get_size()[1] // 2)):
            if ball.get_direction() < 0:
                return True
    # check if the puck has hit player2's paddle
    elif (ball.get_centre()[0] + (ball.get_size()[0] // 2)) >= (player2.get_centre()[0] - (player2.get_size()[0] // 2)):
        if ball.get_centre()[1] >= (player2.get_position_top() - (ball.get_size()[1] // 2)) and ball.get_centre()[1] <= (player2.get_position_bottom() + (ball.get_size()[1] // 2)):
            if ball.get_direction() > 0:
                return True
    else:
        return False

# put image info class here
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, frames = 1, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.frames = frames
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_frames(self):
        return self.frames

    def get_animated(self):
        return self.animated

# Load game sounds
score_snd = load_sound("score.ogg")
paddle_snd = load_sound("paddle.ogg")
wall_snd = load_sound("wall.ogg")

class paddle:
    def __init__ (self, position, size = config.PADDLE_SIZE, colour = config.WHITE, speed = config.PADDLE_SPEED, score = 0):
        self.position = position        # FIX - more acurately referred to as "start position"
        self.size = size[1]
        self.width = size[0]
        self.top = [self.position[0], self.position[1] - (self.size // 2)]
        self.bottom = [self.position[0], self.position[1] + (self.size // 2)]
        self.colour = colour
        self.speed = speed
        self.velocity = 0
        self.score = score

    def update(self):
        # check if the paddle is colliding with boundary
        if (self.velocity == -1 and self.top[1] > 0) or (self.velocity == 1 and self.bottom[1] < config.SCREENSIZE[1]):
            # update paddle position
            self.top[1] += self.velocity * self.speed
            self.bottom[1] += self.velocity * self.speed

    def draw(self):
        pygame.draw.line(screen, self.colour, self.top, self.bottom, self.width)

    def move_up(self):
        self.velocity += -1

    def move_down(self):
        self.velocity += 1

    def stop_up(self):
        self.velocity += 1

    def stop_down(self):
        self.velocity += -1

    def get_position_top(self):
        return self.top[1]

    def get_position_bottom(self):
        return self.bottom[1]

    def get_position_side(self):
        return self.top[0]

    def get_velocity(self):
        return self.velocity

    def get_centre(self):
        return [self.top[0], self.top[1] + (self.size // 2)]

    def get_size(self):
        return [self.width, self.size]

    def get_score(self):
        return self.score

class puck:
    def __init__ (self, position, size = config.PUCK_SIZE, colour = config.WHITE, speed = config.SPEED):
        self.position = position
        self.size = size
        self.colour = colour
        self.speed = speed
        self.direction = [random.choice([-1, 1]), random.choice([-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3])]
        self.velocity = [0, 0]

    def new_round(self):
        screen.blit(text.msg_score, text.centre_text(text.msg_score, config.SCREENSIZE))
        pygame.display.update()
        pygame.time.delay(1500)
        self.position = [(config.SCREENSIZE[0] // 2) - (config.PUCK_SIZE[0] // 2), (config.SCREENSIZE[1] // 2) - (config.PUCK_SIZE[1] // 2)]
        self.direction = [random.choice([-1, 1]), random.choice([-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3])]

    def set_velocity(self):
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]

    def update(self):
        self.set_velocity()
        # update the position of the puck x and y
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        # check for collision with play area boundaries or paddle
        self.check_position()

    def check_position(self):
        # check if the puck hits left or right boundaries
        if self.position[0] <= 0 or self.position[0] >= (config.SCREENSIZE[0] - self.size[0]):
            score_snd.play()
            # report the score and restart round
            score(self.position[0])
            self.new_round()
        # check if the puck hits top or bottom boundaries
        if self.position[1] <= 0 or self.position[1] >= (config.SCREENSIZE[1] - self.size[1]):
            wall_snd.play()
            self.direction[1] *= -1

    def draw(self):
        pygame.draw.rect(screen, self.colour, [self.position, self.size])

    def get_centre(self):
        return [self.position[0] + (self.size[0] // 2), self.position[1] + (self.size[1] //2)]

    def get_size(self):
        return self.size

    def get_direction(self):
        return self.direction[0]

    def bounce(self):
        # triggered if collision() function detects collision with paddle
        paddle_snd.play() # play bounce sound
        self.direction[0] *= -1

# Main game loop
def main():
    # start music
    if config.SOUND == True:
        background_track.play(-1)

    ball = new_game()
    player1 = paddle([config.PADDLE_SIZE[0], config.SCREENSIZE[1] // 2])
    player2 = paddle([config.SCREENSIZE[0] - config.PADDLE_SIZE[0], config.SCREENSIZE[1] // 2])

    while True:
        # event handlers
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key_down(event, player1, player2)
            if event.type == KEYUP:
                key_up(event, player1, player2)

        # write game logic here
        if check_collision(ball, player1, player2):
            ball.bounce()

        # draw the game court
        draw_court()

        # sprite draw code here
        ball.draw()
        player1.draw()
        player2.draw()
        player1.update()
        player2.update()
        ball.update()

        # display whatever is drawn
        pygame.display.update()

        # run at pre-set fps
        clock.tick(config.FPS)

if __name__ == '__main__':
    main()
