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


clock = pygame.time.Clock()
font = pygame.font.SysFont("Tahoma", 26)
seguisy28 = pygame.font.SysFont("segoeuisymbol",28, True)

button_width = 200
button_height = 50
button_y_start = height // 2
button_spacing = 20

start_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start, button_width, button_height)
instructions_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + button_height + button_spacing, button_width, button_height)
modifiers_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + 2*button_height + 2*button_spacing, button_width, button_height)
quit_button_rect = pygame.Rect((width // 2) - (button_width // 2), button_y_start + 3*button_height + 3*button_spacing, button_width, button_height)
back_button_rect = pygame.Rect((width // 2) - (button_width // 2), height - 120, button_width, button_height)
modifier_1_button_rect = pygame.Rect((width // 2) - (button_width), button_y_start, 2*button_width, button_height)
force_menu_button_rect = pygame.Rect(width - 150, 10, button_width // 2, button_height)

def reset_game():
    global platform, falling_blocks, extra_life, p_speed, b_speed, life_speed, extra_life_active, lives, score, last_life_spawn_time
    p_width = width // 2 - 60
    platform = pygame.Rect(p_width, height - 100, 120, 10)
    falling_blocks = pygame.Rect(random.randint(0, width - 20), 0, 20, 20)
    extra_life = pygame.Rect(random.randint(0,width - 20), 0, 20, 20)
    p_speed = 8
    b_speed = 5
    life_speed = 20
    extra_life_active = False
    lives = 3
    score = 0
    last_life_spawn_time = 0

game_state = "Menu"
vert_plat = False

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

        elif game_state == "Game Over!":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "Menu"

    screen.fill(BLACK)
    if game_state == "Menu":
        for y in range(0, height, 40):
            ratio = y / height
            r = int(TOP_LEFT[0] * (1 - ratio) + BOTTOM_RIGHT[0] * ratio)
            g = int(TOP_LEFT[1] * (1 - ratio) + BOTTOM_RIGHT[1] * ratio)
            b = int(TOP_LEFT[2] * (1 - ratio) + BOTTOM_RIGHT[2] * ratio)
            pygame.draw.rect(screen, (r, g, b), (0, y, width, 40))

        
        title_text = font.render("Catch the Falling Blocks!", True, DARK_BROWN)
        title_rect = title_text.get_rect(center = (width // 2, height // 2 - 200))
        screen.blit(title_text, title_rect)

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
        line3 = font.render("Catch RED hearts for extra lives", True, DARK_BROWN)
        line4 = font.render("Game will speed up with higher score, slow down when lives lost", True, DARK_BROWN)
        
        screen.blit(title, title.get_rect(center=(width // 2, 150)))
        screen.blit(line1, line1.get_rect(center=(width // 2, 250)))
        screen.blit(line2, line2.get_rect(center=(width // 2, 300)))
        screen.blit(line3, line3.get_rect(center=(width // 2, 350)))
        screen.blit(line4, line4.get_rect(center=(width // 2, 400)))

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

        if modifier_1_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT, modifier_1_button_rect)
        else:
            pygame.draw.rect(screen, DARK, modifier_1_button_rect)

        title = font.render("Modifiers", True, DARK_BROWN)
        wip_text = font.render("Work in progress!", True, DARK_BROWN)
        screen.blit(title, title.get_rect(center=(width // 2, 150)))
        screen.blit(wip_text, wip_text.get_rect(center=(width // 2, 250)))
        
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
        force_menu_text = font.render("Menu", True, WHITE)
        force_menu_text_rect = force_menu_text.get_rect(center=force_menu_button_rect.center)
        screen.blit(force_menu_text, force_menu_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and platform.left > 0:
            platform.move_ip(-p_speed, 0)
        if keys[pygame.K_RIGHT] and platform.right < width:
            platform.move_ip(p_speed, 0)
        if vert_plat is True and keys[pygame.K_UP] and height - 200 <= platform.top:
            platform.move_ip(0, -p_speed)
        if vert_plat is True and keys[pygame.K_DOWN] and platform.top <= height - 100:
            platform.move_ip(0, p_speed)

        falling_blocks.y += b_speed
        if falling_blocks.colliderect(platform):
            falling_blocks.y = 0
            falling_blocks.x = random.randint(0, width - 20)
            score += 1
            b_speed += 0.5
            p_speed += 0.5



        if lives == 1 and not extra_life_active and current_time - last_life_spawn_time > 5000:
            extra_life.x, extra_life.y = random.randint(0, width - 20), 0
            extra_life_active = True
            last_life_spawn_time = current_time

        if extra_life_active:
            extra_life.y += life_speed
            pygame.draw.circle(screen, RED, extra_life.center, 10)

            if extra_life.colliderect(platform):
                lives += 2
                p_speed *= 2
                b_speed *= 2
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