from math import sin, cos, pi
from itertools import islice

import pygame

WHITE = (255,255,255)

def square(i, theta):
    n = i * 2 + 1
    radius = 50 * (4/(n*pi))
    x = radius * cos(n * theta)
    y = radius * sin(n * theta)
    return x, y, radius

def sawtooth(i, theta):
    n = i + 1
    radius = 50 * (2/(n*pi * (-1 if n%2 == 0 else 1)))
    x = radius * cos(n * theta)
    y = radius * sin(n * theta)
    return x, y, abs(radius)

class Game:
    def __init__(self):
        pass

    def run(self):
        self._init()
        while self._running:
            self._read_inputs()
            self._update()
            self._produce_outputs()
        self._shutdown()

    def _init(self):
        pygame.init()
        self._screen = pygame.display.set_mode((600, 400))
        self._clock = pygame.time.Clock()
        self._running = True
        self._time = 0
        self._steps = 1
        self._wave = []
        self._func = square
        self._up_button = pygame.Rect(50, 50, 30, 30)
        self._dn_button = pygame.Rect(50, 100, 30, 30)
        self._square_button = pygame.Rect(150, 50, 30, 30)
        self._saw_button = pygame.Rect(150, 100, 30, 30)

    def _shutdown(self):
        pass

    def _read_inputs(self):
        self._bup = 0
        self._bpos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self._bup = event.button
                self._bpos = event.pos


    def _update(self):
        self._clock.tick(60)

        if self._bup == 1:
            if self._up_button.collidepoint(self._bpos):
                self._steps += 1
            if self._dn_button.collidepoint(self._bpos):
                if self._steps > 1:
                    self._steps -= 1
            if self._square_button.collidepoint(self._bpos):
                self._func = square
            if self._saw_button.collidepoint(self._bpos):
                self._func = sawtooth

        dx = 150
        dy = 250
        radius = 50

        x = 0
        y = 0
        self._els = []
        self._dots = []
        for i in range(self._steps):
            prevx = x
            prevy = y

            nx, ny, radius = self._func(i, self._time)
            x += nx
            y += ny

            el = pygame.Rect(0, 0, radius*2, radius*2)
            el.centerx = dx+prevx
            el.centery = dy+prevy
            self._els.append(el)
            dot = pygame.Rect(0, 0, 8, 8)
            dot.centerx = dx + x
            dot.centery = dy + y
            self._dots.append(dot)

        self._wave.append(y)

        dx += 200
        self._draw_wave = [
                (dx+i, dy+v) for (i, v) in enumerate(
                    islice(reversed(self._wave), 200))
                ]

        self._time += 0.05

    def _produce_outputs(self):
        self._screen.fill((0, 0, 0))
        for (el, dot) in zip(self._els, self._dots):
            if el.width > 2:
                pygame.draw.ellipse(self._screen, WHITE, el, 1)
            pygame.draw.ellipse(self._screen, WHITE, dot)
            pygame.draw.line(self._screen, WHITE, el.center, dot.center)

        if len(self._draw_wave) > 1:
            pygame.draw.lines(self._screen, WHITE, False, self._draw_wave)
        pygame.draw.line(self._screen, WHITE,
                dot.center, self._draw_wave[0])

        pygame.draw.rect(self._screen, WHITE, self._up_button, 1)
        pygame.draw.line(self._screen, WHITE,
                (self._up_button.centerx+10, self._up_button.centery),
                (self._up_button.centerx-10, self._up_button.centery))
        pygame.draw.line(self._screen, WHITE,
                (self._up_button.centerx, self._up_button.centery+10),
                (self._up_button.centerx, self._up_button.centery-10))

        pygame.draw.rect(self._screen, WHITE, self._dn_button, 1)
        pygame.draw.line(self._screen, WHITE,
                (self._dn_button.centerx+10, self._dn_button.centery),
                (self._dn_button.centerx-10, self._dn_button.centery))

        x = 90
        y = 50
        for i in range(self._steps):
            pygame.draw.line(self._screen, WHITE, (x, y), (x, y))
            x += 5
            if x >= 140:
                x = 90
                y += 5

        pygame.draw.rect(self._screen, WHITE, self._square_button, 1)
        pygame.draw.lines(self._screen, WHITE, False,[
                (self._square_button.centerx+10, self._square_button.centery+10),
                (self._square_button.centerx+10, self._square_button.centery-10),
                (self._square_button.centerx-10, self._square_button.centery-10),
                (self._square_button.centerx-10, self._square_button.centery+10)
            ])

        pygame.draw.rect(self._screen, WHITE, self._saw_button, 1)
        pygame.draw.lines(self._screen, WHITE, False,[
                (self._saw_button.centerx+10, self._saw_button.centery+10),
                (self._saw_button.centerx+10, self._saw_button.centery-10),
                (self._saw_button.centerx-10, self._saw_button.centery+10)
            ])

        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()

