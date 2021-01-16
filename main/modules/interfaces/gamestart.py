
import sys
import pygame
from ..sprites import Dinosaur


def GameStartInterface(screen, sounds, cfg):
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])
    ground = pygame.image.load(cfg.IMAGE_PATHS['ground']).subsurface((0, 0), (83, 19))
    rect = ground.get_rect()
    rect.left, rect.bottom = cfg.SCREENSIZE[0]/20, cfg.SCREENSIZE[1]
    clock = pygame.time.Clock()
    press_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    press_flag = True
                    dino.jump(sounds)
        dino.update()
        screen.fill(cfg.BACKGROUND_COLOR)
        screen.blit(ground, rect)
        dino.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)
        if (not dino.is_jumping) and press_flag:
            return True