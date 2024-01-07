import pygame
import math
import sys
from button import Button

pygame.init()

Width, Height = 800, 600
win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Gravitational Simulator")

PLANET_LIST = {"mercury": [5.53, .38], "venus": [81.5, 0.9], "earth": [100, 1], "mars": [10.7, .38],
               "jupiter": [500, 2.53], "saturn": [400, 1.07], "uranus": [245, 0.89], "neptune": [271, 1.14]}
Planet_Mass = 500
Ship_Mass = 1
G_Force = 5
FPS = 60
Planet_Size = 50
Obj_Size = 5
Vel_scale = 100
Text_Size = 30

BG = pygame.transform.scale(
    pygame.image.load("background.jpg"), (Width, Height))
planet_img = pygame.transform.scale(pygame.image.load(
    "planets/earth.png"), (Planet_Size*2, Planet_Size*2))

menu_rect = pygame.transform.scale(pygame.image.load(
    "assets/Play Rect.png"), (300, 70))
select_rect = pygame.transform.scale(pygame.image.load(
    "assets/Play Rect.png"), (400, 70))

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(planet_img, (self.x - Planet_Size, self.y - Planet_Size))


class spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y

    def draw(self):
        pygame.draw.circle(win, Red, (int(self.x), int(self.y)), Obj_Size)

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G_Force * self.mass * planet.mass) / distance**2

        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = (acceleration * math.cos(angle))
        acceleration_y = (acceleration * math.sin(angle))

        acceleration_x /= self.mass
        acceleration_y /= self.mass

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y


def Gen_ship(location, mouse):
    l_x, l_y = location
    m_x, m_y = mouse
    vel_x = (m_x - l_x) / Vel_scale
    vel_y = (m_y - l_y) / Vel_scale
    obj = spacecraft(l_x, l_y, vel_x, vel_y, Ship_Mass)
    return obj


def start():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(Width // 2, Height // 2, Planet_Mass)
    object = []
    temp_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_pos:
                    obj = Gen_ship(temp_pos, mouse_pos)
                    object.append(obj)
                    temp_pos = None
                else:
                    temp_pos = mouse_pos

        win.blit(BG, (0, 0))

        if temp_pos:
            pygame.draw.line(win, White, temp_pos, mouse_pos, 2)
            pygame.draw.circle(win, Red, temp_pos, Obj_Size)

        for obj in object[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > Width or obj.y < 0 or obj.y > Height
            collision = math.sqrt((obj.x - planet.x) **
                                  2 + (obj.y - planet.y)**2) <= Planet_Size

            if off_screen or collision:
                object.remove(obj)

        planet.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global Ship_Mass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color(
                'dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    Ship_Mass = int(self.text)
                    selection()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 1:
                        self.text += event.unicode
                self.txt_surface = self.font.render(
                    self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def select_mass():
    clock = pygame.time.Clock()
    win.fill("white")
    win.blit(BG, (0, 0))

    MENU_TEXT = get_font(50).render("SELECT PLANET", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(Width // 2, 100))

    INFO_TEXT = get_font(15).render(
        "PRESS ENTER AFTER INPUTTING MASS TO PROCEED", True, "White")
    INFO_RECT = INFO_TEXT.get_rect(center=(Width // 2, 200))

    win.blit(MENU_TEXT, MENU_RECT)
    win.blit(INFO_TEXT, INFO_RECT)
    input_box = InputBox(300, 300, 200, 40)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            input_box.handle_event(event)

        input_box.draw(win)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


def selection():
    while True:
        win.fill("white")
        win.blit(BG, (0, 0))
        global planet_img
        global Planet_Mass
        global G_Force

        input_number = None
        input_str = None

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("SELECT PLANET", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(Width // 2, 50))

        MASS_BUTTON = Button(select_rect, pos=(Width // 2, 150),
                             text_input="SELECT MASS", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        MERCURY_BUTTON = Button(menu_rect, pos=(200, 250),
                                text_input="MERCURY", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        VENUS_BUTTON = Button(menu_rect, pos=(600, 250),
                              text_input="VENUS", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        EARTH_BUTTON = Button(menu_rect, pos=(200, 350),
                              text_input="EARTH", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        MARS_BUTTON = Button(menu_rect, pos=(600, 350),
                             text_input="MARS", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        JUPITER_BUTTON = Button(menu_rect, pos=(200, 450),
                                text_input="JUPITER", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        SATURN_BUTTON = Button(menu_rect, pos=(600, 450),
                               text_input="SATURN", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        URANUS_BUTTON = Button(menu_rect, pos=(200, 550),
                               text_input="URANUS", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        NEPTUNE_BUTTON = Button(menu_rect, pos=(600, 550),
                                text_input="NEPTUNE", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [MASS_BUTTON, MERCURY_BUTTON, VENUS_BUTTON, EARTH_BUTTON, MARS_BUTTON, JUPITER_BUTTON,
                       SATURN_BUTTON, URANUS_BUTTON, NEPTUNE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MASS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_mass()
                if MERCURY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/mercury.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["mercury"][0] * \
                        5, PLANET_LIST["mercury"][1]*5
                    start()
                if VENUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/venus.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["venus"][0] * \
                        5, PLANET_LIST["venus"][1]*5
                    start()
                if EARTH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/earth.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["earth"][0] * \
                        5, PLANET_LIST["earth"][1]*5
                    start()
                if MARS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/mars.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["mars"][0] * \
                        5, PLANET_LIST["mars"][1]*5
                    start()
                if JUPITER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/jupiter.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["jupiter"][0] * \
                        5, PLANET_LIST["jupiter"][1]*5
                    start()
                if SATURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/saturn.png"), (Planet_Size*3, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["saturn"][0] * \
                        5, PLANET_LIST["saturn"][1]*5
                    start()
                if URANUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/uranus.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["uranus"][0] * \
                        5, PLANET_LIST["uranus"][1]*5
                    start()
                if NEPTUNE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    planet_img = pygame.transform.scale(pygame.image.load(
                        "planets/neptune.png"), (Planet_Size*2, Planet_Size*2))
                    Planet_Mass, G_Force = PLANET_LIST["neptune"][0] * \
                        5, PLANET_LIST["neptune"][1]*5
                    start()

        pygame.display.update()


def main():
    while True:
        win.fill("white")
        win.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(Width // 2, 100))

        PLAY_BUTTON = Button(menu_rect, pos=(Width // 2, 250),
                             text_input="SIMULATE", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(menu_rect, pos=(Width // 2, 350),
                                text_input="OPTIONS", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(menu_rect, pos=(Width // 2, 450),
                             text_input="QUIT", font=get_font(Text_Size), base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selection()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
