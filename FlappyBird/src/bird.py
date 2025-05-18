import pygame
# Other imports...

class Bird() :
    def __init__(self, screen) :
        self.screen = screen
        self.x = 150
        self.y = screen.get_height() // 2
        
        self.height = 40
        self.width = 40
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        self.velocity = 5
        self.gravity = 1
        self.angle = 0
    def draw(self):
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))  # Transparent fill
        # Draw the bird at (0, 0) on its own surface
        pygame.draw.rect(self.surface, "red", (0, 0, self.width, self.height))
        # Rotate the surface
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        # Get the rect for positioning
        rect = rotated_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        # Blit to the screen
        self.screen.blit(rotated_surface, rect.topleft)
        
    def fall(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.angle < 70:
            self.angle += 2
        
    def flap(self):
        self.velocity = -13
        self.angle = -25