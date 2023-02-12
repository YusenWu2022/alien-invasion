import pygame.font
from ship import Ship
from pygame.sprite import Group
'''绘图的三级结构'''
class Scoreboard():
    def __init__(self,ai_settings,screen,game_stats):
        self.ai_settings=ai_settings
        self.screen=screen
        self.screen_rect=self.screen.get_rect()
        self.stats=game_stats

        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)
        self.prep_score()
        self.prep_level()
        self.prep_high_score()
        self.prep_ships()
        

    def prep_score(self):
        score_str=str(self.stats.score)  #传引用，会同步变化，所以不需要更改self.stats.score就会自动随着stats.score变化
        self.score_image=self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def prep_level(self):
        level_str=str(self.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.screen_rect.right-20
        self.level_rect.top=self.score_rect.bottom+10

    def prep_high_score(self):
        high_score_str=str(self.stats.high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.right=self.screen_rect.centerx
        self.high_score_rect.top=self.screen_rect.top

    def prep_ships(self):
        self.ships=Group()
        for ship_number in range(0,self.stats.ship_left):
            ship=Ship(self.ai_settings,self.screen)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)


    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.ships.draw(self.screen)
        

