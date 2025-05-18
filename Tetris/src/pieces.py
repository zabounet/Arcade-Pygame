import pygame
import time
import math

class Piece():
    
    SHAPES = {
        "1" : lambda self: [
            pygame.Vector2(self.x + self.width, self.y),
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y),
        ],
        "2" : lambda self: [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - self.width, self.y + self.height),
            pygame.Vector2(self.x, self.y + self.height),
        ],
        "3" : lambda self: [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y + self.height),
        ],
        "4" : lambda self: [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y - self.height),
        ],
        "5" : lambda self: [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - self.width, self.y + self.height),
            pygame.Vector2(self.x - (self.width * 2), self.y + self.height),
        ],
        "6" : lambda self: [
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x, self.y + self.height),
            pygame.Vector2(self.x + self.width , self.y + self.height),
        ],
        "7" : lambda self: [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.width, self.y),
            pygame.Vector2(self.x - (self.width * 2), self.y),
            pygame.Vector2(self.x - self.width, self.y + self.height),
        ],
    }
    
    def __init__(self, rect, screen, color, shape):
        # Private attributes
        self.screen = screen
        self.rect = rect
        self.width = 30
        self.height = 30
        self.x = self.rect.centerx
        self.y = 80
        self.shape = self.SHAPES[shape](self)
        self.color = color

    def draw(self):
        for block in self.shape:
            pygame.draw.rect(self.screen, self.color, (block.x, block.y, self.width, self.height))
        
    def fall(self):
        for block in self.shape:
            block.y += self.height
    
    def move(self, symbol):
        for block in self.shape:
            if symbol == "+":
                block.x += self.width
            else :
                block.x -= self.width
    
    def get_rotated_shape(self):
        pivot = self.shape[0]
        rotated = []
        for block in self.shape:
            rel_x = block.x - pivot.x
            rel_y = block.y - pivot.y
            new_x = -rel_y
            new_y = rel_x
            rotated.append(pygame.Vector2(pivot.x + new_x, pivot.y + new_y))
        return rotated
    
    def rotate(self, game_area_rect):
        pivot = self.shape[0]
        simulated_blocks = []
        for block in self.shape:
            rel_x = block.x - pivot.x
            rel_y = block.y - pivot.y
            new_x = -rel_y
            new_y = rel_x
            sim_x = pivot.x + new_x
            sim_y = pivot.y + new_y
            simulated_blocks.append(pygame.Vector2(sim_x, sim_y))
        # Check if all simulated blocks are in bounds
        if all(
            game_area_rect.left <= block.x < game_area_rect.right and
            game_area_rect.top <= block.y < game_area_rect.bottom
            for block in simulated_blocks
        ):
            # Apply rotation if valid
            for i, block in enumerate(self.shape):
                block.x = simulated_blocks[i].x
                block.y = simulated_blocks[i].y