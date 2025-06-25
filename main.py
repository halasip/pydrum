import pygame
from pygame import mixer
import os


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

playing = True
active_length = 0
active_beat = 0
beat_changed = False
running = True


boxes = []
fps = 60
bpm = 120  # Beats per minute
beats = 8
instruments = []
timer = pygame.time.Clock()

# Import sound files
# for each file in sounds directory, load the sound
sounds = []
kitidx = 1 
for file in sorted(os.listdir(f'sounds/kit{kitidx}')):
    sound_name = file.split('.')[0]
    sounds.append(mixer.Sound(os.path.join(f'sounds/kit{kitidx}', file)))
    instruments.append(sound_name.title())

clicked_boxes = [[ -1 for _ in range(beats)] for _ in range(len(instruments))]

def play_sound():
    for i in range(len(clicked_boxes)):
        if clicked_boxes[i][active_beat] == 1:
            sounds[i].play()


def draw_grid():
    lbox_width = 250    
    bbox_height = 250

    lbox_height = HEIGHT - bbox_height
    bbox_width  = WIDTH

    left_box = pygame.draw.rect(screen, white, [0, 0, lbox_width, lbox_height], 5)
    bottom_box = pygame.draw.rect(screen, white, [0, lbox_height, bbox_width, bbox_height], 5)
    boxes = []
    colors = [ white, red, blue, green, dark_grey, light_grey ]

    row_hight = lbox_height // len(instruments)
    col_width = (WIDTH - lbox_width) // beats

    for j in range(len(instruments)):
        text = label_font.render(instruments[j], True, green)
        screen.blit(text, (30, j*row_hight+30))
        pygame.draw.line(screen, white, (0, j*row_hight), (250, j*row_hight), 5)

        for i in range(beats):
            rect_dimensions = [lbox_width+i*col_width, j*row_hight, col_width, row_hight]
            if clicked_boxes[j][i] == -1:
                color = black
            else:
                color = red
            pygame.draw.rect(screen, color, rect_dimensions, 0, 11)
            rect = pygame.draw.rect(screen, light_grey, rect_dimensions, 5, 5)
            boxes.append((rect,(j, i)))

    # -5 and +10 to make the active beat rectangle wider and more visible
    active_beat_rect = pygame.draw.rect(screen, green, [lbox_width + active_beat * col_width -5, 0, col_width +10, lbox_height], 10, 5)

    return boxes



while running:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid()

    if beat_changed:
        play_sound()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked_boxes[coords[0]][coords[1]] *= -1
                    print(f"Clicked on {instruments[coords[0]]} at beat {coords[1]}")
                    # Here you can add sound playing logic
                    pygame.draw.rect(screen, red, boxes[i][0])

    beat_length = fps * 60 // bpm
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            beat_changed = True
            if active_beat < beats - 1:
                active_beat += 1
            else:
                active_beat = 0

    pygame.display.flip()

pygame.quit()