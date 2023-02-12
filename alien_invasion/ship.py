import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.screen=screen
        self.image=pygame.image.load('D:\\alien_invasion\\images\\ship.bmp')
        self.screen_rect=screen.get_rect()
        self.rect=self.image.get_rect()
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.move_right=False
        self.move_left=False
        self.ai_settings=ai_settings
        self.centerx_float=float(self.rect.centerx)
        
    def update(self):
        if self.move_right and self.rect.right<self.screen_rect.right:
            self.centerx_float+=self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left>0:
            self.centerx_float-=self.ai_settings.ship_speed_factor
        self.rect.centerx=self.centerx_float
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def center(self):
        self.rect.centerx=self.screen_rect.centerx
