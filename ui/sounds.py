import pygame

pygame.mixer.init()
play_sounds = False

move_sound = pygame.mixer.Sound('ui/assets/move-self.mp3')
capture_sound = pygame.mixer.Sound('ui/assets/capture.mp3')
throw_dice = pygame.mixer.Sound('ui/assets/dice_throw.mp3')

def play_sound(sound):
    if not play_sounds: return
    sound.play()