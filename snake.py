# Copyright 2023 Mark Muriuki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time

import pygame
import random

# Testing code
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Set the size of each block in the grid
BLOCK_SIZE = 20

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the caption of the window
pygame.display.set_caption("Python Xenzia")

# Set up the clock
clock = pygame.time.Clock()


# Define the Snake class
class Snake:
    def __init__(self):
        self.speed = 10
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * BLOCK_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * BLOCK_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed = 10
        self.score = 0
        while True:
            snake = Snake()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            screen.fill(WHITE)
            font = pygame.font.SysFont(None, 48)
            title = font.render("Game Over", True, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(title, title_rect)

            font = pygame.font.SysFont(None, 24)
            score_text = "Your score: " + str(snake.score)
            score = font.render(score_text, True, BLACK)
            score_rect = score.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(score, score_rect)

            instructions = font.render("Press Enter to play again or Esc to quit", True, BLACK)
            instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
            screen.blit(instructions, instructions_rect)

            pygame.display.update()

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)


# Define the Food class
class Food:
    def __init__(self):
        x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
        self.position = (x, y)
        self.color = RED

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)


# Define constants for the directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Define the menu function
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 48)
        title = font.render("Snake Game", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(None, 24)
        instructions1 = font.render("Use the arrow keys to move", True, BLACK)
        instructions1_rect = instructions1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(instructions1, instructions1_rect)

        instructions2 = font.render("Press Enter to start or Esc to quit", True, BLACK)
        instructions2_rect = instructions2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
        screen.blit(instructions2, instructions2_rect)

        pygame.display.update()


# Call the menu function before the game loop
menu()


# Define the game loop function
def game_loop():
    snake = Snake()
    food = Food()

    # Initial snake speed
    speed = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food = Food()
            # Increase speed every 5 points
            if snake.score % 5 == 0:
                speed += 2

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)

        font = pygame.font.SysFont(None, 24)
        score_text = font.render("Score: {}".format(snake.score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        clock.tick(speed)


game_loop()

pygame.quit()
