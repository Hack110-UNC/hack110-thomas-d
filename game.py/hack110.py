import pygame
from pygame.locals import *
import random
import sys 

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Falling Blocks")

WHITE, BLUE, RED, BLACK, DARK_BROWN, LIGHT, DARK = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (60, 45, 30), (170, 170, 170), (100, 100, 100)
BOTTOM_RIGHT = (220,180,130)
TOP_LEFT = (245, 240, 220)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)


clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 28, bold = True)
title_font = pygame.font.SysFont("Calibri", 56, bold = True)
seguisy28 = pygame.font.SysFont("segoeuisymbol",28, True)

button_width = 200
button_height = 50
button_y_start = height // 2
button_spacing = 20
norm_max, hard_max = 0, 0

start_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start, button_width, button_height)
instructions_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + button_height + button_spacing, button_width, button_height)
modifiers_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + 2*button_height + 2*button_spacing, button_width, button_height)
quit_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + 3*button_height + 3*button_spacing, button_width, button_height)
back_button_rect = pygame.Rect((width // 2) - (button_width // 2), height - 120, button_width, button_height)
modifier_1_button_rect = pygame.Rect((width // 2) - (button_width), button_y_start - 100, 2*button_width, button_height)
modifier_2_button_rect = pygame.Rect((width // 2) - (button_width), button_y_start - 100 + button_height + button_spacing, 2*button_width, button_height)
modifier_3_button_rect = pygame.Rect((width // 2) - (button_width), button_y_start - 100 + 2*button_height + 2*button_spacing, 2*button_width, button_height)
modifier_4_button_rect = pygame.Rect((width // 2) - (button_width), button_y_start - 100 + 3*button_height + 3*button_spacing, 2*button_width, button_height)
force_menu_button_rect = pygame.Rect(width - 100, 10, button_width // 4, button_height)

try:
    menu_background_image = pygame.image.load("game.py/images/colorful-blocks-falling-gently-with-clouds-below-daytime-animation-video.jpg").convert()
    menu_background_image = pygame.transform.scale(menu_background_image, (width, height))
except Exception as e:
    print(f"Error loading image: {e}")  # I have no idea what this does. My background wouldn't display
                                        # without it so I had to search this up.
    menu_background_image = None

def reset_game():
    global platform, falling_blocks, extra_life, p_speed, b_speed, life_speed, extra_life_active, lives, score, last_life_spawn_time
    if hard_mode:
        platform_width = 80 
    else:
        platform_width = 120 
    p_width = width // 2 - (platform_width // 2) 
    platform = pygame.Rect(p_width, height - 100, platform_width, 10)
    falling_blocks = pygame.Rect(random.randint(0, width - 20), 0, 20, 20)
    extra_life = pygame.Rect(random.randint(0,width - 20), 0, 20, 20)
    p_speed = 8
    b_speed = 5
    life_speed = 20
    extra_life_active = False
    if hard_mode: 
        lives = 2
    else: 
        lives = 5
    score = 0
    last_life_spawn_time = 0

game_state = "Menu"
vert_plat = False
invert_controls = 1
hard_mode = False


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "Menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "Game"
                elif instructions_button_rect.collidepoint(mouse_pos):
                    game_state = "Instructions"
                elif modifiers_button_rect.collidepoint(mouse_pos):
                    game_state = "Modifiers"
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False

        elif game_state == "Instructions":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(mouse_pos):
                    game_state = "Menu"

        elif game_state == "Modifiers":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(mouse_pos):
                    game_state = "Menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if modifier_1_button_rect.collidepoint(mouse_pos):
                    vert_plat = not vert_plat
            if event.type == pygame.MOUSEBUTTONDOWN:
                if modifier_2_button_rect.collidepoint(mouse_pos):
                    invert_controls *= -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if modifier_3_button_rect.collidepoint(mouse_pos):
                    hard_mode = not hard_mode

        elif game_state == "Game Over!":
            if hard_mode is False:
                if score > norm_max:
                    norm_max = score
            else:
                if score > hard_max:
                    hard_max = score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "Menu"

    screen.fill(BLACK)
    if game_state == "Menu":
        # for y in range(0, height, 40):
        #     ratio = y / height
        #     r = int(TOP_LEFT[0] * (1 - ratio) + BOTTOM_RIGHT[0] * ratio)
        #     g = int(TOP_LEFT[1] * (1 - ratio) + BOTTOM_RIGHT[1] * ratio)
        #     b = int(TOP_LEFT[2] * (1 - ratio) + BOTTOM_RIGHT[2] * ratio)
        #     pygame.draw.rect(screen, (r, g, b), (0, y, width, 40))
        if game_state == "Menu":
            if menu_background_image:
                screen.blit(menu_background_image, (0, 0))
            else:
                screen.fill(TOP_LEFT) 
        
        title_text = title_font.render("Catch the Falling Blocks!", True, BLACK)
        title_rect = title_text.get_rect(center = (width // 2, height // 2 - 200))
        screen.blit(title_text, title_rect)

        norm_max_text = font.render(f"High Score (Normal Mode): {norm_max}", True, BLACK)
        norm_max_rect = norm_max_text.get_rect(midleft = (10, height - 60))
        screen.blit(norm_max_text, norm_max_rect)

        hard_max_text = font.render(f"High Score (Hard Mode): {hard_max}", True, BLACK)
        hard_max_rect = hard_max_text.get_rect(midleft = (10, height - 10))
        screen.blit(hard_max_text, hard_max_rect)

        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, start_button_rect)
        else:
            pygame.draw.rect(screen, DARK, start_button_rect)
        
        start_text = font.render("Start!", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        if instructions_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, instructions_button_rect)
        else:
            pygame.draw.rect(screen, DARK, instructions_button_rect)
        instructions_text = font.render("Instructions", True, WHITE)
        instructions_text_rect = instructions_text.get_rect(center=instructions_button_rect.center)
        screen.blit(instructions_text, instructions_text_rect)

        if modifiers_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifiers_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifiers_button_rect)

        modifiers_text = font.render("Modifiers", True, WHITE)
        modifiers_text_rect = modifiers_text.get_rect(center=modifiers_button_rect.center)
        screen.blit(modifiers_text, modifiers_text_rect)

        if quit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, quit_button_rect)
        else:
            pygame.draw.rect(screen, DARK, quit_button_rect)

        quit_text = font.render("Quit", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

    elif game_state == "Game Over!":
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, RED)
        restart_text = font.render("Press ENTER to return to Menu", True, WHITE)
        game_over_rect = game_over_text.get_rect(center = (width // 2, height // 2 - 40))
        restart_rect = restart_text.get_rect(center = (width // 2, height // 2 + 20))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    elif game_state == "Instructions":
        for y in range(0, height, 40):
            ratio = y / height
            r = int(TOP_LEFT[0] * (1 - ratio) + BOTTOM_RIGHT[0] * ratio)
            g = int(TOP_LEFT[1] * (1 - ratio) + BOTTOM_RIGHT[1] * ratio)
            b = int(TOP_LEFT[2] * (1 - ratio) + BOTTOM_RIGHT[2] * ratio)
            pygame.draw.rect(screen, (r, g, b), (0, y, width, 40))

        title = font.render("Instructions", True, DARK_BROWN)
        line1 = font.render("Use LEFT and RIGHT arrows to move platform", True, DARK_BROWN)
        line2 = font.render("Catch BLUE blocks to increase score", True, DARK_BROWN)
        line3 = font.render("Catch RED hearts for extra lives*", True, DARK_BROWN)
        line4 = font.render("Game will speed up with higher score, slow down when lives lost", True, DARK_BROWN)
        line5 = font.render("*Normal mode exclusive ", True, DARK_BROWN)

        screen.blit(title, title.get_rect(center=(width // 2, 150)))
        screen.blit(line1, line1.get_rect(center=(width // 2, 250)))
        screen.blit(line2, line2.get_rect(center=(width // 2, 300)))
        screen.blit(line3, line3.get_rect(center=(width // 2, 350)))
        screen.blit(line4, line4.get_rect(center=(width // 2, 400)))
        screen.blit(line5, line5.get_rect(center=(width // 2, 500)))

        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, back_button_rect)
        else:
            pygame.draw.rect(screen, DARK, back_button_rect)\
        
        back_text = font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

    elif game_state == "Modifiers":
        for y in range(0, height, 40):
            ratio = y / height
            r = int(TOP_LEFT[0] * (1 - ratio) + BOTTOM_RIGHT[0] * ratio)
            g = int(TOP_LEFT[1] * (1 - ratio) + BOTTOM_RIGHT[1] * ratio)
            b = int(TOP_LEFT[2] * (1 - ratio) + BOTTOM_RIGHT[2] * ratio)
            pygame.draw.rect(screen, (r, g, b), (0, y, width, 40))

        title = font.render("Modifiers", True, DARK_BROWN)
        screen.blit(title, title.get_rect(center=(width // 2, 150)))
        
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, back_button_rect)
        else:
            pygame.draw.rect(screen, DARK, back_button_rect)
        
        back_text = font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        if modifier_1_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifier_1_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifier_1_button_rect)
        if vert_plat is False:
            modifier_1_text = font.render("Platform Vertical Motion: Off", True, WHITE)
        else: 
            modifier_1_text = font.render("Platform Vertical Motion: On", True, WHITE)
        modifier_1_text_rect = modifier_1_text.get_rect(center = modifier_1_button_rect.center)
        screen.blit(modifier_1_text, modifier_1_text_rect)

        if modifier_2_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifier_2_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifier_2_button_rect)
        if invert_controls == 1:
            modifier_2_text = font.render("Inverted Controls: Off", True, WHITE)
        else: 
            modifier_2_text = font.render("Inverted Controls: On", True, WHITE)
        modifier_2_text_rect = modifier_2_text.get_rect(center = modifier_2_button_rect.center)
        screen.blit(modifier_2_text, modifier_2_text_rect)

        if modifier_3_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifier_3_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifier_3_button_rect)
        if hard_mode is False:
            modifier_3_text = font.render("Normal", True, WHITE)
        else: 
            modifier_3_text = font.render("Hard", True, WHITE)
        modifier_3_text_rect = modifier_3_text.get_rect(center = modifier_3_button_rect.center)
        screen.blit(modifier_3_text, modifier_3_text_rect)

        modifier_4_text = font.render("Coming Soon!", True, WHITE)
        if modifier_4_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifier_4_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifier_4_button_rect)
        modifier_4_text_rect = modifier_4_text.get_rect(center = modifier_4_button_rect.center)
        screen.blit(modifier_4_text, modifier_4_text_rect)


    elif game_state == "Game":
        current_time = pygame.time.get_ticks()
        for y in range(0, height, 40):
                ratio = y / height
                r = int(TOP_LEFT[0] * (1 - ratio) + BOTTOM_RIGHT[0] * ratio)
                g = int(TOP_LEFT[1] * (1 - ratio) + BOTTOM_RIGHT[1] * ratio)
                b = int(TOP_LEFT[2] * (1 - ratio) + BOTTOM_RIGHT[2] * ratio)
                pygame.draw.rect(screen, (r, g, b), (0, y, width, 40))
        if event.type == pygame.MOUSEBUTTONDOWN:
                if force_menu_button_rect.collidepoint(mouse_pos):
                    game_state = "Menu"

        if force_menu_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, force_menu_button_rect)
        else:
            pygame.draw.rect(screen, DARK, force_menu_button_rect)
            
        force_menu_text = seguisy28.render("🏠", True, WHITE)
        force_menu_text_rect = force_menu_text.get_rect(center=force_menu_button_rect.center)
        screen.blit(force_menu_text, force_menu_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and invert_controls*platform.left > (width*invert_controls-width)/2:
            platform.move_ip(-p_speed * invert_controls, 0)
        if keys[pygame.K_RIGHT] and invert_controls*platform.right < (width*invert_controls+width)/2:
            platform.move_ip(p_speed * invert_controls, 0)
        if vert_plat is True and keys[pygame.K_UP] and height - 200 + (height - 150)*(invert_controls - 1)< invert_controls*platform.top:
            platform.move_ip(0, -p_speed * invert_controls)
        if vert_plat is True and keys[pygame.K_DOWN] and invert_controls*platform.top < height - 100 + (height - 150)*(invert_controls - 1):
            platform.move_ip(0, p_speed * invert_controls)

        falling_blocks.y += b_speed
        if falling_blocks.colliderect(platform):
            falling_blocks.y = 0
            falling_blocks.x = random.randint(0, width - 20)
            score += 1
            b_speed += 1
            p_speed += 1



        if lives == 1 and not extra_life_active and current_time - last_life_spawn_time > 5000 and hard_mode is False:
            extra_life.x, extra_life.y = random.randint(0, width - 20), 0
            extra_life_active = True
            last_life_spawn_time = current_time

        if extra_life_active:
            extra_life.y += life_speed
            pygame.draw.circle(screen, RED, extra_life.center, 10)

            if extra_life.colliderect(platform):
                lives += 2
                extra_life_active = False


            elif extra_life.y > height:
                extra_life_active = False

        if falling_blocks.y > height:
            if lives == 1:
                game_state = "Game Over!"
            else:
                lives -= 1
                b_speed /= 1.5
                p_speed  /= 1.5
                falling_blocks.y = 0
                falling_blocks.x = random.randint(0, width - 20)

        pygame.draw.rect(screen, BLACK, platform)
        pygame.draw.rect(screen, BLUE, falling_blocks)

        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = seguisy28.render(f"Lives: {"❤️"*lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()