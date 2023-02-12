import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()                        #一定要记得初始化父类！！！！不然会报错没有sprite相关函数！！！
        self.ai_settings=ai_settings
        self.screen=screen
        self.image=pygame.image.load("D:\\alien_invasion\\images\\alien.bmp")
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x=float(self.rect.x)
        self.direction=1

    def update(self):
        self.x+=self.ai_settings.alien_speed_factor*self.direction
        self.rect.x=self.x
        screen_rect=self.screen.get_rect()
        #if self.rect.right>=screen_rect.right or self.rect.left<=0: 导致一次跳好几下
        if self.x>=screen_rect.right or self.x<=0:
            self.rect.y+=self.ai_settings.alien_slip_speed_factor
            self.direction*=-1

    def blitme(self):
        self.screen.blit(self.image,self.rect)