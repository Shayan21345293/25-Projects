import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Load images (replace with your actual image paths)
player_img = pygame.transform.scale(pygame.image.load('player.png'), (80, 80))
enemy_img = pygame.transform.scale(pygame.image.load('alien.png'), (100, 100))
bullet_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('bullet.png'), (32, 32)), 90)
powerup_img = pygame.transform.scale(pygame.image.load('up.png'), (30, 30))
boss_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('boss.png'), (350, 300)), 180)

# Load sounds (replace with your actual sound paths)
bullet_sound = pygame.mixer.Sound('laser.mp3')
bullet_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound('explosion.mp3')
explosion_sound.set_volume(0.5)
powerup_sound = pygame.mixer.Sound('pe.mp3')
powerup_sound.set_volume(0.3)
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

# Player setup
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 4
default_player_speed = 4
power_up_active = False
power_up_duration = 5000

# Enemies setup
enemies = []
num_enemies = 6
enemy_speed = 2.5
enemy_drop = 35
for _ in range(num_enemies):
    enemies.append({
        'x': random.randint(0, 736),
        'y': random.randint(50, 150),
        'x_change': enemy_speed,
        'y_change': enemy_drop
    })

# Bullets setup
bullets = []
bullet_speed = 10

# Power-Up setup
power_up = {
    'x': random.randint(0, 736),
    'y': random.randint(50, 150),
    'y_change': 2,
    'state': "ready",
    'start_time': 0
}

# Score setup
score = 0
font = pygame.font.Font(None, 36)
over_font = pygame.font.Font(None, 64)

# Boss setup
boss = {
    'x': 320,
    'y': 50,
    'x_change': 2,
    'health': 20,
    'alive': True,
    'bullets': [],
    'bullet_timer': 0,
    'hitbox_radius': 80  # Larger hitbox for the boss
}

# Game state
game_started = False
game_over = False
debug_mode = False  # Set to True to see hitboxes

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.Font(None, size)
    text_surf = font_obj.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)
    else:
        screen.blit(text_surf, (x, y))

def is_collision(x1, y1, x2, y2, threshold=27):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < threshold

def fire_bullet(x, y):
    # Center the bullet on player's ship (player is 80px wide)
    bullets.append({'x': x + 40 - 16, 'y': y})  # 16 is half of bullet width (32px)
    bullet_sound.play()

def boss_fire():
    # Create a spread of bullets aimed downward
    for angle in range(-30, 31, 15):  # -30, -15, 0, 15, 30 degrees
        rad = math.radians(angle)
        speed_x = math.sin(rad) * 3  # Horizontal component
        speed_y = math.cos(rad) * 5  # Vertical component (downward)
        # Start bullets from different points on the boss
        start_x = boss['x'] + 160 + (angle / 3) * 2
        start_y = boss['y'] + 160
        boss['bullets'].append({
            'x': start_x,
            'y': start_y,
            'speed_x': speed_x,
            'speed_y': speed_y
        })

# Main game loop
running = True
while running:
    screen.fill((0, 0, 30))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_started and not game_over and boss['alive']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change = player_speed
                if event.key == pygame.K_SPACE:
                    if power_up_active:
                        for offset in [-20, 0, 20]:
                            fire_bullet(player_x + offset, player_y)
                    else:
                        if len(bullets) < 1:
                            fire_bullet(player_x, player_y)
                if event.key == pygame.K_d:  # Toggle debug mode with D key
                    debug_mode = not debug_mode
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_x_change = 0
        
        if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
            game_started = True
        
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            # Reset game
            player_x = 370
            score = 0
            boss['health'] = 30
            boss['alive'] = True
            power_up_active = False
            bullets.clear()
            boss['bullets'].clear()
            game_over = False
            game_started = False
    
    # Game states
    if not game_started:
        draw_text("Space Invaders", 64, (255, 255, 255), 400, 200)
        draw_text("Click to Start Game", 36, (255, 255, 255), 400, 300)
    elif game_over:
        draw_text("GAME OVER", 64, (255, 0, 0), 400, 250)
        draw_text("Click to Play Again", 36, (255, 255, 255), 400, 350)
    elif not boss['alive']:
        draw_text("YOU WIN!", 64, (0, 255, 0), 400, 250)
    else:
        # Player movement
        player_x += player_x_change
        player_x = max(0, min(player_x, 736))
        
        # Regular enemies
        if score < 20:
            draw_text(f"Score: {score}/20 to fight Boss", 28, (255, 255, 0), 400, 10)
            for enemy in enemies:
                enemy['x'] += enemy['x_change']
                if enemy['x'] <= 0 or enemy['x'] >= 736:
                    enemy['x_change'] *= -1
                    enemy['y'] += enemy['y_change']
                
                # Enemy-bullet collision
                for bullet in bullets[:]:
                    if is_collision(enemy['x'] + 50, enemy['y'] + 50, bullet['x'] + 16, bullet['y'] + 16):
                        explosion_sound.play()
                        bullets.remove(bullet)
                        score += 1
                        enemy['x'] = random.randint(0, 736)
                        enemy['y'] = random.randint(50, 150)
                
                # Draw enemy
                screen.blit(enemy_img, (enemy['x'], enemy['y']))
                if debug_mode:
                    pygame.draw.circle(screen, (255, 0, 255), (enemy['x'] + 50, enemy['y'] + 50), 27, 1)
                
                # Game over if enemy reaches bottom
                if enemy['y'] > 420:
                    game_over = True
        else:
            # Boss fight
            boss['x'] += boss['x_change']
            if boss['x'] <= 0 or boss['x'] >= 640:
                boss['x_change'] *= -1
            
            # Boss firing
            if pygame.time.get_ticks() - boss['bullet_timer'] > 2000:  # Fire every second
                boss_fire()
                boss['bullet_timer'] = pygame.time.get_ticks()
            
            # Calculate boss center position
            boss_center_x = boss['x'] + 175
            boss_center_y = boss['y'] + 150
            
            # Boss-bullet collision with larger threshold
            for bullet in bullets[:]:
                bullet_center_x = bullet['x'] + 16
                bullet_center_y = bullet['y'] + 16
                if is_collision(boss_center_x, boss_center_y, bullet_center_x, bullet_center_y, boss['hitbox_radius']):
                    explosion_sound.play()
                    bullets.remove(bullet)
                    boss['health'] -= 1
                    if boss['health'] <= 0:
                        boss['alive'] = False
            
            # Draw boss with health bar
            screen.blit(boss_img, (boss['x'], boss['y']))
            pygame.draw.rect(screen, (255, 0, 0), (boss['x'], boss['y'] - 10, 160, 10))
            pygame.draw.rect(screen, (0, 255, 0), (boss['x'], boss['y'] - 10, 160 * (boss['health'] / 20), 10))
            if debug_mode:
                pygame.draw.circle(screen, (255, 0, 255), (int(boss_center_x), int(boss_center_y)), boss['hitbox_radius'], 1)
        
        # Player bullets
        for bullet in bullets[:]:
            screen.blit(bullet_img, (bullet['x'], bullet['y']))
            bullet['y'] -= bullet_speed
            if bullet['y'] < 0:
                bullets.remove(bullet)
            if debug_mode:
                pygame.draw.circle(screen, (0, 255, 255), (bullet['x'] + 16, bullet['y'] + 16), 16, 1)
        
        # Boss bullets
        for b in boss['bullets'][:]:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)
            b['x'] += b['speed_x']
            b['y'] += b['speed_y']
            if is_collision(player_x + 40, player_y + 40, b['x'], b['y'], 30):
                game_over = True
            if b['x'] < 0 or b['x'] > 800 or b['y'] > 600:
                boss['bullets'].remove(b)
        
        # Power-Up
        if power_up['state'] == "ready":
            power_up['y'] += power_up['y_change']
            if power_up['y'] > 600:
                power_up['y'] = random.randint(50, 150)
                power_up['x'] = random.randint(0, 736)
            screen.blit(powerup_img, (power_up['x'], power_up['y']))
        
        # Power-Up collection
        if (power_up['state'] == "ready" and
            player_x < power_up['x'] + 40 and player_x + 80 > power_up['x'] and
            player_y < power_up['y'] + 40 and player_y + 80 > power_up['y']):
            powerup_sound.play()
            power_up['state'] = "taken"
            power_up_active = True
            power_up['start_time'] = pygame.time.get_ticks()
            player_speed += 2
        
        # Power-Up expiration
        if power_up_active and pygame.time.get_ticks() - power_up['start_time'] > power_up_duration:
            power_up_active = False
            player_speed = default_player_speed
            power_up['state'] = "ready"
            power_up['y'] = random.randint(50, 150)
            power_up['x'] = random.randint(0, 736)
        
        # Draw player and score
        screen.blit(player_img, (player_x, player_y))
        draw_text(f"Score: {score}", 36, (255, 255, 255), 10, 10, False)
        if debug_mode:
            draw_text("DEBUG MODE", 24, (255, 0, 0), 750, 10, False)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()