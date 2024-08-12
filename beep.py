import pygame
import os


def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/win31.mp3')  # Укажи путь к звуковому файлу
    pygame.mixer.music.play()
    pygame.time.delay(3000)
