import pygame
import os


def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(
        "/home/pytem/Загрузки/zvuk_-monety.mp3")  # Укажи путь к звуковому файлу
    pygame.mixer.music.play()
    pygame.time.delay(
        3000)  # Подожди 5 секунд, чтобы музыка проиграла полностью
