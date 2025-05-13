import pygame
import sys
import paddle
import ball

class Pong:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.dt = 0
        
        self.playerOneScore = 0
        self.playerTwoScore = 0
        
        self.playerOne = paddle.Paddle(10 ,self.screen)
        self.playerTwo = paddle.Paddle(770, self.screen)
        self.initialPos = self.playerOne.y
        
        self.ball = ball.Ball(self.screen)
        self.service = True

        pygame.display.set_caption("Pong " + str(self.playerOneScore) + " - " + str(self.playerTwoScore))
        
    def run(self):
        while self.running:
            self.events()
            
            if(self.ball.start):
                self.update_ai_paddle()
                
                if(self.ball.rect.colliderect(self.playerOne.x, self.playerOne.y, self.playerOne.width, self.playerOne.height)):
                    self.ball.x_speed *= -1.2
                    
                    self.ball.incline = self.colision_point(self.playerOne, self.ball)
                if(self.ball.rect.colliderect(self.playerTwo.x, self.playerTwo.y, self.playerTwo.width, self.playerTwo.height)):
                    self.ball.x_speed *= -1.2
                    
                    self.ball.incline = self.colision_point(self.playerTwo, self.ball)
                if(self.ball.rect.y < 0 or self.ball.rect.y > self.screen.get_height() - self.ball.rect.height):
                    self.ball.incline *= -1
                    
                if(self.ball.rect.x < 0):
                    self.service = True
                    self.playerTwoScore += 1
                    pygame.time.wait(2000)
                    self.playerOne.y = self.initialPos
                    self.playerTwo.y = self.initialPos      
                elif(self.ball.rect.x > self.screen.get_width()):
                    self.service = True
                    self.playerOneScore += 1
                    pygame.time.wait(2000)
                    self.playerOne.y = self.initialPos
                    self.playerTwo.y = self.initialPos
                    
                if(self.service == True):
                    self.ball.rect.x = self.screen.get_width() / 2
                    self.ball.rect.y = self.screen.get_height() / 2
                    self.ball.incline = 0
                    self.ball.x_speed = 5
                    self.service = False
                    
                self.ball.move()
                pygame.display.set_caption("Pong " + str(self.playerOneScore) + " - " + str(self.playerTwoScore))
            
            self.draw()
            self.dt = self.clock.tick(self.fps)
            
        pygame.quit()
        sys.exit()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ball.start = True
                
        keys = pygame.key.get_pressed()
        self.move(keys)
            
    def move(self, keys):
        if keys[pygame.K_z] and self.playerOne.y > 0:
            self.playerOne.y -= 5
        if keys[pygame.K_x] and self.playerOne.y < self.screen.get_height() - self.playerOne.height:
            self.playerOne.y += 5
        # if keys[pygame.K_UP] and self.playerTwo.y > 0:
        #     self.playerTwo.y -= 5
        # if keys[pygame.K_DOWN] and self.playerTwo.y < self.screen.get_height() - self.playerTwo.height:
        #     self.playerTwo.y += 5
        
    def predict_ball_position(self):
        predicted_x = self.ball.rect.x + self.ball.x_speed * self.dt
        predicted_y = self.ball.rect.y + self.ball.incline * self.dt
        # Account for vertical screen bounds and rebound effect
        screen_height = self.screen.get_height()
        while predicted_y < 0 or predicted_y > screen_height:
            if predicted_y < 0:
                predicted_y = -predicted_y
                # self.ball.incline = -self.ball.incline
            elif predicted_y > screen_height:
                predicted_y = 2*screen_height - predicted_y
                # self.ball.incline = -self.ball.incline
        return predicted_x, predicted_y

    def update_ai_paddle(self):
        screen_width = self.screen.get_width()
        if self.ball.rect.x > screen_width - 75:
            # Si la balle est à moins de 130 pixels du bord droit, se concentrer sur la position actuelle de la balle
            target_y = self.ball.rect.y
        else:
            # Sinon, prédire la position future de la balle
            _, target_y = self.predict_ball_position()

        # Déplacer playerTwo vers la position cible (target_y)
        if self.playerTwo.y + self.playerTwo.height / 2 < target_y:
            self.playerTwo.y += 5
        elif self.playerTwo.y + self.playerTwo.height / 2 > target_y:
            self.playerTwo.y -= 5

        # S'assurer que playerTwo reste dans les limites de l'écran
        self.playerTwo.y = max(0, min(self.playerTwo.y, self.screen.get_height() - self.playerTwo.height))
            
    def colision_point(self, paddle, ball):
        paddle_center_y = paddle.y + paddle.height / 2
        collision_offset = (ball.rect.centery - paddle_center_y) * 0.2
        
        return collision_offset

    def draw(self):
        self.screen.fill((0,0,0))
        self.playerOne.draw(self.screen, (255,0,0))
        self.playerTwo.draw(self.screen, (0,0,255))
        self.ball.draw(self.screen)
        pygame.display.flip()
        
if __name__ == "__main__":
    game = Pong()
    game.run()
    
    
    # Fix bugs
    # Add sound
    # Add AI
    # Add countdown