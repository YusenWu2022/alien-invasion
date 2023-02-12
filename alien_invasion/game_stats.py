def read_high_score(filepath):
    high_score=0
    with open(filepath) as obj:
        high_score=int(obj.read())
    return high_score
    
class Game_stats():
    def __init__(self,ai_settings):
        self.ai_settings=ai_settings
        self.reset_stats()
        self.active=False
        self.high_score=read_high_score('data\\data.txt')
    
    def reset_stats(self):
        self.ship_left=self.ai_settings.ship_limit
        self.active=True
        self.meteorite_birth=False
        self.score=0
        self.level=1
