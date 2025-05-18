import pygame
import random
import math
import pieces as p
import core
# Other imports...

class Game() :
    def __init__(self) :
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((720, 940))
        self.music = pygame.mixer.Sound("./assets/audio/TetrisMusic.wav")
        self.line_break_sound = pygame.mixer.Sound("./assets/audio/LineDeletion.wav")
        
        self.border_thickness = 2
        self.game_area = pygame.Rect(20, 20, 480, 900)
        self.border_rect = pygame.Rect(
            self.game_area.left - self.border_thickness,
            self.game_area.top - self.border_thickness,
            self.game_area.width + 2 * self.border_thickness,
            self.game_area.height + 2 * self.border_thickness
        )
        
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.fps = 4
        # pygame.key.set_repeat(1000)
        self.running = True
        self.playing = False
        self.game_over = False
        
        self.score = 0
        self.total_lines = 0
        self.treshold = 6
        
        self.landed = False 
        self.pieces = {
            "green" : "1",
            "red" : "2",
            "blue" : "3",
            "purple" : "4",
            "orange" : "5",
            "cyan" : "6",
            "pink" : "7"
        }
        
        self.pieces_down = []
        self.active_piece = core.get_random_piece(self.game_area, self.screen, self.pieces)
        self.next_piece = core.get_random_piece(self.game_area, self.screen, self.pieces)
    
    def run(self) :
        while self.running :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_RETURN and not self.game_over and not self.playing:
                        self.playing = True
                        self.music.play(-1)
                        
                    if self.playing :
                        if event.key == pygame.K_SPACE:
                            rotated_shape = self.active_piece.get_rotated_shape()
                            
                            if core.can_move(rotated_shape, 0, self.pieces_down, self.game_area):
                                self.active_piece.rotate(self.game_area)
                            
                        if event.key == pygame.K_d:
                            if core.can_move(self.active_piece.shape, self.active_piece.width, self.pieces_down, self.game_area):
                                self.active_piece.move("+")
                                
                        if event.key == pygame.K_q:
                            if core.can_move(self.active_piece.shape, -self.active_piece.width, self.pieces_down, self.game_area):
                                self.active_piece.move("-")
                                
                        if event.key == pygame.K_s:
                            self.fps = self.fps*3
                            
                if event.type == pygame.KEYUP and self.playing:
                    if event.key == pygame.K_s   :
                        self.fps = self.fps/3
                
            self.screen.fill("black")
            pygame.draw.rect(self.screen, "white", self.border_rect)
            pygame.draw.rect(self.screen, "black", self.game_area)
            self.active_piece.draw()
            
            if self.playing :
                
                for block in self.pieces_down :
                    pygame.draw.rect(self.screen, block["color"], (block["x"], block["y"], self.active_piece.width, self.active_piece.height))
                    
                for block in self.next_piece.shape :
                    pygame.draw.rect(self.screen, self.next_piece.color, (block.x + 350, block.y + 50, self.next_piece.width, self.next_piece.height))
                
                text = self.font.render("NEXT", True, (255, 255, 255))
                text_rect = text.get_rect(midtop=(self.screen.get_width() - 120, 50))
                self.screen.blit(text, text_rect)
                
                text = self.font.render("Score", True, (255, 255, 255))
                text_rect = text.get_rect(midtop=(self.screen.get_width() - 120, self.screen.get_height() / 2))
                self.screen.blit(text, text_rect)
                
                text = self.font.render(str(self.score), True, (255, 255, 255))
                text_rect = text.get_rect(midtop=(self.screen.get_width() - 120, self.screen.get_height() / 2 + 50))
                self.screen.blit(text, text_rect)
                
                for block in self.active_piece.shape:
                    if block.y + self.active_piece.height >= self.game_area.bottom or core.will_collide(self.active_piece, self.pieces_down):
                        self.landed = True
                        break
                
                
                if self.landed :
                    for block in self.active_piece.shape:
                        self.pieces_down.append({
                            "x": block.x,
                            "y": block.y,
                            "color": self.active_piece.color
                        })
                    
                    rows = {}  # y-coordinate : count

                    # Count blocks per row
                    for block in self.pieces_down:
                        y = block["y"]
                        rows[y] = rows.get(y, 0) + 1

                    # Find full lines
                    full_lines = [y for y, count in rows.items() if count == self.game_area.width // self.active_piece.width]

                    if full_lines:
                        self.line_break_sound.play(1)
                        # Remove blocks in full lines
                        self.pieces_down = [block for block in self.pieces_down if block["y"] not in full_lines]
                        # Move blocks above down
                        for y in sorted(full_lines):
                            for block in self.pieces_down:
                                if block["y"] < y:
                                    block["y"] += self.active_piece.height
                        
                        points = 0
                        if len(full_lines) == 1:
                            points += 200
                            self.total_lines += 1
                        elif len(full_lines) == 2:
                            points += 400
                            self.total_lines += 2
                        elif len(full_lines) == 3:
                            points += 800
                            self.total_lines += 3
                        elif len(full_lines) == 4:
                            points += 1600
                            self.total_lines += 4

                        if not self.pieces_down and len(full_lines) > 2:
                            self.score += points * (points/50)
                        else:
                            self.score += points

                        if self.total_lines <= self.treshold:
                            self.fps += 3
                            self.treshold += 6
                        
                    self.game_over = any(
                        block["y"] <= 80 + self.active_piece.width and
                        (self.game_area.centerx == block["x"])
                        for block in self.pieces_down
                    )
                        
                    if self.game_over:
                        self.music.stop()
                        self.playing = False
                        while any(block["y"] < self.game_area.bottom - self.active_piece.height for block in self.pieces_down):
                            for block in self.pieces_down:
                                if block["y"] < self.game_area.bottom - self.active_piece.height:
                                    block["y"] += self.active_piece.height
                                else:
                                    block["y"] = self.game_area.bottom - self.active_piece.height
                            self.screen.fill("black")
                            pygame.draw.rect(self.screen, "white", self.border_rect)
                            pygame.draw.rect(self.screen, "black", self.game_area)
                            for block in self.pieces_down:
                                pygame.draw.rect(self.screen, block["color"], (block["x"], block["y"], self.active_piece.width, self.active_piece.height))
                            pygame.display.flip()
                            self.line_break_sound.play(1)
                            pygame.time.wait(100)
                        self.pieces_down.clear()
                        
                        self.running = False # ! Temporary

                    self.active_piece = self.next_piece
                    self.next_piece = core.get_random_piece(self.game_area, self.screen, self.pieces)
                    self.landed = False
                        
                self.active_piece.fall()
            
            if self.game_over:
                pass
            
            pygame.display.flip()
            self.clock.tick_busy_loop(self.fps)
            
        pygame.quit()
        exit()

if __name__ == "__main__" :
    pygame.init()  
    pygame.mixer.init()
    
    game = Game()
    game.run()
    
    # ? Add Main menu
    # ? Add LeaderBoard
    # ? Add Music
    # ? Add Executable
    # ? Add Game Over
    # ? Add small delay before piece landing is taken to account (not sure because the unforgiveness of the game currently is fun)