import sys
import time
import pygame
import scoreboard as sb
from button import Button
from game_stats import Game_stats
from time_control import Clock
from alien import Alien
from pygame.sprite import Group
from ship import Ship
import game_functions as gf
from settings import Settings
from award import Award
from meteorite import Meteorite


def run_game():
    start = Clock()
    pygame.init()
    ai_settings = Settings()
    game_stats = Game_stats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_lenth))
    play_button = Button(ai_settings, screen, 'play')
    ship = Ship(ai_settings, screen)
    scoreboard = sb.Scoreboard(ai_settings, screen, game_stats)
    bullets = Group()
    aliens = Group()
    meteorites = Group()
    awards = Group()
    #gf.create_fleet(ai_settings, screen, aliens, ship)
    while True:
        gf.check_events(ai_settings, screen, ship, bullets,
                        game_stats, play_button, aliens, scoreboard)
        if game_stats.active:
            gf.create_enemies(ai_settings, screen, aliens,
                              start, meteorites, game_stats)
            ship.update()
            gf.update_bullets(bullets, aliens, game_stats,
                              ai_settings, scoreboard, meteorites, awards,screen)
            gf.update_enemies(ai_settings, game_stats, ship, bullets,
                              aliens, screen, scoreboard, meteorites, awards)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens,
                         play_button, game_stats, scoreboard, meteorites, awards)


run_game()
