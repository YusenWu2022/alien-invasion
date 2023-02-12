'''仅供设定常数数值使用,需要重整为动态和静态两组便于管理'''

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_lenth = 600
        self.bg_color = (5, 39, 175)

        self.ship_speed_factor=1.5
        self.ship_limit=2
        
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=255,0,0
        self.bullet_allowed=3

        self.alien_birth_spare=3
        self.alien_points=10

        self.speedup_scale=1.03
        self.level_points=20
        self.initialize_dynamic_settings()

        self.meteorite_speed=0.02
        self.meteorite_points=20
        self.meteorite_birth_level=3

        self.award_speed=0.08

    def initialize_dynamic_settings(self):
        self.alien_speed_factor=0.15
        self.alien_slip_speed_factor=50
        self.alien_birth_per_time=1

    def upgrade_settings(self,level_now):
        self.alien_speed_factor*=self.speedup_scale
        if level_now%2==0:
            self.alien_slip_speed_factor*=self.speedup_scale
        if level_now%4==0:
            self.alien_birth_per_time+=1
        