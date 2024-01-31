import pygame
from pygame.locals import *

from enum import Enum

from . import areas

class UPDATE(Enum):
    Move = 0

class MOVE(Enum):
    Down = 0
    Left = 1
    Right = 2

class Block(pygame.sprite.Sprite):
    def __init__(self, color, position, blocks):
        # Parent constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 20))
        self.image.fill((200,200,200))
        pygame.draw.rect(self.image, color, pygame.Rect(2,2,16,16))

        self.rect = self.image.get_rect().move(position)
        self.all_blocks = blocks # This is a bug: this is passed by copy, which means all blocks see the board at the time of creation and get no updates
        self.draw = True

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def collide(self, x, y):
        self.rect = self.rect.move(x, y)
        retval = len(pygame.sprite.spritecollide(self, self.all_blocks, False)) > 0
        self.rect = self.rect.move(-x, -y)
        return retval

    def can_move(self, x, y):
        # Moving Left
        if x < 0:
            # Simple OOB Check
            if self.rect.x < 20:
                return False
            # Piece Collision
            return not self.collide(-20, 0)
        
        # Moving Right
        if x > 0:
            if self.rect.x > 159:
                return False
            return not self.collide(20, 0)
        
        # TODO Check for piece colision
        if y > 0 and self.rect.y > 379:
            return False

        return True

    def die(self):
        self.kill()
        self.image = None
        self.rect = None
        self.draw = False
    
    def check_stuck(self):
        if self.rect.y > 379:
            return True
        self.rect = self.rect.move(0, 20)
        retval = pygame.sprite.spritecollide(self, self.all_blocks, False)
        self.rect = self.rect.move(0,-20)
        return retval        

class _PieceBase(object):
    def __init__(self, s_play, g_allblocks : pygame.sprite.Group):
        self.blocks = []
        self.all_blocks = g_allblocks
        self.surf = s_play
        self.surf.add_piece(self)

    def update(self, type, data):
        match type:
            case UPDATE.Move:
                  match data:
                    case MOVE.Down:
                        for b in self.blocks:
                            if not b.can_move(0, 20):
                                return
                        for b in self.blocks:
                            b.move(0, 20)
                    case MOVE.Left:
                        for b in self.blocks:
                            if not b.can_move(-20, 0):
                                return
                        for b in self.blocks:
                            b.move(-20, 0)
                    case MOVE.Right:
                        for b in self.blocks:
                            if not b.can_move(20, 0):
                                return
                        for b in self.blocks:
                            b.move(20, 0)

    def add(self, x, y):
        self.blocks.append(Block(self.color, (x, y), self.all_blocks))

    def draw(self, surf : pygame.Surface):
        for b in self.blocks:
            if b.draw:
                surf.blit(b.image, b.rect)

    def draw_pos(self, surf : pygame.Surface, coord):
        for b in self.blocks:
            if b.draw:
                surf.blit(b.image, (coord[0] + b.rect.x, coord[1] + b.rect.y))

    def rotate(self):
        pass

    def get_height(self):
        maxy = 0
        for b in self.blocks:
            if b.rect.y > maxy:
                maxy = b.rect.y
        return maxy + 20
    
    def get_width(self):
        maxx = 0
        for b in self.blocks:
            if b.rect.x > maxx:
                maxx = b.rect.x
        return maxx + 20
    
    def new_surf(self, surf):
        self.surf.remove_piece(self)
        self.surf = surf
        self.surf.add_piece(self)

class Square(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (8, 5, 117)
        self.add(0,0)
        self.add(0,20)
        self.add(20,0)
        self.add(20,20)

    def rotate(self):
        pass

class Line(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (105, 18, 86)
        self.add(0,0)
        self.add(0,20)
        self.add(0,40)
        self.add(0,60)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                if(
                    self.blocks[0].collide(0,60) or
                    self.blocks[1].collide(20, 40) or
                    self.blocks[2].collide(40, 20) or
                    self.blocks[3].collide(60, 0)
                ):
                    return
                self.blocks[0].move(0,60)
                self.blocks[1].move(20, 40)
                self.blocks[2].move(40, 20)
                self.blocks[3].move(60, 0)
                self.rotation = 1
            case 1:
                if(
                    self.blocks[0].collide(-0,-60) or
                    self.blocks[1].collide(-20, -40) or
                    self.blocks[2].collide(-40, -20) or
                    self.blocks[3].collide(-60, -0)
                ):
                    return
                self.blocks[0].move(-0, -60)
                self.blocks[1].move(-20, -40)
                self.blocks[2].move(-40, -20)
                self.blocks[3].move(-60, -0)
                self.rotation = 0

class L(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (196, 101, 18)
        self.add(0,0)
        self.add(0,20)
        self.add(0,40)
        self.add(20,40)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                '''
                0   | 210   
                1   | 3
                23  |
                '''
                if (
                    self.blocks[0].collide(40, 0) or 
                    self.blocks[1].collide(20, -20) or 
                    self.blocks[2].collide(0, -40) or 
                    self.blocks[3].collide(-20, -20)
                    ):
                    return
                self.blocks[0].move(40, 0)
                self.blocks[1].move(20, -20)
                self.blocks[2].move(0, -40)
                self.blocks[3].move(-20, -20)
                self.rotation = 1
            case 1:
                '''
                210 | 32  
                3   |  1
                    |  0
                '''
                if (
                    self.blocks[0].collide(-20, 40) or 
                    self.blocks[1].collide(0, 20) or 
                    self.blocks[2].collide(20, 0) or 
                    self.blocks[3].collide(0, -20)
                    ):
                    return
                self.blocks[0].move(-20,40)
                self.blocks[1].move(0,20)
                self.blocks[2].move(20,0)
                self.blocks[3].move(0,-20)
                self.rotation = 2
            case 2:
                '''
                 32 |   3
                  1 | 012 
                  0 |  
                '''
                if (
                    self.blocks[0].collide(-40, 0) or 
                    self.blocks[1].collide(-20, 20) or 
                    self.blocks[2].collide(0, 20) or 
                    self.blocks[3].collide(20, 0)
                    ):
                    return
                self.blocks[0].move(-40,0)
                self.blocks[1].move(-20,20)
                self.blocks[2].move(0,40)
                self.blocks[3].move(20,20)
                self.rotation = 3
            case 3:
                '''
                  3 | 0
                012 | 1
                    | 23
                '''
                if (
                    self.blocks[0].collide(20,-40) or 
                    self.blocks[1].collide(0, -20) or 
                    self.blocks[2].collide(-20, 0) or 
                    self.blocks[3].collide(0, 20)
                    ):
                    return
                self.blocks[0].move(20,-40)
                self.blocks[1].move(0,-20)
                self.blocks[2].move(-20,0)
                self.blocks[3].move(0,20)
                self.rotation = 0

class T(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (3,150,5)
        self.add(20,0)
        self.add(0,20)
        self.add(20,20)
        self.add(40,20)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                if(
                    self.blocks[1].collide(0, -40) or
                    self.blocks[2].collide(-20, -20) or
                    self.blocks[3].collide(-40, 0)
                ):
                    return
                self.blocks[1].move(0, -40)
                self.blocks[2].move(-20, -20)
                self.blocks[3].move(-40, 0)
                self.rotation = 1
            case 1:
                if(
                    self.blocks[1].collide(40, 0) or
                    self.blocks[2].collide(20, -20) or
                    self.blocks[3].collide(0, -40)
                ):
                    return
                self.blocks[1].move(40, 0)
                self.blocks[2].move(20, -20)
                self.blocks[3].move(0, -40)
                self.rotation = 2
            case 2:
                if(
                    self.blocks[1].collide(0, 40) or
                    self.blocks[2].collide(20, 20) or
                    self.blocks[3].collide(40, 0)
                ):
                    return
                self.blocks[1].move(0,40)
                self.blocks[2].move(20, 20)
                self.blocks[3].move(40, 0)
                self.rotation = 3
            case 3:
                if(
                    self.blocks[1].collide(-40, 0) or
                    self.blocks[2].collide(-20, 20) or
                    self.blocks[3].collide(0, 40)
                ):
                    return
                self.blocks[1].move(-40,0)
                self.blocks[2].move(-20, 20)
                self.blocks[3].move(0, 40)
                self.rotation = 0

class Z(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (150,150,3)
        self.add(0,0)
        self.add(20,0)
        self.add(20,20)
        self.add(40,20)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                if(
                    False
                ):
                    return
                self.blocks[0].move(20, 40)
                self.blocks[1].move(20, 0)
                self.rotation = 1
            case 1:
                if(
                    self.blocks[0].collide(0, 20) or
                    self.blocks[3].collide(40, 20)
                ):
                    return
                self.blocks[0].move(-20, -40)
                self.blocks[1].move(-20, 0)
                self.rotation = 0

class rZ(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (146,3,150)
        self.add(20,0)
        self.add(40,0)
        self.add(20,20)
        self.add(0,20)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                if(
                    self.blocks[2].collide(20, 0) or
                    self.blocks[3].collide(20, -40)
                ):
                    return
                self.blocks[2].move(20, 0)
                self.blocks[3].move(20, -40)
                self.rotation = 1
            case 1:
                if(
                    self.blocks[2].collide(-20, 0) or
                    self.blocks[3].collide(-20, 40)
                ):
                    return
                self.blocks[2].move(-20, 0)
                self.blocks[3].move(-20, 40)
                self.rotation = 0

class rL(_PieceBase):
    def __init__(self, s_play : areas.PlayArea, g_allblocks : pygame.sprite.Group):
        _PieceBase.__init__(self, s_play, g_allblocks)

        self.color = (16,20,235)
        self.add(20,0)
        self.add(20,20)
        self.add(20,40)
        self.add(0,40)

        self.rotation = 0

    def rotate(self):
        match self.rotation:
            case 0:
                if (
                    self.blocks[0].collide(20, 40) or 
                    self.blocks[1].collide(0, 20) or 
                    self.blocks[2].collide(-20, 0) or 
                    self.blocks[3].collide(0, -20)
                    ):
                    return
                self.blocks[0].move(20,40)
                self.blocks[1].move(0,20)
                self.blocks[2].move(-20,0)
                self.blocks[3].move(0, -20)
                self.rotation = 1
            case 1:
                if (
                    self.blocks[0].collide(-40, 0) or 
                    self.blocks[1].collide(-20, -20) or 
                    self.blocks[2].collide(0, -40) or 
                    self.blocks[3].collide(20, -20)
                    ):
                    return
                self.blocks[0].move(-40,0)
                self.blocks[1].move(-20,-20)
                self.blocks[2].move(0,-40)
                self.blocks[3].move(20,-20)
                self.rotation = 2
            case 2:
                if (
                    self.blocks[0].collide(0, -40) or 
                    self.blocks[1].collide(20, -20) or 
                    self.blocks[2].collide(40, 0) or 
                    self.blocks[3].collide(20, 20)
                    ):
                    return
                self.blocks[0].move(0,-40)
                self.blocks[1].move(20,-20)
                self.blocks[2].move(40,0)
                self.blocks[3].move(20,20)
                self.rotation = 3
            case 3:
                if (
                    self.blocks[0].collide(40, 0) or 
                    self.blocks[1].collide(20, 20) or 
                    self.blocks[2].collide(0, 40) or 
                    self.blocks[3].collide(-20, 20)
                    ):
                    return
                self.blocks[0].move(40,0)
                self.blocks[1].move(20,20)
                self.blocks[2].move(0,40)
                self.blocks[3].move(-20,20)
                self.rotation = 0
