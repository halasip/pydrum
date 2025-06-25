import pygame
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 1200, 800

black = (0, 0, 0)
white = (255, 255, 255)
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
clicked_boxes = [[ -1 for _ in range(beats)] for _ in range(len(instruments))]

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

    for j in range(len(instruments)):
        text = label_font.render(instruments[j], True, green)
        screen.blit(text, (30, j*row_hight+30))
        pygame.draw.line(screen, white, (0, j*row_hight), (250, j*row_hight), 5)

        for i in range(beats):
            rect = pygame.draw.rect(screen, light_grey, [lbox_width+i*col_width, j*row_hight, col_width, row_hight], 5)
            boxes.append((rect,(j, i)))

    return boxes



running = True
while running:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    idx, beat = boxes[i][1]
                    print(f"Clicked on {instruments[idx]} at beat {beat}")
                    # Here you can add sound playing logic
                    pygame.draw.rect(screen, red, boxes[i][0])

    pygame.display.flip()

pygame.quit()