import pygame
from pygame import mixer
import yaml
import os

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
fps = 30
class PyDrum:



    def __init__(self):
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PyDrum")


        self.label_font = pygame.font.Font('freesansbold.ttf', 32)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 24)
        self.beats = 8
        self.timer = pygame.time.Clock()

        # Import sound files
        # for each file in sounds directory, load the sound
        self.sounds = []
        self.instruments = []
        kitidx = 1 
        for file in sorted(os.listdir(f'sounds/kit{kitidx}')):
            sound_name = file.split('.')[0]
            self.sounds.append(mixer.Sound(os.path.join(f'sounds/kit{kitidx}', file)))
            self.instruments.append(sound_name.title())

        pygame.mixer.set_num_channels(len(self.sounds)*3)

        self.pads = [[ -1 for _ in range(self.beats)] for _ in range(len(self.instruments))]
        self.active_instr = [ 1 for _ in range(len(self.instruments)) ]




    def draw_grid(self, active_beat):
        lbox_width = 250    
        bbox_height = 200

        lbox_height = HEIGHT - bbox_height
        bbox_width  = WIDTH

        left_box = pygame.draw.rect(self.screen, white, [0, 0, lbox_width, lbox_height], 5)
        bottom_box = pygame.draw.rect(self.screen, white, [0, lbox_height, bbox_width, bbox_height], 5)
        boxes = []
        instrument_boxes = []

        row_hight = lbox_height // len(self.instruments)
        col_width = (WIDTH - lbox_width) // self.beats

        for j in range(len(self.instruments)):
            on = self.active_instr[j] == 1
            if not on:
                pygame.draw.rect(self.screen, dark_grey,[0, j*row_hight, lbox_width, row_hight], 0, 0)
            instrument_boxes.append(pygame.draw.rect(self.screen, white ,[0, j*row_hight, lbox_width, row_hight], 5 , 0))
            self.screen.blit(self.label_font.render(self.instruments[j], True, white if on else light_grey), (30, j*row_hight+30))

            for i in range(self.beats):
                active = self.pads[j][i] == 1
                rect_dimensions = [lbox_width+i*col_width, j*row_hight, col_width, row_hight]
                if active:
                    pygame.draw.rect(self.screen, green if on else dark_grey, rect_dimensions, 0, 11)
                else:
                    pygame.draw.rect(self.screen, midgrey, rect_dimensions, 0, 11)
                rect = pygame.draw.rect(self.screen, gold, rect_dimensions, 2, 2)
                boxes.append((rect,(j, i)))

        # -5 and +10 to make the active beat rectangle wider and more visible
        active_beat_rect = pygame.draw.rect(self.screen, green, [lbox_width + active_beat * col_width -5, 0, col_width +10, lbox_height], 10, 5)

        # lower menu buttons
        return boxes, instrument_boxes

    def beats_change_render(self,num_beats):
        pygame.draw.rect(self.screen, dark_grey, [550, HEIGHT-150, 200, 100], 5, 5)
        self.screen.blit(self.medium_font.render("Beat count", True, white), (560, HEIGHT-130))
        self.screen.blit(self.label_font.render( f"{num_beats}"  , True, white), (610, HEIGHT-90))
        beats_change_rect1 = pygame.draw.rect(self.screen, dark_grey, [700, HEIGHT-100, 50, 50], 0, 0)
        beats_change_rect2 = pygame.draw.rect(self.screen, dark_grey, [700, HEIGHT-150, 50, 50], 0, 0)
        self.screen.blit(self.medium_font.render("+1", True, white), (710, HEIGHT-100+10))
        self.screen.blit(self.medium_font.render("-1", True, white), (715, HEIGHT-150+10))

        return beats_change_rect1, beats_change_rect2 

    def bpm_render(self,bpm):
        bpm_change_rect = []
        bpm_box = pygame.draw.rect(self.screen, dark_grey, [300, HEIGHT-150, 200, 100], 5, 5)
        bpm_text = self.medium_font.render(f"{bpm} bpm", True, white)
        self.screen.blit(bpm_text, (325, HEIGHT-130))
        bpm_text_list = ["<<", "<", ">",  ">>"]
        bpm_text_shift = [0,+8,+10,0]
        for i in range(4):
            bpm_change_rect.append(pygame.draw.rect(self.screen, dark_grey, [300+i*50, HEIGHT-100, 50, 50], 0, 0))
            self.screen.blit(self.medium_font.render(bpm_text_list[i], True, white), (310+bpm_text_shift[i]+i*50, HEIGHT-90))
        return bpm_change_rect

    def save_screen_render(self,saved_beats, pattern_name):
        save_box = pygame.draw.rect(self.screen, dark_grey, [WIDTH//2-100, HEIGHT//2-50, 200, 100], 0, 5)
        exit_box = pygame.draw.rect(self.screen, dark_grey, [WIDTH//2-100, HEIGHT//2+60, 200, 40], 0, 5)
        self.screen.blit(self.label_font.render("Saving " + pattern_name, True, white), (WIDTH//2-90, HEIGHT//2-90))
        self.screen.blit(self.medium_font.render("Save pattern", True, white if pattern_name not in saved_beats.keys() else red), (WIDTH//2-70, HEIGHT//2-20))
        self.screen.blit(self.medium_font.render("Exit", True, white), (WIDTH//2-30, HEIGHT//2+70))
        return save_box, exit_box

    def load_screen_render(self,saved_beats, pattern_name):
        patterns_box = []
        load_box = pygame.draw.rect(self.screen, dark_grey, [WIDTH//2-100, HEIGHT//2-50, 200, 100], 0, 5)
        exit_box = pygame.draw.rect(self.screen, dark_grey, [WIDTH//2-100, HEIGHT//2+60, 200, 40], 0, 5)
        self.screen.blit(self.label_font.render("Loading " + pattern_name, True, white), (WIDTH//2-90, HEIGHT//2-90))
        self.screen.blit(self.label_font.render("Available self.beats", True, white), (25, 25))
        for i,name in enumerate(saved_beats):
            patterns_box.append(pygame.draw.rect(self.screen, white, [50, 70+i*50, 250, 40], 1, 0))
            self.screen.blit(self.label_font.render("- "+name, True, green if pattern_name == name else white), (50, 75+i*50))
        self.screen.blit(self.medium_font.render("Load pattern", True, white if pattern_name in saved_beats.keys() else red), (WIDTH//2-70, HEIGHT//2-20))
        self.screen.blit(self.medium_font.render("Exit", True, white), (WIDTH//2-30, HEIGHT//2+70))
        return load_box, exit_box, patterns_box

    def run(self):
        playing = True
        bpm = 120
        active_length = 0
        active_beat = 0
        beat_changed = False
        save_screen = False
        load_screen = False
        saved_beats = {}
        pattern_name = ""


        boxes = []
        while self.running:
            instrument_boxes = []
            bpm_change_rect = []
            patterns_box = []
            
            self.timer.tick(fps)
            self.screen.fill(black)


            if save_screen:
                save_box, exit_box = self.save_screen_render(saved_beats, pattern_name)


            elif load_screen:
                load_box, exit_box, patterns_box = self.load_screen_render(saved_beats, pattern_name)

            else:
                boxes, instrument_boxes = self.draw_grid(active_beat)
                play_box = pygame.draw.rect(self.screen, dark_grey, [50, HEIGHT-150, 200, 100], 0, 5)
                self.screen.blit(self.label_font.render("Play/Pause", True, white), (60, HEIGHT-130))
                if playing:
                    text = self.medium_font.render("Play", True, light_grey)
                    if beat_changed:
                        for i in range(len(self.pads)):
                            if self.pads[i][active_beat] == 1 and self.active_instr[i] == 1:
                                self.sounds[i].play()
                        beat_changed = False
                else:
                    text = self.medium_font.render("Pause", True, light_grey)
                self.screen.blit(text, (60, HEIGHT-90))
            
                bpm_change_rect = self.bpm_render(bpm)

                beats_change_rect1, beats_change_rect2 = self.beats_change_render(self.beats)


                save_pattern_box = pygame.draw.rect(self.screen, dark_grey, [800, HEIGHT-100, 200, 40], 0,5)
                load_pattern_box = pygame.draw.rect(self.screen, dark_grey, [800, HEIGHT-150, 200, 40], 0,5)
                self.screen.blit(self.medium_font.render("Save pattern", True, white), (810, HEIGHT-90))
                self.screen.blit(self.medium_font.render("Load pattern", True, white), (810, HEIGHT-140))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.TEXTINPUT:
                    if save_screen or load_screen:
                        if event.text.isprintable():
                            pattern_name += event.text
                        elif event.key == pygame.K_BACKSPACE:
                            pattern_name = pattern_name[:-1]

                if event.type == pygame.MOUSEBUTTONUP:
                    if (save_screen or load_screen) and exit_box.collidepoint(event.pos):
                        save_screen = False
                        load_screen = False
                        
                    if save_screen and save_box.collidepoint(event.pos):
                        saved_beats[pattern_name]={}
                        
                        saved_beats[pattern_name]["tempo"]=bpm
                        saved_beats[pattern_name]["instruments"]=self.active_instr.copy()
                        saved_beats[pattern_name]["beats"]=self.beats
                        saved_beats[pattern_name]["pattern"]=[item.copy() for item in self.pads]
                        if pattern_name:
                            with open(f"patterns/saved_beats.txt", "w") as f:
                                # for name in saved_beats.keys(self):
                                #     f.write(f"beat name: {name}, tempo: {saved_beats[pattern_name]}, self.instruments: {saved_beats[pattern_name]}, self.beats: {saved_beats[pattern_name]} pattern: {saved_beats[pattern_name]=}")
                                f.write(yaml.safe_dump(saved_beats, sort_keys=False))
                        pattern_name = ""
                        save_screen = False
                    
                    if load_screen and load_box.collidepoint(event.pos):
                        if pattern_name not in saved_beats.keys():
                            try:
                                with open(f"patterns/saved_beats.txt", "r") as f:
                                    saved_beats = yaml.safe_load(f)
                                print(f"Pattern saved_beats loaded.")
                            except FileNotFoundError:
                                print(f"Pattern saved_beats not found.")
                        if pattern_name in saved_beats.keys():
                            self.bpm = saved_beats[pattern_name]["tempo"]
                            self.active_instr = saved_beats[pattern_name]["instruments"].copy()
                            self.beats = saved_beats[pattern_name]["beats"]
                            self.pads = [item.copy() for item in saved_beats[pattern_name]["pattern"]]
                            load_screen = False
                        pattern_name = ""

                    for i in range(len(boxes)):
                        if boxes[i][0].collidepoint(event.pos):
                            coords = boxes[i][1]
                            self.pads[coords[0]][coords[1]] *= -1
                    
                    for i in range(len(patterns_box)):
                        if patterns_box[i].collidepoint(event.pos):
                            pattern_name = list(saved_beats.keys())[i]
                            bpm = saved_beats[pattern_name]["tempo"]
                            self.active_instr = saved_beats[pattern_name]["instruments"].copy()
                            self.beats = saved_beats[pattern_name]["beats"]
                            self.pads = [item.copy() for item in saved_beats[pattern_name]["pattern"]]
                            pattern_name = ""
                            load_screen = False

                    for i in range(len(instrument_boxes)):
                        if instrument_boxes[i].collidepoint(event.pos):
                            self.active_instr[i] *= -1
                    
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
                        self.beats += 1
                        for i in range(len(self.pads)):
                            self.pads[i].append(-1)

                    if beats_change_rect2.collidepoint(event.pos):
                        self.beats -= 1
                        for i in range(len(self.pads)):
                            self.pads[i].pop(-1)


                    if save_pattern_box.collidepoint(event.pos):
                        save_screen = True

                    if load_pattern_box.collidepoint(event.pos):
                        load_screen = True

            beat_length = fps * 60 // bpm
            if playing:
                if active_length < beat_length:
                    active_length += 1
                else:
                    active_length = 0
                    beat_changed = True
                    if active_beat < self.beats - 1:
                        active_beat += 1
                    else:
                        active_beat = 0

            pygame.display.flip()



if __name__ == '__main__':
    app = PyDrum()
    app.run()