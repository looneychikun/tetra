#! env python
import random
import pygame
from pygame.locals import *
from enum import Enum

from content import shapes, areas

class UPDATE(Enum):
    DROP_CLOCK = 3745

class Tetrar:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.main_font = None
        self.size = self.width, self.height = 800, 600
        
        self.s_play = None
        self.s_preview = None
        self.s_score = None

        self.score = 0
        
        self.g_allblocks = pygame.sprite.Group()

        self.shapes = [
            shapes.L,
            shapes.Square,
            shapes.Line,
            shapes.T,
            shapes.Z,
            shapes.rZ,
            shapes.rL
        ]

        self.drop_clock = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        self.s_play = areas.PlayArea()
        self.s_score = areas.ScoreArea(self)
        self.s_preview = areas.NextArea()
        
        # Set game window Title
        pygame.display.set_caption("Tetrar")
        
        self.p_next = random.choice(self.shapes)(self.s_preview, self.g_allblocks)
        self.p_active = random.choice(self.shapes)(self.s_play, self.g_allblocks)
        # self.p_active = shapes.rZ(self.s_play, self.g_allblocks)

        pygame.time.set_timer(pygame.event.Event(UPDATE.DROP_CLOCK.value), 1000)

        self._running = True

    #region Event Logic
    def on_event(self, event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_s | pygame.K_DOWN:
                        self.p_active.update(shapes.UPDATE.Move, shapes.MOVE.Down)
                    case pygame.K_a | pygame.K_LEFT:
                        self.p_active.update(shapes.UPDATE.Move, shapes.MOVE.Left)
                    case pygame.K_d | pygame.K_RIGHT:
                        self.p_active.update(shapes.UPDATE.Move, shapes.MOVE.Right)
                    case pygame.K_w | pygame.K_UP:
                        self.p_active.rotate()
            case UPDATE.DROP_CLOCK.value:
                self.p_active.update(shapes.UPDATE.Move, shapes.MOVE.Down)
            case pygame.QUIT:
                self._running = False
                
    #endregion
    
    #region Game Logic
    def on_loop(self):
        # Check to see if the active piece is "stuck" to any other game blocks
        for b in self.p_active.blocks:
            if b.check_stuck():
                # Piece has collided, lets add them to all and make a new piece
                self.g_allblocks.add(self.p_active.blocks)
                self.p_active = self.p_next
                self.p_active.new_surf(self.s_play)
                self.p_next = random.choice(self.shapes)(self.s_preview, self.g_allblocks)
                # self.p_active = random.choice(self.shapes)(self.s_play, self.g_allblocks)
                break
        
        # Check to see if the player has completed a line

        # Make a rect that will fit inside a row in the play area
        hitScan = pygame.sprite.Sprite()
        hitScan.rect = pygame.Rect(10, self.s_play.get_rect().bottom + 10, 170, 5)

        # Starting at the bottom check each row for a 9 sprites hit
        lines = []
        for i in range(19):
            hitScan.rect = hitScan.rect.move(0, -20)
            collides = pygame.sprite.spritecollide(hitScan, self.g_allblocks, False)
            if len(collides) == 9:
                lines.append(collides[0].rect.topleft)
                for s in collides:
                    s.die()
        
        # Iterate backwards through the lines and move all sprites above the given line down
        # by one row
        for l in lines[::-1]:
            hitScan.rect = pygame.Rect(0, 0, 180, l[1] - 1)
            collides = pygame.sprite.spritecollide(hitScan, self.g_allblocks, False)
            for s in collides:
                s.move(0, 20)

        if len(lines) == 4:
            # Tetris! Score multiplyer
            self.score += 4300
        self.score += 1000 * len(lines)

    #endregion

    #region Render Logic
    def on_render(self):
        # Screen clear
        self._display_surf.fill((0,0,0))

        # Draw areas
        self._display_surf.blit(self.s_play.draw(), 
                         (self._display_surf.get_rect().centerx - (self.s_play.border.get_width() / 2),
                          self._display_surf.get_rect().centery - self.s_play.border.get_height() / 2)
                          )
        self._display_surf.blit(self.s_score.draw(), 
                         (self._display_surf.get_rect().centerx - (self.s_score.border.get_width() / 2),
                          20)
                          )
        self._display_surf.blit(self.s_preview.draw(), 
                          (150,
                          self._display_surf.get_rect().centery - (self.s_preview.border.get_height() / 2) + 120)
                          )

        # Draw active piece
        #self.g_active.draw(self.s_play)

        # DEBUG: Display hitscan bars
        # hitScan = pygame.sprite.Sprite()
        # hitScan.rect = pygame.Rect(10, self.s_play.get_rect().bottom + 10, 170, 5)
        # for i in range(19):
        #     hitScan.rect = hitScan.rect.move(0, -20)
        #     pygame.draw.rect(self._display_surf, (255, 255, 255), hitScan)

        pygame.display.flip()
    #endregion

    def on_cleanup(self):
        pygame.time.set_timer(pygame.event.Event(UPDATE.DROP_CLOCK.value), 0)
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    TETRAR = Tetrar()
    TETRAR.on_execute()