import pygame
from pygame import mixer
import pyaml
import os


pygame.init()

WIDTH, HEIGHT = 1200, 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gold = (255, 215, 0)
dark_grey = (50, 50, 50)
midgrey = (100, 100, 100)
light_grey = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyDrum")
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

running = True
fps = 60
beats = 8
timer = pygame.time.Clock()

# Import sound files
# for each file in sounds directory, load the sound
sounds = []
instruments = []
kitidx = 1 
for file in sorted(os.listdir(f'sounds/kit{kitidx}')):
    sound_name = file.split('.')[0]
    sounds.append(mixer.Sound(os.path.join(f'sounds/kit{kitidx}', file)))
    instruments.append(sound_name.title())

pygame.mixer.set_num_channels(len(sounds)*3)

pads = [[ -1 for _ in range(beats)] for _ in range(len(instruments))]
active_instr = [ 1 for _ in range(len(instruments)) ]




def draw_grid():
    lbox_width = 250    
    bbox_height = 200

    lbox_height = HEIGHT - bbox_height
    bbox_width  = WIDTH

    left_box = pygame.draw.rect(screen, white, [0, 0, lbox_width, lbox_height], 5)
    bottom_box = pygame.draw.rect(screen, white, [0, lbox_height, bbox_width, bbox_height], 5)
    boxes = []
    instrument_boxes = []

    row_hight = lbox_height // len(instruments)
    col_width = (WIDTH - lbox_width) // beats

    for j in range(len(instruments)):
        on = active_instr[j] == 1
        if not on:
            pygame.draw.rect(screen, dark_grey,[0, j*row_hight, lbox_width, row_hight], 0, 0)
        instrument_boxes.append(pygame.draw.rect(screen, white ,[0, j*row_hight, lbox_width, row_hight], 5 , 0))
        screen.blit(label_font.render(instruments[j], True, white if on else light_grey), (30, j*row_hight+30))

        for i in range(beats):
            active = pads[j][i] == 1
            rect_dimensions = [lbox_width+i*col_width, j*row_hight, col_width, row_hight]
            if active:
                pygame.draw.rect(screen, green if on else dark_grey, rect_dimensions, 0, 11)
            else:
                pygame.draw.rect(screen, midgrey, rect_dimensions, 0, 11)
            rect = pygame.draw.rect(screen, gold, rect_dimensions, 2, 2)
            boxes.append((rect,(j, i)))

    # -5 and +10 to make the active beat rectangle wider and more visible
    active_beat_rect = pygame.draw.rect(screen, green, [lbox_width + active_beat * col_width -5, 0, col_width +10, lbox_height], 10, 5)

    # lower menu buttons
    return boxes, instrument_boxes

def beats_change_render(num_beats):
    pygame.draw.rect(screen, dark_grey, [550, HEIGHT-150, 200, 100], 5, 5)
    screen.blit(medium_font.render("Beat count", True, white), (560, HEIGHT-130))
    screen.blit(label_font.render( f"{num_beats}"  , True, white), (610, HEIGHT-90))
    beats_change_rect1 = pygame.draw.rect(screen, dark_grey, [700, HEIGHT-100, 50, 50], 0, 0)
    beats_change_rect2 = pygame.draw.rect(screen, dark_grey, [700, HEIGHT-150, 50, 50], 0, 0)
    screen.blit(medium_font.render("+1", True, white), (710, HEIGHT-100+10))
    screen.blit(medium_font.render("-1", True, white), (715, HEIGHT-150+10))

    return beats_change_rect1, beats_change_rect2 

def bpm_render(bpm):
    bpm_change_rect = []
    bpm_box = pygame.draw.rect(screen, dark_grey, [300, HEIGHT-150, 200, 100], 5, 5)
    bpm_text = medium_font.render(f"{bpm} bpm", True, white)
    screen.blit(bpm_text, (325, HEIGHT-130))
    bpm_text_list = ["<<", "<", ">",  ">>"]
    bpm_text_shift = [0,+8,+10,0]
    for i in range(4):
        bpm_change_rect.append(pygame.draw.rect(screen, dark_grey, [300+i*50, HEIGHT-100, 50, 50], 0, 0))
        screen.blit(medium_font.render(bpm_text_list[i], True, white), (310+bpm_text_shift[i]+i*50, HEIGHT-90))
    return bpm_change_rect

def save_screen_render():
    save_box = pygame.draw.rect(screen, dark_grey, [WIDTH//2-100, HEIGHT//2-50, 200, 100], 0, 5)
    exit_box = pygame.draw.rect(screen, dark_grey, [WIDTH//2-100, HEIGHT//2+60, 200, 40], 0, 5)
    screen.blit(medium_font.render("Save pattern", True, white), (WIDTH//2-70, HEIGHT//2-20))
    screen.blit(medium_font.render("Exit", True, white), (WIDTH//2-30, HEIGHT//2+70))
    return save_box, exit_box

def load_screen_render():
    load_box = pygame.draw.rect(screen, dark_grey, [WIDTH//2-100, HEIGHT//2-50, 200, 100], 0, 5)
    exit_box = pygame.draw.rect(screen, dark_grey, [WIDTH//2-100, HEIGHT//2+60, 200, 40], 0, 5)
    screen.blit(medium_font.render("Load pattern", True, white), (WIDTH//2-70, HEIGHT//2-20))
    screen.blit(medium_font.render("Exit", True, white), (WIDTH//2-30, HEIGHT//2+70))
    return load_box, exit_box


playing = True
bpm = 120
active_length = 0
active_beat = 0
beat_changed = False
save_screen = False
load_screen = False

while running:

    boxes = []
    instrument_boxes = []
    bpm_change_rect = []
    
    timer.tick(fps)
    screen.fill(black)


    if save_screen:
        save_box, exit_box = save_screen_render()


    elif load_screen:
        load_box, exit_box = load_screen_render()

    else:
        boxes, instrument_boxes = draw_grid()
        play_box = pygame.draw.rect(screen, dark_grey, [50, HEIGHT-150, 200, 100], 0, 5)
        screen.blit(label_font.render("Play/Pause", True, white), (60, HEIGHT-130))
        if playing:
            text = medium_font.render("Play", True, light_grey)
            if beat_changed:
                for i in range(len(pads)):
                    if pads[i][active_beat] == 1 and active_instr[i] == 1:
                        sounds[i].play()
                beat_changed = False
        else:
            text = medium_font.render("Pause", True, light_grey)
        screen.blit(text, (60, HEIGHT-90))
    
        bpm_change_rect = bpm_render(bpm)

        beats_change_rect1, beats_change_rect2 = beats_change_render(beats)


        save_pattern_box = pygame.draw.rect(screen, dark_grey, [800, HEIGHT-100, 200, 40], 0,5)
        load_pattern_box = pygame.draw.rect(screen, dark_grey, [800, HEIGHT-150, 200, 40], 0,5)
        screen.blit(medium_font.render("Save pattern", True, white), (810, HEIGHT-90))
        screen.blit(medium_font.render("Load pattern", True, white), (810, HEIGHT-140))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                        

        if event.type == pygame.MOUSEBUTTONUP:
            if save_screen or load_screen:
                if exit_box.collidepoint(event.pos):
                    save_screen = False
                    load_screen = False
                break

            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    pads[coords[0]][coords[1]] *= -1
                    print(f"Clicked on {instruments[coords[0]]} at beat {coords[1]}")
                    # Here you can add sound playing logic
                    pygame.draw.rect(screen, red, boxes[i][0])

            for i in range(len(instrument_boxes)):
                if instrument_boxes[i].collidepoint(event.pos):
                    active_instr[i] *= -1
            
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

            if beats_change_rect1.collidepoint(event.pos):
                beats += 1
                for i in range(len(pads)):
                    pads[i].append(-1)

            if beats_change_rect2.collidepoint(event.pos):
                beats -= 1
                for i in range(len(pads)):
                    pads[i].pop(-1)

            if save_pattern_box.collidepoint(event.pos):
                save_screen = True
                # pattern_name = input("Enter pattern name: ")
                # if pattern_name:
                #     with open(f"patterns/{pattern_name}.txt", "w") as f:
                #         for row in pads:
                #             f.write(" ".join(map(str, row)) + "\n")
                #     print(f"Pattern saved as {pattern_name}.txt")
            
            if load_pattern_box.collidepoint(event.pos):
                load_screen = True
                # pattern_name = input("Enter pattern name to load: ")
                # if pattern_name:
                #     try:
                #         with open(f"patterns/{pattern_name}.txt", "r") as f:
                #             for i, line in enumerate(f):
                #                 pads[i] = list(map(int, line.strip().split()))
                #         print(f"Pattern {pattern_name} loaded.")
                #     except FileNotFoundError:
                #         print(f"Pattern {pattern_name} not found.")

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