import pygame
import random

CAPTION = "Runner2"
SCREEN_SIZE = (1200, 600)
BACKGROUND_COLOR = (0,0,0)
CEILING_HEIGHT = 150
FLOOR_HEIGHT = SCREEN_SIZE[1]-150

SET_PIECE1 = {
    (SCREEN_SIZE[0], CEILING_HEIGHT, 32, 150),
    (SCREEN_SIZE[0]+300, FLOOR_HEIGHT-150, 32, 150),
    (SCREEN_SIZE[0]+600, CEILING_HEIGHT, 32, 150)
}

SET_PIECE2 = {
        (SCREEN_SIZE[0], FLOOR_HEIGHT-150, 32, 150),
        (SCREEN_SIZE[0]+32, CEILING_HEIGHT, 32, 150)
}

class Wall:


    def __init__(self, x_pos, y_pos, width, height):
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.x_pos = x_pos
        self.color = (0, 0, 0)
        self.solid = True
        self.falling_down = False
        self.falling_up = False

    def update(self, speed):
        self.x_pos -= speed
        self.rect.x = self.x_pos

        if self.solid:
            self.color = (0,0,0)
        else:
            self.color = (250,250,0)

        if self.falling_down:
            self.rect.y += 5
        if self.falling_up:
            self.rect.y -= 5

        if self.rect.y > FLOOR_HEIGHT-150:
            self.falling_down = False
            self.rect.y = FLOOR_HEIGHT-150
        if self.rect.y < CEILING_HEIGHT:
            self.falling_up = False
            self.rect.y = CEILING_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Bullet:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def update(self):
        self.x_pos += 10

    def draw(self, surface):
        pygame.draw.line(surface, (250, 250, 0), (self.x_pos, self.y_pos), 
                (self.x_pos-30, self.y_pos))

class Player:

    def __init__(self):
        self.image = pygame.image.load('src/player.png')
        self.rect = pygame.Rect(100, 150, 32, 32)
        self.going_left = False
        self.going_right = False
        self.in_air = True
        self.upside_down = False
        self.invincibility = 0

    def update(self):

        if self.going_right:
            self.rect.x += 1 
        if self.going_left:
            self.rect.x -= 1
        if self.rect.x > SCREEN_SIZE[0]-32:
            self.rect.x = SCREEN_SIZE[0]-32
        if self.rect.x < 0:
            self.rect.x = 0 

        if self.in_air and self.upside_down:
            self.rect.y -= 5
        elif self.in_air and not self.upside_down:
            self.rect.y += 5

        if (self.upside_down and self.rect.y < CEILING_HEIGHT):
            self.in_air = False
            self.rect.y = CEILING_HEIGHT

        if (not self.upside_down and self.rect.y > FLOOR_HEIGHT-32):
            self.in_air = False
            self.rect.y = FLOOR_HEIGHT-32

        if self.invincibility > 0:
            self.invincibility -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Runner2():
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.player = Player()
        self.walls = []
        self.bullets = []
        self.speed = 0.5 
        self.game_time = 0
        self.set_pieces = [SET_PIECE1, SET_PIECE2]

    def play_game(self):
        while not self.done:
            self.key_presses()
            self.update()
            self.draw()
            self.speed += .0001
            if len(self.walls) == 0:
                i = random.randint(0, len(self.set_pieces)-1)
                for wall in self.set_pieces[i]:
                    self.walls.append(Wall(wall[0], wall[1], wall[2], wall[3]))
            self.game_time += 1


    def key_presses(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_RIGHT:
                    self.player.going_right = True
                    self.player.going_left = False
                if event.key == pygame.K_LEFT:
                    self.player.going_left = True
                    self.player.going_right = False
                if event.key == pygame.K_LSHIFT and not self.player.in_air:
                    self.player.upside_down = not self.player.upside_down
                    self.player.in_air = True
                    for wall in self.walls:
                        if not wall.solid and not self.player.upside_down:
                            wall.falling_down = True
                            wall.solid = True
                        if not wall.solid and self.player.upside_down:
                            wall.falling_up = True
                            wall.solid = True
                if event.key == pygame.K_z:
                    self.bullets.append(Bullet(self.player.rect.x+30, self.player.rect.y+16))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.going_right = False
                if event.key == pygame.K_LEFT:
                    self.player.going_left = False

    def update(self):
        self.player.update()
 
        for bullet in self.bullets:
            if bullet.x_pos > SCREEN_SIZE[0]:
                self.bullets.remove(bullet)
            else:
                bullet.update()

        for wall in self.walls:
            if wall.rect.x < -100:
                self.walls.remove(wall)
            else:
                wall.update(self.speed)
                if wall.rect.colliderect(self.player.rect) and self.player.invincibility == 0:
                    self.speed -= .5
                    self.player.invincibility = 500
                for bullet in self.bullets:
                    if (wall.rect.collidepoint(bullet.x_pos, bullet.y_pos) or
                       wall.rect.collidepoint(bullet.x_pos-32, bullet.y_pos)):
                        wall.solid = not wall.solid
                        self.bullets.remove(bullet)

        if self.speed < .5:
            self.speed = .5

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, (100, 100, 250), pygame.Rect(0, 150, 1200, 300))
        for wall in self.walls:
            wall.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE)
    game_instance = Runner2()
    game_instance.play_game()
    pygame.quit()
