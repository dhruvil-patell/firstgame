import pygame
import time
import random
pygame.init()

#screen size
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dhruvils Game")
tag = 0 

# adjusting the player size
player_width = 30
player_height = 35
player = pygame.image.load("player.png").convert_alpha()
player = pygame.transform.scale(player, (player_width, player_height))
player2 = pygame.image.load("player2.png").convert_alpha()
player2 = pygame.transform.scale(player2, (player_width, player_height))

# making my game acc work
score_player1 = 0
score_player2 = 0


# intalizing
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))


# movement
groundLevel = 380 - player_height
x = 0
x2 = 300
y = groundLevel
y2 = groundLevel

gravity = 1 
gravity2 = 1      

jump_strength = 15  

y_velocity = 0
y_velocity2 = 0

start_time = time.time()
last_collision_time = 0  # Track last collision for cooldown

# Tagging game variables
current_tagger = 1  # 1 for player1 tagging player2, 2 for player2 tagging player1
round_duration = 30  # 2 minutes in seconds
round_start_time = time.time()


# make a platform platforms
def platform(x, y, width):
    r = pygame.Rect(x, y, width, 10)
    return r

def draw(r):
    pygame.draw.rect(screen, (150, 75, 0), r)

# making characters look back and forth
def character(picture_nane):
    character = pygame.image.load(picture_nane).convert_alpha()
    character = pygame.transform.scale(character, (player_width, player_height))
    return character

# keeping the players inside the screen
def inside(x, x2):
    if x < 0:
        x = 0
    if x >= screen_width:
        x = 780
    if x2 < 0:
        x2 = 0 
    if x2 >= screen_width:
        x2 = 780
    return x, x2

# Trying to make new maps
def create_map(*platforms):
    return list(platforms)


map1 = create_map(platform(200, 300, 100), platform(400, 250, 100), platform(600, 200, 100), platform(360, 150, 100))
map2 = create_map(platform(300, 300, 100), platform(400, 150, 100), platform(600, 250, 100), platform(200, 160, 100))
map3 = create_map(platform(random.randint(100, 300), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100))
map4 = create_map(platform(300, 300, 100), platform(400, 150, 100), platform(600, 250, 100), platform(360, 100, 100))
map5 = create_map(platform(300, 300, 100), platform(400, 150, 100), platform(600, 250, 100), platform(360, 100, 100))
map_selection = map1


clock = pygame.time.Clock()
Jumping = False
Jumping2 = False

# Font for displaying text
font = pygame.font.Font("font.ttf", 40) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    
# staying inside the screen
    x, x2 = inside(x, x2)

# Creating Graphics
    screen.blit(background, (0, 0))
    ground = pygame.Rect(0, 380, screen_width, 20)
    pygame.draw.rect(screen, (0, 247, 107), ground)

# Input Handling
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= 6
        player = character("player_flipped.png")
    if keys[pygame.K_RIGHT]:
        x += 6
        player = character("player.png")
    if keys[pygame.K_UP] and Jumping == False:
        y_velocity = -jump_strength
        Jumping = True
    
    if keys[pygame.K_a]:
        x2 -= 6
        player2 = character("player2.png")
    if keys[pygame.K_d]:
        x2 += 6
        player2 = character("player2_flipped.png")
    if keys[pygame.K_w] and Jumping2 == False:
        y_velocity2 =- jump_strength
        Jumping2 = True

    # Map Selections
    if keys[pygame.K_2]:
        map_selection = map2
    if keys[pygame.K_1]:
        map_selection = map1
    if keys[pygame.K_3]:
        map3 = create_map(platform(random.randint(100, 300), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100), platform(random.randint(100, 500), random.randint(100, 500), 100))
        map_selection = map3   
    if keys[pygame.K_4]:
        map_selection = map4
    if keys[pygame.K_5]:
        map_selection = map5


    y_velocity += gravity
    y += y_velocity
    if y > groundLevel:
        y = groundLevel
        Jumping = False
        y_velocity = 0

    y_velocity2 += gravity2
    y2 += y_velocity2
    if y2 > groundLevel:
        y2 = groundLevel
        Jumping2 = False
        y_velocity2 = 0
     

# Players Code
    player_hitbox = pygame.Rect(x, y, player_width, player_height)
    player2_hitbox = pygame.Rect(x2, y2, player_width, player_height)                                                    
    screen.blit(player, (x, y))
    screen.blit(player2, (x2, y2))

# Drawing the platforms
    if map_selection == map1:
        for obj in map1:
            draw(obj)
    elif map_selection == map2:
        for obj in map2:
            draw(obj)
    elif map_selection == map3:
        for obj in map3:
            draw(obj)
    elif map_selection == map4:
        for obj in map4:
            draw(obj)
    elif map_selection == map5:
        for obj in map5:
            draw(obj)



# Physics and Collision Detection
    for obj in map_selection:
        if player_hitbox.colliderect(obj):
            if player_hitbox.centery < obj.centery:
                y = obj.top - player_height
                Jumping = False
            else:
                y = obj.bottom
            y_velocity = 0

        if player2_hitbox.colliderect(obj):
            if player2_hitbox.centery < obj.centery:
                y2 = obj.top - player_height
                Jumping2 = False
            else:
                y2 = obj.bottom
            y_velocity2 = 0

    if player_hitbox.colliderect(player2_hitbox):
        current_time = time.time()
        if current_time - last_collision_time > 1.0:  # 1 second cooldown
            if current_tagger == 1:
                score_player1 += 1
            else:
                score_player2 += 1
            print(f"Player {current_tagger} scored! P1: {score_player1} P2: {score_player2}")
            last_collision_time = current_time

    # Check if round time is up and switch tagger
    time_elapsed = time.time() - round_start_time
    if time_elapsed >= round_duration:
        current_tagger = 2 if current_tagger == 1 else 1
        round_start_time = time.time()
        print(f"Time's up! Now Player {current_tagger}'s turn to tag!")

    # Display timer and scores
    time_left = max(0, int(round_duration - time_elapsed))
    timer_text = f"Player {current_tagger}'s turn - Time {time_left}s"
    score_text = f"P1 {score_player1}  P2 {score_player2}"
    
    timer_surface = font.render(timer_text, True, (255, 255, 255))
    score_surface = font.render(score_text, True, (255, 255, 255))
    
    screen.blit(timer_surface, (10, 10))
    screen.blit(score_surface, (10, 50))

    clock.tick(60)

    pygame.display.update()
