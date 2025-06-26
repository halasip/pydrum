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
medium_font = pygame.font.Font('freesansbold.ttf', 24)

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

pygame.mixer.set_num_channels(len(sounds)*3)

pads = [[ -1 for _ in range(beats)] for _ in range(len(instruments))]

def play_sound():
    for i in range(len(pads)):
        if pads[i][active_beat] == 1:
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
            if pads[j][i] == -1:
                color = black
            else:
                color = red
            pygame.draw.rect(screen, color, rect_dimensions, 0, 11)
            rect = pygame.draw.rect(screen, light_grey, rect_dimensions, 5, 5)
            boxes.append((rect,(j, i)))

    # -5 and +10 to make the active beat rectangle wider and more visible
    active_beat_rect = pygame.draw.rect(screen, green, [lbox_width + active_beat * col_width -5, 0, col_width +10, lbox_height], 10, 5)

    # lower menu buttons
    



    return boxes



while running:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid()

    if beat_changed:
        play_sound()
        beat_changed = False



    play_box = pygame.draw.rect(screen, dark_grey, [50, HEIGHT-150, 200, 100], 0, 5)
    screen.blit(label_font.render("Play/Pause", True, white), (60, HEIGHT-130))
    if playing:
        text = medium_font.render("Play", True, light_grey)
        if beat_changed:
            play_sound()
            beat_changed = False
    else:
        text = medium_font.render("Pause", True, light_grey)
    screen.blit(text, (60, HEIGHT-90))

    bpm_box = pygame.draw.rect(screen, dark_grey, [300, HEIGHT-150, 200, 100], 5, 5)
    bpm_text = medium_font.render(f"{bpm} bpm", True, white)
    screen.blit(bpm_text, (325, HEIGHT-130))
    bpm_change_rect = []
    bpm_text_list = ["<<", "<", ">",  ">>"]
    bpm_text_shift = [0,-10,-10,0]
    for i in range(4):
        bpm_change_rect.append(pygame.draw.rect(screen, light_grey, [300+i*50, HEIGHT-100, 50, 50], 0, 0))
        screen.blit(medium_font.render(bpm_text_list[i], True, white), (320+bpm_text_shift[i]+i*50, HEIGHT-90))


    pygame.draw.rect(screen, dark_grey, [550, HEIGHT-150, 200, 100], 5, 5)
    screen.blit(medium_font.render("Beat count", True, white), (560, HEIGHT-130))
    screen.blit(label_font.render( f"{beats}"  , True, white), (610, HEIGHT-90))
    beats_change_rect1 = pygame.draw.rect(screen, light_grey, [700, HEIGHT-100, 50, 50], 0, 5)
    beats_change_rect2 = pygame.draw.rect(screen, light_grey, [700, HEIGHT-150, 50, 50], 0, 5)
    screen.blit(medium_font.render("+1", True, white), (700, HEIGHT-100))
    screen.blit(medium_font.render("-1", True, white), (700, HEIGHT-150))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
                        
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    pads[coords[0]][coords[1]] *= -1
                    print(f"Clicked on {instruments[coords[0]]} at beat {coords[1]}")
                    # Here you can add sound playing logic
                    pygame.draw.rect(screen, red, boxes[i][0])

        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(bpm_change_rect)):
                if bpm_change_rect[i].collidepoint(event.pos):
                    match(i):
                        case(0): bpm -= 5
                        case(1): bpm -= 1
                        case(2): bpm += 1
                        case(3): bpm += 5
            if play_box.collidepoint(event.pos):
                playing = not playing
                if playing:
                    active_length = 0
                    active_beat = 0
                    beat_changed = True
                else:
                    active_length = 0

            elif beats_change_rect1.collidepoint(event.pos):
                beats += 1
                for i in range(len(pads)):
                    pads[i].append(-1)

            elif beats_change_rect2.collidepoint(event.pos):
                beats -= 1
                for i in range(len(pads)):
                    pads[i].pop(-1)


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