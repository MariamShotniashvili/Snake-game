# [0.5pt] Forbid 180 degree turns - If the snake is moving upwards and the player presses `S` or `Down Arrow`
# it should not be counted as collision and the snake should continue moving in the initial direction.
# These rules should apply to all 4 directions.

# Start Menu:
# 1. [1pt] Start - Instead of starting the game directly add a button/key for it.
#     For example, Snake should start moving only after space is pressed.
#     In such a case you should also display text to let the player know what to press to start the game.

# Ending Screen
#   1. [1pt] End screen - Instead of closing the application on colliding, display the ending screen.


import random
import time
import pygame

class Snake:
    def __init__(self, screen, radius):
        self.cells = 5
        self.X = [300]*self.cells
        self.Y = [300]*self.cells
        self.direction = "Right"
        self.screen = screen
        self.R = radius

    def renderS(self):
        for i in range(self.cells):
            if i == 0:
                pygame.draw.circle(self.screen, pygame.Color(179, 118, 245), (self.X[i], self.Y[i]), self.R)
            else:
                pygame.draw.circle(self.screen, pygame.Color(84, 5, 168), (self.X[i], self.Y[i]), self.R)

    def move(self):
        for i in range(self.cells - 1, 0, -1):
            self.X[i] = self.X[i-1]
            self.Y[i] = self.Y[i-1]
        if self.direction == "Right":
            self.X[0] += 2*self.R
        if self.direction == "Left":
            self.X[0] -= 2*self.R
        if self.direction == "Up":
            self.Y[0] -= 2*self.R
        if self.direction == "Down":
            self.Y[0] += 2*self.R


    def collide_food(self, x, y):
        return self.X[0] == x and self.Y[0] == y

    def self_collide(self):
        for i in range(1, self.cells):
            if self.X[0] == self.X[i] and self.Y[0] == self.Y[i]:
                return True

    def border_collide(self):
        return self.X[0] <= 0 or self.X[0] >= 1200 or self.Y[0] <= 0 or self.Y[0] >= 700


    def eat_food(self):
        self.cells += 1
        self.X.append(300)
        self.Y.append(800)

class Food:
    def __init__(self, screen):
        self.posX = random.randint(1, 39)*30
        self.posY = random.randint(1, 22)*30
        self.screen = screen

    def renderF(self):
        pygame.draw.circle(self.screen, pygame.Color("red"), (self.posX, self.posY), 12)

    def move_randomly(self):
        self.posX = random.randint(1, 39)*30
        self.posY = random.randint(1, 22)*30

pygame.init()

class App:
    
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.food = None
        self.start = False
        self.end = False

    def run(self):
        while not self.start:
            self.init()
        while self.running:
            self.update()
            self.render()
            time.sleep(0.1)
        while self.end:
            self.cleanUp()
            time.sleep(2.)

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")

        self.screen.fill((201, 235, 52))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 100)

        self.screen.blit(font.render('--Snake--', False, pygame.Color(84, 5, 168)), (340, 150))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 50)

        self.screen.blit(font.render('Press Space to Play!', False, pygame.Color(84, 5, 168)), (340, 350))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.start = True

        if self.start:
            self.clock = pygame.time.Clock()
            self.running = True

            self.snake = Snake(self.screen, 15)
            self.food = Food(self.screen)

    def update(self):
        self.events()
        self.snake.move()

        if self.snake.collide_food(self.food.posX, self.food.posY):
            self.food.move_randomly()
            self.snake.eat_food()

        if self.snake.self_collide():
            pygame.mixer.Sound.play(pygame.mixer.Sound("hit-sound-effect.mp3"))
            self.end = True
            self.running = False

        if self.snake.border_collide():
            pygame.mixer.Sound.play(pygame.mixer.Sound("hit-sound-effect.mp3"))
            time.sleep(0.1)
            self.end = True
            self.running = False


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.snake.direction == "Up" or self.snake.direction == "Down":
                pass
            else:
                self.snake.direction = "Up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.snake.direction == "Up" or self.snake.direction == "Down":
                pass
            else:
                self.snake.direction = "Down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.snake.direction == "Right" or self.snake.direction == "Left":
                pass
            else:
                self.snake.direction = "Left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.snake.direction == "Right" or self.snake.direction == "Left":
                pass
            else:
                self.snake.direction = "Right"


    def render(self):
        self.screen.fill((201, 235, 52))
        self.snake.renderS()
        self.food.renderF()
        pygame.display.flip()
        self.clock.tick(60)


    def cleanUp(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")

        self.screen.fill((201, 235, 52))

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 100)

        self.screen.blit(font.render('Game Over :(', False, pygame.Color(84, 5, 168)), (300, 250))

        pygame.display.flip()

        self.end = False


if __name__ == "__main__":
    app = App()
    app.run()