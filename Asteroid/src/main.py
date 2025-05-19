import pygame
import random
import vessel as v
import asteroid as a
import projectile as p
# Other imports...

class Game() :
    def __init__(self) :
        pygame.display.set_caption("Asteroid")
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        self.playing = True

        self.score = 0
        
        pygame.key.set_repeat(100)

        self.vessel = v.Vessel(self.screen)
        self.asteroids = []
        self.projectile = None
        
        pygame.time.set_timer(pygame.USEREVENT, 2000)

    def random_spawn_coords(self, screen_width, screen_height, margin=150) :
        border = random.choice(['left', 'right', 'top', 'bottom'])
        if border == 'left':
            x = -margin
            y = random.randint(0, screen_height)
        elif border == 'right':
            x = screen_width + margin
            y = random.randint(0, screen_height)
        elif border == 'top':
            x = random.randint(0, screen_width)
            y = -margin
        else: 
            x = random.randint(0, screen_width)
            y = screen_height + margin
        return x, y
    
    def split_asteroid(self, asteroid) :
        self.asteroids.append(a.Asteroid(self.screen, 
                              random.randint(asteroid.x - 50, asteroid.x + 50), 
                              random.randint(asteroid.y - 50, asteroid.y + 50),
                              asteroid.width//2,
                              asteroid.height//2,
                              asteroid.speed + 1,
                              asteroid.break_counter))

        self.asteroids.append(a.Asteroid(self.screen, 
                              random.randint(asteroid.x - 50, asteroid.x + 50), 
                              random.randint(asteroid.y - 50, asteroid.y + 50),
                              asteroid.width//2,
                              asteroid.height//2,
                              asteroid.speed + 1,
                              asteroid.break_counter))

    def run(self) :
        while self.running :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_UP :
                        self.vessel.is_moving = True
                    if event.key == pygame.K_RIGHT :
                        self.vessel.turn(-1)
                    if event.key == pygame.K_LEFT :
                        self.vessel.turn(1)
                    if event.key == pygame.K_SPACE and self.projectile == None :
                        self.projectile = self.vessel.shoot()
                        
                if event.type == pygame.KEYUP :
                    if event.key == pygame.K_UP :
                        self.vessel.is_moving = False
                    if event.key == pygame.K_RIGHT :
                        self.vessel.stop_turn()
                    if event.key == pygame.K_LEFT :
                        self.vessel.stop_turn()
                if event.type == pygame.USEREVENT :
                    x, y = self.random_spawn_coords(self.screen.get_width(), self.screen.get_height(), 150)
                    self.asteroids.append(a.Asteroid(self.screen, x, y, 100, 100, 2, 0))

            if(self.playing) :
                
                self.screen.fill((0, 0, 0))
                self.vessel.draw()
                self.vessel.update()
                
                text = self.font.render("Score : " + str(self.score), True, (255, 128, 0))
                text_rect = text.get_rect(midtop=(self.screen.get_width() / 2, 20))
                self.screen.blit(text, text_rect)

                for asteroid in self.asteroids :
                    asteroid.draw()
                    asteroid.update()
                    if(
                        asteroid.x + asteroid.width > self.vessel.x >= asteroid.x - asteroid.width
                        and asteroid.y + asteroid.height > self.vessel.y >= asteroid.y - asteroid.height
                    ):
                        self.running = False

                if self.projectile != None :
                    self.projectile.draw()
                    self.projectile.update()
                    
                    for i,asteroid in enumerate(self.asteroids) :
                        if(
                            asteroid.x + asteroid.width > self.projectile.x >= asteroid.x - asteroid.width
                            and asteroid.y + asteroid.height > self.projectile.y >= asteroid.y - asteroid.height
                        ):
                            asteroid.break_counter += 1
                            
                            if asteroid.break_counter == 1 :
                                self.score += 10
                                self.split_asteroid(asteroid)
                                del self.asteroids[i]
                            if asteroid.break_counter == 2 :
                                self.score += 25
                                self.split_asteroid(asteroid)
                                del self.asteroids[i]
                            if asteroid.break_counter == 3 :
                                self.score += 50
                                del self.asteroids[i]

                            self.projectile = None
                            break
                    if (
                        not self.projectile == None and
                        (self.projectile.x < -100 or self.projectile.x > self.screen.get_width() + 100 or
                        self.projectile.y < -100 or self.projectile.y > self.screen.get_height() + 100) 
                    ):
                        self.projectile = None

                pygame.display.flip()

                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__" :
    pygame.init()  
    
    game = Game()
    game.run()