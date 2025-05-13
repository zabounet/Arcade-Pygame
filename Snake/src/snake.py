import pygame
import time

class Snake():
    def __init__(self, screen):
        # Private attributes
        self.screen = screen
        self.__width = 20
        self.__height = 20
        self.x = (screen.get_width() // 2) // self.__width * self.__width
        self.y = (screen.get_height() // 2) // self.__height * self.__height
        
        # Public attributes
        self.segments = [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.__width, self.y),
            pygame.Vector2(self.x - (self.__width * 2), self.y)
        ]
        self.color = (255, 255, 255)
        self.direction = "RIGHT"
        self.food_eaten = 0

    def move(self):
        if self.direction == "RIGHT":
            self.x += self.__width
        if self.direction == "LEFT":
            self.x -= self.__width
        if self.direction == "UP":
            self.y -= self.__height
        if self.direction == "DOWN":
            self.y += self.__height
            
            
        # self.__x = max(min(self.__x, self.screen.get_width() - self.__width), 0)
        # self.__y = max(min(self.__y, self.screen.get_height() - self.__height), 0)
        
         # Update the positions of the segments
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i] = self.segments[i - 1].copy()
        self.segments[0] = pygame.Vector2(self.x, self.y)


        if(self.x >= self.screen.get_width()
           or self.x < 0
           or self.y >= self.screen.get_height()
           or self.y < 0
        ) :
            return False
        for i in range(1, len(self.segments)) :
            if self.segments[0].x == self.segments[i].x and self.segments[0].y == self.segments[i].y :
                return False
        return True

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.screen, self.color, (segment[0], segment[1], self.__width, self.__height))
            
    def add_segment(self):
        self.segments.append(pygame.Vector2(self.segments[-1].x, self.segments[-1].y))

                
    def reset(self):
        self.x = self.screen.get_width() / 2
        self.y = self.screen.get_height() / 2
        self.segments = [
            pygame.Vector2(self.x, self.y),
            pygame.Vector2(self.x - self.__width, self.y),
            pygame.Vector2(self.x - (self.__width * 2), self.y)
        ]
        self.direction = "RIGHT"