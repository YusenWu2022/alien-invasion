import pygame
from pygame.sprite import Sprite

class Award(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.ai_settings=ai_settings
        self.screen=screen
        self.image=pygame.image.load("images\\award.bmp")
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.y=float(self.rect.y)
    def update(self):
        self.y+=self.ai_settings.award_speed
        self.rect.y=self.y
    def blitme(self):
        self.screen.blit(self.image,self.rect)