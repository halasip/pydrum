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

fps = 60
timer = pygame.time.Clock()

def draw_grid():
    left_box = pygame.draw.rect(screen, white, [0, 0, 300, HEIGHT-300], 5)
    bottom_box = pygame.draw.rect(screen, white, [0, HEIGHT-300, WIDTH, 300], 5)
    boxes = []
    colors = [dark_grey, white, light_grey]
    for idx,sound in enumerate(["Kick", "Snare", "Hi-Hat", "Bass Drum", "Kick"]):
        # box = pygame.draw.rect(screen, colors.pop(0), [0, 0, 200, 200], 5)
        # boxes.append(box)
        # colors.append(light_grey)
        text = label_font.render(sound, True, green)
        screen.blit(text, (20, idx*100+30))
        pygame.draw.rect(screen, light_grey, [0, idx*100+10, 300, 75], 5)



running = True
while running:
    timer.tick(fps)
    screen.fill(black)

    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()