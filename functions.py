import pygame as pg

def music_player(path):

    # Loading the music
    pg.mixer.music.load(path)
    
    # Playing the music forever
    player = pg.mixer.music.play(loops=-1, fade_ms=5)
    
    return player