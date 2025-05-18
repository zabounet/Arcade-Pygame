import pygame
import random
import bird as b
import pipe as p
# Other imports...

class Game() :
    def __init__(self) :
        pygame.display.set_caption("Flappy Square")
        self.screen_height, self.screen_width = 720, 1280
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.font = pygame.font.Font("./assets/fonts/scoreFont.ttf", 50)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.playing = False
        self.score = 0
        
        self.bird = b.Bird(self.screen)
        self.dummy_pipe = p.Pipe(self.screen, -100, -100, 0, False)
        
        self.pipes = []
                
    def spawn_pipe(self):
        
        gap_y = random.randint(self.dummy_pipe.min_gap_y, self.dummy_pipe.max_gap_y)
        top_pipe_height = gap_y
        bottom_pipe_height = self.screen_height - (gap_y + self.dummy_pipe.gap_size)

        top_pipe = p.Pipe(self.screen, self.screen_width, 0, top_pipe_height, True)
        bottom_pipe = p.Pipe(self.screen, self.screen_width, gap_y + self.dummy_pipe.gap_size, bottom_pipe_height, False)

        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)

    def run(self) :
        while self.running :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE and self.playing :
                        self.bird.flap()
                    if event.key == pygame.K_RETURN and not self.playing :
                        self.playing = True
                        self.spawn_pipe()
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                if event.type == pygame.USEREVENT :
                    self.spawn_pipe()
                
            self.screen.fill((100, 100, 235))
            self.bird.draw()

            if(self.playing) :
                
                self.bird.fall()
                
                if self.bird.y + self.bird.height > self.screen_height:
                    self.playing = False
                    
                for pipe in self.pipes:
                    pipe.draw()
                    
                    if self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + pipe.width:
                        if pipe.is_top:
                            if self.bird.y < pipe.y + pipe.height:
                                self.playing = False
                        else:
                            if self.bird.y + self.bird.height > pipe.y:
                                self.playing = False
                    
                    if self.bird.x > pipe.x + pipe.width and not pipe.scored and not pipe.is_top :
                        self.score += 1
                        pipe.scored = True
                    
                    pipe.move()

                self.pipes = [pipe for pipe in self.pipes if pipe.x >= -100]
                
                text = self.font.render(str(self.score), True, (0, 0, 0))
                text_rect = text.get_rect(midtop=(self.screen.get_width() / 2, 0))
                self.screen.blit(text, text_rect)
                
            pygame.display.flip()
                
            self.clock.tick(self.fps)
                
        pygame.quit()

if __name__ == "__main__" :
    pygame.init()  
    
    game = Game()
    game.run()