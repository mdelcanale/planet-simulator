import pygame
import math


pygame.init()

WIDTH, HEIGHT = 1440, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")  # Nome

VENUS = (255, 255, 255)
SUN = (255, 255, 0)
EARTH = (0, 20, 220)
MARS = (188, 39, 50)
MERCURY = (168, 169, 169)
JUPITER = (152, 86, 0)
BG = (255, 0, 255)

FONT = pygame.font.SysFont("sans-serif", 14)
FONT_PLANET = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100 / AU
    TIMESTEP = 3600*24*3

    def __init__(self, x, y, radius, color, mass, name:str) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0


    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, VENUS)
            win.blit(distance_text, (x - distance_text.get_width() /
                     1.5, y - distance_text.get_width() / 1.5 ))
            name_text = FONT_PLANET.render(f"{self.name}",1, BG)
            win.blit(name_text, (x - name_text.get_width() /
                     0.5, y - name_text.get_width() / 0.5))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self. x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, SUN, 1.98892 * 10**30, None)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 12, EARTH, 5.9742 * 10**24, 'Terra')
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 8, MARS, 6.39 * 10**23, 'Marte')
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 5, MERCURY, 3.30 * 10**23, 'Mercúrio')
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 9, VENUS, 4.8685 * 10**24, 'Vênus')
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 15, JUPITER, 1.898 * 10**27, 'Júpiter')
    jupiter.y_vel = 13.1 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
