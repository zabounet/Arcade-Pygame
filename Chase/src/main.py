# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
pygame.mixer.init()
grow_sound = pygame.mixer.Sound("audio/grow.mp3")
lose_sound = pygame.mixer.Sound("audio/lose.mp3")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.Font(None, 100)
entity_dimensions = 20
player_dimensions = 40
player_color = "0000FF"
lost = False
player_initial_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player_pos = pygame.Vector2(player_initial_pos)

def RandomPositionX(player_pos):
    min_x = max(100, int(player_pos.x) - 100)
    max_x = min(screen.get_width() - 100, int(player_pos.x) + 100)
    while True:
        rand_x = random.randint(0, screen.get_width() - 100)
        if min_x <= rand_x <= max_x:
            continue
        else:
            return rand_x

def RandomPositionY(player_pos):
    min_y = max(100, int(player_pos.y) - 100)
    max_y = min(screen.get_height() - 100, int(player_pos.y) + 100)
    while True:
        rand_y = random.randint(0, screen.get_height() - 100)
        if min_y <= rand_y <= max_y:
            continue
        else:
            return rand_y

ennemies = [
    {
        'x': RandomPositionX(player_pos),
        'y': RandomPositionY(player_pos),
        'size': entity_dimensions
    }
]
ennemies_speed = 1
score = 0


pygame.time.set_timer(pygame.USEREVENT, 5000)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            pry = RandomPositionY(player_pos)
            prx = RandomPositionX(player_pos)
            size = entity_dimensions
            ennemies.append({'x': prx, 'y': pry, 'size': size})
            if len(ennemies) % 5 == 0:
                ennemies_speed += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttonYes.collidepoint(event.pos):                
                lost = False
            elif buttonDeny.collidepoint(event.pos):
                running = False
                
            with open("score.txt", "a") as file:
                file.write(f"\n{int(score)}")
                score = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_color = f"{random.randint(0, 0xFFFFFF):06x}"
                score += 1
                
    if(not lost):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        
        text = font.render(f"Score : {int(score)}", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() / 2, 50))
        screen.blit(text, text_rect)
        
        score += 1
        # Ennemies logic 
        i = 0
        while i < len(ennemies):
            ennemy = ennemies[i]
            pygame.draw.circle(screen, "red", (ennemy['x'], ennemy['y']), ennemy['size'])
            
            if ennemy['x'] < player_pos.x:
                ennemy['x'] += 100 * dt
            elif ennemy['x'] > player_pos.x:
                ennemy['x'] -= 100 * dt
            if ennemy['y'] < player_pos.y:
                ennemy['y'] += 100 * dt
            elif ennemy['y'] > player_pos.y:
                ennemy['y'] -= 100 * dt
            
            # Prevent ennemies from stacking on top of each other
            for other_ennemy in ennemies:
                if other_ennemy != ennemy:
                    if abs(ennemy['x'] - other_ennemy['x']) < ennemy['size'] + other_ennemy['size']:
                        grow_sound.play()
                        ennemies.remove(other_ennemy)
                        ennemy['size'] += other_ennemy['size']
                        
                        score += 1000
            i += 1
                
            distance = player_pos.distance_to(pygame.Vector2(ennemy['x'], ennemy['y'])) - player_dimensions - ennemy['size']
            if(distance < 1):
                lose_sound.play()
                lost = True
            
        pygame.draw.circle(screen, f"#{player_color}", player_pos, player_dimensions)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and player_pos.y > 0 + player_dimensions:
            player_pos.y -= 350 * dt + 0.01
        if keys[pygame.K_s] and player_pos.y < screen.get_height() - player_dimensions:
            player_pos.y += 350 * dt + 0.01
        if keys[pygame.K_q] and player_pos.x > 0 + player_dimensions:
            player_pos.x -= 350 * dt + 0.01
        if keys[pygame.K_d] and player_pos.x < screen.get_width() - player_dimensions:
            player_pos.x += 350 * dt + 0.01
            
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        
    else:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        
        text = font.render("LeaderBoard :", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() / 2, 40))
        screen.blit(text, text_rect)
        
        with open("score.txt", "r") as file:
            scores = file.readlines()
            scores = [int(score) for score in scores]
            scores.sort(reverse=True)
            for i in range(3):
                text = font.render(f"{i + 1} - {scores[i]}", True, "white")
                text_rect = text.get_rect(center=(screen.get_width() / 2, 100 + 70 * i))
                screen.blit(text, text_rect)
        
        text = font.render("Game Over !", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
        
        text = font.render(f"Score : {int(score)}", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 70))
        screen.blit(text, text_rect)
        
        # Buttons to either stop the game or restart it
        buttonYes = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 100, 200, 70)
        pygame.draw.rect(screen, "blue", buttonYes)
        text = font.render("Yes", True, "white")
        text_rect = text.get_rect(center=buttonYes.center)
        screen.blit(text, text_rect)
        
        buttonDeny = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 200, 200, 70)
        pygame.draw.rect(screen, "red", buttonDeny)
        text = font.render("No", True, "white")
        text_rect = text.get_rect(center=buttonDeny.center)
        screen.blit(text, text_rect)
        
        player_pos = pygame.Vector2(player_initial_pos)
        
        pygame.display.flip()
        
        ennemies = [
            {
                'x': RandomPositionX(player_pos),
                'y': RandomPositionY(player_pos),
                'size': entity_dimensions
            }
        ]
        
        pygame.time.set_timer(pygame.USEREVENT, 5000)
        
pygame.quit()