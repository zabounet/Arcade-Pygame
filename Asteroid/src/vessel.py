import pygame
import math
import projectile as p

class Vessel():
    def __init__(self, screen):
        self.screen = screen

        self.x = screen.get_width() // 2
        self.y = screen.get_height() // 2
        
        self.width = 30
        self.height = 30
        
        self.surface = pygame.Surface((self.width*2, self.height*2), pygame.SRCALPHA)

        self.is_rotating = False
        self.is_moving = False
        
        self.angle = 0
        
        self.move_velocity = 0
        self.max_move_velocity = 8
        self.move_acceleration = 1
        self.move_deceleration = 1
        
        self.rotation_velocity = 0
        self.max_rotation_velocity = 6
        self.rotation_acceleration = 0.5
        self.rotation_deceleration = 1
        
        self.polygon = [
                (self.width, self.height - self.height // 2),
                (self.width - self.width // 2, self.height + self.height // 2),
                (self.width, self.height + self.height // 4),
                (self.width + self.width // 2, self.height + self.height // 2),
            ]
        
    def draw(self):
        self.surface.fill((0, 0, 0, 0)) 
        
        pygame.draw.polygon(
            self.surface,
            "white",
            self.polygon
        )
    
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        self.screen.blit(rotated_surface, rect.topleft)
        
    def turn(self, dx):
        self.is_rotating = True
        self.turn_direction = dx
    
    def update(self):
        # Rotation inertia
        if self.is_rotating and not self.is_moving:
            if self.rotation_velocity < self.max_rotation_velocity:
                self.rotation_velocity += self.rotation_acceleration
        else:
            if self.rotation_velocity > 0:
                self.rotation_velocity -= self.rotation_deceleration
            if self.rotation_velocity < 0:
                self.rotation_velocity = 0

        if self.rotation_velocity > 0:
            self.angle += self.rotation_velocity * self.turn_direction

        # Movement inertia
        if self.is_moving:
            if self.move_velocity < self.max_move_velocity:
                self.move_velocity += self.move_acceleration
        else:
            if self.move_velocity > 0:
                self.move_velocity -= self.move_deceleration
            if self.move_velocity < 0:
                self.move_velocity = 0

        self.x += math.cos(math.radians(self.angle + 90)) * self.move_velocity
        self.y += math.sin(math.radians(self.angle - 90)) * self.move_velocity
    
    def stop_turn(self):
        self.is_rotating = False

    def shoot(self):
        tip_length = self.height // 2  # Distance from center to tip
        tip_x = self.x + math.cos(math.radians(self.angle + 90)) * tip_length
        tip_y = self.y + math.sin(math.radians(self.angle - 90)) * tip_length
        return p.Projectile(tip_x, tip_y, self.angle, self.screen)