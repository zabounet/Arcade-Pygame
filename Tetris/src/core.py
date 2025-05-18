import pygame
import random
import pieces as p

def get_random_piece(game_area_rect, screen, pieces) :
    color, shape = random.choice(list(pieces.items()))
    return p.Piece(game_area_rect, screen, color, shape)
        
def will_collide(active_piece, pieces_down):
    for block in active_piece.shape:
        next_y = block.y + active_piece.height
        for landed in pieces_down:
            if block.x == landed["x"] and next_y == landed["y"]:
                return True
    return False

def can_move(shape, dx, pieces_down, game_area_rect):
    for block in shape:
        new_x = block.x + dx
        new_y = block.y

        if not (game_area_rect.left <= new_x < game_area_rect.right and
                game_area_rect.top <= new_y < game_area_rect.bottom):
            return False

        for landed in pieces_down:
            if new_x == landed["x"] and new_y == landed["y"]:
                return False
    return True