import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
screen_width = 800
screen_height = 640
lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((screen_width + side_margin, screen_height + lower_margin))
pygame.display.set_caption("Level Editor")


# define game variables
rows = 16
max_cols = 150
tile_size = screen_height // rows
tile_types = 27
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
sky_image = pygame.image.load("Images/Background/sky_cloud1.png").convert_alpha()
mountains_image = pygame.image.load("Images/Background/mountains.png").convert_alpha()
forest_image = pygame.image.load("Images/Background/forest.png").convert_alpha()
# store tiles in list
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f"Images/Tiles/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

# define colors
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)

# define font
font = pygame.font.SysFont("Comic Sans MS", 30)
# create empty list
world_data = []
for row in range(rows):
    r = [-1] * max_cols
    world_data.append(r)

# create ground
for tile in range(0, max_cols):
    world_data[rows - 1][tile] = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing bg
def draw_bg():
    screen.fill(green)
    width = sky_image.get_width()
    for x in range(5):
        screen.blit(sky_image, ((x * width) - scroll * 0.3, 0))
        screen.blit(mountains_image, ((x * width) - scroll * 0.65, screen_height - mountains_image.get_height() - 50))
        screen.blit(forest_image, ((x * width) - scroll * 0.8, screen_height - forest_image.get_height()))


save_img = pygame.image.load("Images/Buttons/save.png").convert_alpha()
load_img = pygame.image.load("Images/Buttons/load.png").convert_alpha()


# draw grid
def draw_grid():
    # vertical lines
    for c in range(max_cols + 1):
        pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, screen_height))
    # horizontal lines
    for c in range(rows + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


# func for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * tile_size - scroll, y * tile_size))


# create buttons
save_button = button.Button(screen_width // 1.5, screen_height + lower_margin - 80, save_img, 0.5)
load_button = button.Button(screen_width // 1.5 + 300, screen_height + lower_margin - 80, load_img, 0.5)
# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(screen_width + (75 * button_col) + 20, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 4:
        button_row += 1
        button_col = 0


run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f"Level: {level}", font, white, 10, screen_height + lower_margin - 90)
    draw_text(f"Press UP or DOWN to change level", font, white, 10, screen_height + lower_margin - 60)
    # save and load data
    if save_button.draw(screen):
        # save level data
        with open(f"level{level}_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        # load in level data
        # reset scroll to the start
        scroll = 0
        with open(f"level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # draw tile panel and tiles
    pygame.draw.rect(screen, green, (screen_width, 0, side_margin, screen_height))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    pygame.draw.rect(screen, red, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (max_cols * tile_size) - screen_width:
        scroll += 5 * scroll_speed

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // tile_size
    y = pos[1] // tile_size

    # check that coordinates are within the tile area
    if pos[0] < screen_width and pos[1] < screen_height:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
