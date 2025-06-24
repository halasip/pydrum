import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
dark_grey = (50, 50, 50)
light_grey = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyDRUM")

label_font = pygame.font.Font("freesansbold.ttf", 36)

fps = 60
clock = pygame.time.Clock()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(black)


    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
exit()