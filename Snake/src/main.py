import pygame
import random
import sys
import snake as s
import food as f
import os
import sys
# Other imports...

# Get the user's home directory
home_dir = os.path.expanduser("~")
game_data_dir = os.path.join(home_dir, '.snek_game')
os.makedirs(game_data_dir, exist_ok=True)

score_file = os.path.join(game_data_dir, 'score.txt')
if not os.path.exists(score_file):
    with open(score_file, 'w') as file:
        file.write("0\n0\n0")
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
audio_file = os.path.join(base_dir, 'assets', 'audio', 'snekSong.wav')

class Game() :
    def __init__(self) :
        pygame.display.set_caption("Snek")
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.music = pygame.mixer.Sound(audio_file)
        self.music.play(-1)
        self.running = True
        self.playing = True
        
        self.score = 0
        with open(score_file, "r") as file:
                    scores = file.readlines()
                    scores = [int(score) for score in scores]
                    scores.sort(reverse=True)
                    if scores.__len__() > 0 :
                        self.highscore = max(self.score, scores[0])
        
        self.snek = s.Snake(self.screen)
        self.food = f.Food(self.screen, self.snek)
        pygame.time.set_timer(pygame.USEREVENT, 5000)

    def run(self) :
        while self.running :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_z :
                        if(self.snek.direction != "DOWN") :
                            self.snek.direction = "UP"
                    if event.key == pygame.K_s :
                        if(self.snek.direction != "UP") :
                            self.snek.direction = "DOWN"
                    if event.key == pygame.K_q :
                        if(self.snek.direction != "RIGHT") :
                            self.snek.direction = "LEFT"
                    if event.key == pygame.K_d :
                        if(self.snek.direction != "LEFT") :
                            self.snek.direction = "RIGHT"
                if(not self.playing) :
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if buttonYes.collidepoint(event.pos) :
                            self.music.play(-1)
                            pygame.time.set_timer(pygame.USEREVENT, 5000)
                            self.snek.reset()
                            self.fps = 10
                            self.playing = True
                            with open(score_file, "a") as file:
                                file.write(f"\n{int(self.score)}")
                                self.score = 0
                        if buttonDeny.collidepoint(event.pos) :
                            self.running = False
                            with open(score_file, "a") as file:
                                file.write(f"\n{int(self.score)}")
                                
                if event.type == pygame.USEREVENT :
                    self.fps += 2

            if(self.playing) :
                
                if(len(sys.argv) > 1 and sys.argv[1] == "epilepsy") :
                    self.screen.fill((random.randint(0, 230), random.randint(0, 230), random.randint(0, 230)))
                    self.snek.color = (random.randint(0, 230), random.randint(0, 230), random.randint(0, 230))
                else :
                    self.screen.fill((0, 0, 0))
                    
                if(self.score > self.highscore) :
                    self.highscore = self.score
                    
                text = self.font.render("HighScore : " + str(self.highscore), True, (255, 255, 255))
                text_rect = text.get_rect(topleft=(0, 0))
                self.screen.blit(text, text_rect)
                
                text = self.font.render("Score : " + str(self.score), True, (255, 255, 255))
                text_rect = text.get_rect(midtop=(self.screen.get_width() / 2, 0))
                self.screen.blit(text, text_rect)
                
                text = self.font.render("FPS : " + str(self.fps), True, (255, 255, 255))
                text_rect = text.get_rect(topright=(self.screen.get_width(), 0))
                self.screen.blit(text, text_rect)
                
                
                self.food.draw()
                self.snek.draw()
                self.playing = self.snek.move()
                
                if self.food.check_collision() :
                    self.score += int((self.snek.segments.__len__() * self.fps / 2))
                    self.snek.add_segment()
                    self.snek.food_eaten += 1
                    self.snek.color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
                    
                pygame.display.flip()
                
                self.clock.tick(self.fps)
                
            else :
                
                self.music.stop()
                # fill the screen with a color to wipe away anything from last frame
                self.screen.fill("black")
                
                text = self.font.render("LeaderBoard :", True, "white")
                text_rect = text.get_rect(center=(self.screen.get_width() / 2, 40))
                self.screen.blit(text, text_rect)
                
                with open(score_file, "r") as file:
                    scores = file.readlines()
                    scores = [int(score) for score in scores]
                    scores.sort(reverse=True)
                    for i in range(3):
                        text = self.font.render(f"{i + 1} - {scores[i]}", True, "white")
                        text_rect = text.get_rect(center=(self.screen.get_width() / 2, 100 + 70 * i))
                        self.screen.blit(text, text_rect)
                
                
                text = self.font.render("Game Over !", True, "white")
                text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
                self.screen.blit(text, text_rect)

                # Buttons to either stop the game or restart it
                buttonYes = pygame.Rect(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 100, 200, 70)
                pygame.draw.rect(self.screen, "blue", buttonYes)
                text = self.font.render("Play again", True, "white")
                text_rect = text.get_rect(center=buttonYes.center)
                self.screen.blit(text, text_rect)
                
                buttonDeny = pygame.Rect(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 200, 200, 70)
                pygame.draw.rect(self.screen, "red", buttonDeny)
                text = self.font.render("Quit", True, "white")
                text_rect = text.get_rect(center=buttonDeny.center)
                self.screen.blit(text, text_rect)
                
                pygame.display.flip()

        pygame.quit()

if __name__ == "__main__" :
    pygame.init()  
    pygame.mixer.init()
    
    game = Game()
    game.run()