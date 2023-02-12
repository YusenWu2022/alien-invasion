import sys
import time
from time import sleep
import random
import pygame
from button import Button
from game_stats import Game_stats
from time_control import Clock
from pygame.sprite import Group
from alien import Alien
from bullet import Bullet
from award import Award
from meteorite import Meteorite

def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def quit(high_score):
    with open('data\data.txt','w') as obj:
        obj.write(str(high_score))
    sys.exit()

def check_keydown_events(ai_settings, screen, ship, bullets, event,game_stats):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key==pygame.K_q:
        quit(game_stats.high_score)


def check_keyup_events(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False


def check_play_button(mouse_x,mouse_y,play_button,game_stats,ship,bullets,aliens,ai_settings,scoreboard):
    if play_button.rect.collidepoint(mouse_x,mouse_y) and game_stats.active==False:
        game_stats.reset_stats()
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        aliens.empty()
        bullets.empty()
        ship.center()
        scoreboard.prep_level()
        scoreboard.prep_score()
        scoreboard.prep_ships()

def check_events(ai_settings, screen, ship, bullets,game_stats,play_button,aliens,scoreboard):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(game_stats.high_score)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings, screen, ship, bullets, event,game_stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(mouse_x,mouse_y,play_button,game_stats,ship,bullets,aliens,ai_settings,scoreboard)


def update_screen(ai_settings, screen, ship, bullets,aliens,play_button,game_stats,scoreboard,meteorites,awards):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    awards.draw(screen)
    aliens.draw(screen)
    meteorites.draw(screen)
    scoreboard.show_score()
    if game_stats.active==False:
        play_button.draw_button()
    pygame.display.flip()

def create_one_award(ai_settings,screen,awards):
    award=Award(ai_settings,screen)
    award.x=random.random()*(ai_settings.screen_width-10)+5
    award.rect.x=award.x
    award.rect.y=award.rect.height*2
    awards.add(award)

def check_upgrade(ai_settings,game_stats,scoreboard,awards,screen):
    if game_stats.score%ai_settings.level_points==0 and game_stats.score!=0:
        game_stats.level+=1
        if game_stats.level>=ai_settings.meteorite_birth_level:
            game_stats.meteorite_birth=True
        ai_settings.upgrade_settings(game_stats.level)
        scoreboard.prep_level()
        create_one_award(ai_settings,screen,awards)

def check_high_score(game_stats,scoreboard):
    if game_stats.score>game_stats.high_score:
        game_stats.high_score=game_stats.score
        scoreboard.prep_high_score()

def check_aliens_bullets_collide(bullets,aliens,game_stats,ai_settings,scoreboard,awards,screen):
    collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)#击中外星人的子弹会穿过
    if collisions:
        for aliens in collisions.values():
            game_stats.score+=ai_settings.alien_points*len(aliens)
            check_high_score(game_stats,scoreboard)
            scoreboard.stats.score=game_stats.score#无用语句，因为本来就是引用，会随之变化
            scoreboard.prep_score()
        check_upgrade(ai_settings,game_stats,scoreboard,awards,screen)
    
def check_meteorites_bullets_collide(bullets,meteorites,game_stats,ai_settings,scoreboard,awards,screen):
    collisions=pygame.sprite.groupcollide(bullets,meteorites,True,True) #击中陨石的子弹会损失
    if collisions:
        for meteorites in collisions.values():
            game_stats.score+=ai_settings.meteorite_points*len(meteorites)
            check_high_score(game_stats,scoreboard)
            scoreboard.stats.score=game_stats.score
            scoreboard.prep_score()
        check_upgrade(ai_settings,game_stats,scoreboard,awards,screen)


def update_bullets(bullets,aliens,game_stats,ai_settings,scoreboard,meteorites,awards,screen):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_aliens_bullets_collide(bullets,aliens,game_stats,ai_settings,scoreboard,awards,screen)
    check_meteorites_bullets_collide(bullets,meteorites,game_stats,ai_settings,scoreboard,awards,screen)
    

def ship_hit(ai_settings,game_stats,ship,bullets,aliens,screen,scoreboard,meteorites):
    game_stats.ship_left-=1
    scoreboard.prep_ships()
    if game_stats.ship_left<=0:
        game_stats.active=False
        pygame.mouse.set_visible(True)
    meteorites.empty()
    aliens.empty()
    bullets.empty()
    ship.center()
    sleep(0.5)

def check_aliens_bottom(aliens,screen):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            return True
    return False

def check_meteorites_bottom(meteorites,screen):
    screen_rect=screen.get_rect()
    for meteorite in meteorites.sprites():
        if meteorite.rect.bottom>=screen_rect.bottom:
            return True
    return False

def check_awards_bottom(awards,screen):
    screen_rect=screen.get_rect()
    for award in awards.sprites():
        if award.rect.bottom>=screen_rect.bottom:
            awards.remove(award)

def check_awards_ship_collide(ai_settings,game_stats,ship,bullets,aliens,screen,scoreboard,meteorites,awards):
    if pygame.sprite.spritecollideany(ship,awards):
        game_stats.ship_left+=1
        awards.empty()
        scoreboard.prep_ships()
    
def update_enemies(ai_settings,game_stats,ship,bullets,aliens,screen,scoreboard,meteorites,awards):
    aliens.update()
    meteorites.update()
    awards.update()
    if pygame.sprite.spritecollideany(ship,aliens) or check_aliens_bottom(aliens,screen) or pygame.sprite.spritecollideany(ship,meteorites) or check_meteorites_bottom(meteorites,screen):
        ship_hit(ai_settings,game_stats,ship,bullets,aliens,screen,scoreboard,meteorites)
    check_awards_ship_collide(ai_settings,game_stats,ship,bullets,aliens,screen,scoreboard,meteorites,awards)
    check_awards_bottom(awards,screen)

def get_number_alien_x(ai_settings,alien_width):
    available_space_x=ai_settings.screen_width-2*alien_width
    number_alien_x=int(available_space_x/(2*alien_width))   #每行最多的外星人数目
    return number_alien_x

def get_number_rows(ai_settings,alien_height,ship_height):
    available_space_y=ai_settings.screen_lenth-ship_height-3*alien_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_one_random_alien(ai_settings,screen,aliens):
    alien=Alien(ai_settings,screen)
    alien.rect.y=alien.rect.height*2
    alien.width=alien.rect.width
    alien.x=random.random()*(ai_settings.screen_width-10)+5
    alien.rect.x=alien.x
    direction_store=[-1,1]
    alien.direction=direction_store[random.randint(0,1)]
    aliens.add(alien)

def create_one_meteorite(ai_settings,screen,meteorites):
    meteorite=Meteorite(ai_settings,screen)
    meteorite.rect.y=2*meteorite.rect.height 
    meteorite.width=meteorite.rect.width
    meteorite.x=random.random()*(ai_settings.screen_width-10)+5
    meteorite.rect.x=meteorite.x
    meteorites.add(meteorite)

def create_enemies(ai_settings,screen,aliens,start,meteorites,game_stats):
    end=Clock()
    if(end.time-start.time >= ai_settings.alien_birth_spare):
        start.time=end.time
        for i in range(0,ai_settings.alien_birth_per_time):
            create_one_random_alien(ai_settings,screen,aliens)
        if game_stats.meteorite_birth:
            create_one_meteorite(ai_settings,screen,meteorites)

def create_alien(ai_settings,screen,aliens,alien_num,row_number):
    alien=Alien(ai_settings,screen)
    alien.x=alien.rect.width+2*alien_num*alien.rect.width
    alien.width=alien.rect.width  #注意：这里要把宽度存起来，存到width里面
    alien.rect.x=alien.x       #为了后面调整的时候浮点计算，这里也用alien.x保持一致
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,aliens,ship):
    alien=Alien(ai_settings,screen)   #为了获得尺寸建立的临时实例
    number_alien_x=get_number_alien_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,alien.rect.height,ship.rect.height)
    for row_number in range(0,number_rows):
        for alien_num in range(0,number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_num,row_number)
