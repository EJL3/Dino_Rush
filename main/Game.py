
import core
import sys
import random
import pygame
from modules import *


def main(highest_score):

    pygame.init()
    screen = pygame.display.set_mode(core.SCREENSIZE)
    pygame.display.set_caption('By Rizwan.AR')

    sounds = {}
    for key, value in core.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)

    GameStartInterface(screen, sounds, core)

    score = 0
    score_board = Scoreboard(core.IMAGE_PATHS['numbers'], position=(534, 15), bg_color=core.BACKGROUND_COLOR)
    highest_score = highest_score
    highest_score_board = Scoreboard(core.IMAGE_PATHS['numbers'], position=(435, 15), bg_color=core.BACKGROUND_COLOR, is_highest=True)
    dino = Dinosaur(core.IMAGE_PATHS['dino'])
    ground = Ground(core.IMAGE_PATHS['ground'], position=(0, core.SCREENSIZE[1]))
    cloud_sprites_group = pygame.sprite.Group()
    cactus_sprites_group = pygame.sprite.Group()
    ptera_sprites_group = pygame.sprite.Group()
    add_obstacle_timer = 0
    score_timer = 0

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()
        screen.fill(core.BACKGROUND_COLOR)

        if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
            cloud_sprites_group.add(Cloud(core.IMAGE_PATHS['cloud'], position=(core.SCREENSIZE[0], random.randrange(30, 75))))

        add_obstacle_timer += 1
        if add_obstacle_timer > random.randrange(50, 150):
            add_obstacle_timer = 0
            random_value = random.randrange(0, 10)
            if random_value >= 5 and random_value <= 7:
                cactus_sprites_group.add(Cactus(core.IMAGE_PATHS['cacti']))
            else:
                position_ys = [core.SCREENSIZE[1]*0.82, core.SCREENSIZE[1]*0.75, core.SCREENSIZE[1]*0.60, core.SCREENSIZE[1]*0.20]
                ptera_sprites_group.add(Ptera(core.IMAGE_PATHS['ptera'], position=(600, random.choice(position_ys))))

        dino.update()
        ground.update()
        cloud_sprites_group.update()
        cactus_sprites_group.update()
        ptera_sprites_group.update()
        score_timer += 1
        if score_timer > (core.FPS//12):
            score_timer = 0
            score += 1
            score = min(score, 99999)
            if score > highest_score:
                highest_score = score
            if score % 100 == 0:
                sounds['point'].play()
            if score % 1000 == 0:
                ground.speed -= 1
                for item in cloud_sprites_group:
                    item.speed -= 1
                for item in cactus_sprites_group:
                    item.speed -= 1
                for item in ptera_sprites_group:
                    item.speed -= 1

        for item in cactus_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in ptera_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)

        dino.draw(screen)
        ground.draw(screen)
        cloud_sprites_group.draw(screen)
        cactus_sprites_group.draw(screen)
        ptera_sprites_group.draw(screen)
        score_board.set(score)
        highest_score_board.set(highest_score)
        score_board.draw(screen)
        highest_score_board.draw(screen)

        pygame.display.update()
        clock.tick(core.FPS)

        if dino.is_dead:
            break

    return GameEndInterface(screen, core), highest_score


if __name__ == '__main__':
    highest_score = 0
    while True:
        flag, highest_score = main(highest_score)
        if not flag: break
