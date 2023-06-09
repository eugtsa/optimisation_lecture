import pygame
from helpers.exceptions import QuitGameException, RetryLevelException
from time import sleep


def press_any_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitGameException()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    raise RetryLevelException()
                if event.key == pygame.K_q:
                    raise QuitGameException()
                return
        sleep(0.05)
