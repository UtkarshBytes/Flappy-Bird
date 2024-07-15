import pygame
import Config
import tile_map
import light_handling
import random

# Initialize Pygame
pygame.init()

# Set up the Pygame window
win = pygame.display.set_mode(Config.WINDOW_SIZE)
clock = pygame.time.Clock()

# Initialize the tile map and light handling objects
map = tile_map.Tile_map()
light = light_handling.light_handling(map.walls, map.points)

# Initialize Flappy Bird variables
fps = 60
screen_width = 460
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
collision_sound_played = False
bg = pygame.image.load('bg_4dark.png')
ground_img = pygame.image.load('floordark.png')
button_img = pygame.image.load('restart.png')
flap_sound = pygame.mixer.Sound('wing_flap.wav')
score_sound = pygame.mixer.Sound('point.wav')
collision_sound = pygame.mixer.Sound('hit.wav')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    global collision_sound_played
    collision_sound_played = False
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        global flying, game_over, collision_sound_played, score, pass_pipe
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 500:
                self.rect.y += int(self.vel)
        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
                flap_sound.play()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bottomdark.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

# Main game loop
flag = True
while flag:
    clock.tick(Config.FPS)

    # Handle events for both games
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    # Update the tile map and light handling
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    map.update_variables(mouse_pos, mouse_pressed, light)
    light.update_variables(mouse_pos, mouse_pressed)

    # Draw the tile map and light handling
    win.fill((0, 0, 0))
    light.draw(win)
    map.draw(win)

    # Flappy Bird game logic
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                score_sound.play()
    draw_text(str(score), font, white, int(screen_width / 2), 20)
    screen.blit(ground_img, (ground_scroll, 500))
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) \
            or flappy.rect.top < 0 or flappy.rect.bottom >= 500:
        game_over = True
        if not collision_sound_played:
            collision_sound.play()
            collision_sound_played = True
    if flappy.rect.bottom >= 500:
        game_over = True
        flying = False
    if not game_over and flying:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.MOUSEBUTTONUP and not flying and not game_over:
            flying = True

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

