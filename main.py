import pygame
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 1200, 800

black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
darkgrey = (20, 20, 20)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
dark_grey = (50, 50, 50)
light_grey = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyDrum")
label_font = pygame.font.Font('freesansbold.ttf', 32)

boxes = []
fps = 60
beats = 8
instruments = ["Kick", "Snare", "Hi-Hat", "Bass Drum", "Crash"]
timer = pygame.time.Clock()

def draw_grid():
    lbox_width = 250    
    bbox_height = 250

    lbox_height = HEIGHT - bbox_height
    bbox_width  = WIDTH

    left_box = pygame.draw.rect(screen, white, [0, 0, lbox_width, lbox_height], 5)
    bottom_box = pygame.draw.rect(screen, white, [0, lbox_height, WIDTH, bbox_height], 5)
    boxes = []
    colors = [ white, red, blue, green, dark_grey, light_grey ]

    row_hight = lbox_height // len(instruments)
    col_width = (WIDTH - lbox_width) // beats

    for idx,sound in enumerate(instruments):
        text = label_font.render(instruments[idx], True, green)
        screen.blit(text, (30, idx*row_hight+30))
        pygame.draw.line(screen, white, (0, idx*row_hight), (250, idx*row_hight), 5)

        for i in range(beats):
            rect = pygame.draw.rect(screen, light_grey, [lbox_width+i*col_width, idx*row_hight, col_width, row_hight], 5)
            boxes.append((rect,(idx, i)))

    return boxes



running = True
while running:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()