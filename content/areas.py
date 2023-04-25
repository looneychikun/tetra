import pygame
from pygame.locals import *

class PlayArea(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, (180, 400))
        self.border = pygame.Surface((190, 410))
        self.border.fill((255,255,255))
        self.fill((0,0,0))
        self.groups = []

    def draw(self):
        self.fill((0,0,0))
        for g in self.groups:
            g.draw(self)


        self.border.blit(self, (5,5))
        return self.border
    
    def add_piece(self, new_piece):
        self.groups.append(new_piece)
    
    def remove_piece(self, old_piece):
        self.groups.remove(old_piece)


class ScoreArea(pygame.Surface):
    def __init__(self, tetrar):
        pygame.Surface.__init__(self, (200, 50))
        self.border = pygame.Surface((210, 60))
        self.border.fill((255,255,255))
        self.fill((0,0,0))
        self.font = pygame.font.SysFont('Consolas', 30)
        self.tetrar = tetrar

    def draw(self):
        self.fill((0,0,0))
        text = self.font.render(f'{self.tetrar.score:011,}', True, (200, 200, 200))
        self.blit(text, (100 - text.get_width() / 2, 25 - text.get_height() / 2))


        self.border.blit(self, (5,5))
        return self.border
    
    def add_piece(self, new_piece):
        self.groups.append(new_piece)

class NextArea(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, (100, 100))
        self.border = pygame.Surface((110, 110))
        self.border.fill((255,255,255))
        self.fill((0,0,0))
        self.piece = None

    def draw(self):
        self.fill((0,0,0))
        if self.piece:
            self.piece.draw_pos(self, (50 - self.piece.get_width() / 2, 50 - self.piece.get_height() / 2))


        self.border.blit(self, (5,5))
        return self.border
    
    def add_piece(self, new_piece):
        self.piece = new_piece

    def remove_piece(self, old_piece):
        self.piece = None