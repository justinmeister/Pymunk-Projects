"""The purpose of this example is to demonstrate a ball
rolling down a series of ramps."""

import os, sys
import pygame as pg
import pymunk as pk

SCREEN_SIZE = (800, 600)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
START_X = 100
START_Y = 500
GRAVITY = (0.0, -400)


class Ball(object):
    """Ball that rolls down ramps"""
    def __init__(self, x, y):
        self.mass = 1
        self.radius = 14
        self.inertia = pk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pk.Body(self.mass, self.inertia)
        self.body.position = x, y
        self.shape = pk.Circle(self.body, self.radius)

    def update(self):
        """Update ball information by converting pymunk coordinates
        into pygame coordinates"""
        self.x = int(self.body.position.x)
        self.y = int(self.body.position.y * -1 + SCREEN_SIZE[1])

    def draw(self, surface):
        """Draws ball to a surface"""
        circle_center = (self.x, self.y)
        radius = int(self.radius)
        pg.draw.circle(surface, ORANGE, circle_center, radius)


class Ramp(object):
    """Ramp that the ball rolls on"""
    def __init__(self, name):
        self.body = pk.Body()
        self.name = name
        self.shape = self.set_dimensions()

    def set_dimensions(self):
        """Set the specific dimensions for the created ramp"""
        if self.name == 'ramp 1':
            self.body.position = (200, 400)
            shape = pk.Segment(self.body, (-150, 100), (150, 0), 10)
        elif self.name == 'ramp 2':
            self.body.position = (550, 350)
            shape = pk.Segment(self.body, (-150, 0), (150, 100), 10)
        elif self.name == 'ramp 3':
            self.body.position = (200, 300)
            shape = pk.Segment(self.body, (-150, 100), (150, 0), 10)
        elif self.name == 'ramp 4':
            self.body.position = (550, 250)
            shape = pk.Segment(self.body, (-150, 0), (150, 100), 10)
        elif self.name == 'ramp 5':
            self.body.position = (200, 200)
            shape = pk.Segment(self.body, (-150, 100), (150, 0), 10)
        elif self.name == 'ramp 6':
            self.body.position = (550, 150)
            shape = pk.Segment(self.body, (-150, 0), (150, 100), 10)
            
        return shape
        

    def draw(self, surface):
        """Draws ramp to a surface"""
        pymunk_point_a = self.body.position + self.shape.a
        pymunk_point_b = self.body.position + self.shape.b
        point_a = self.convert_to_pg_coordinates(pymunk_point_a)
        point_b = self.convert_to_pg_coordinates(pymunk_point_b)
        
        pg.draw.lines(surface, (0, 0, 50), False, [point_a, point_b], 23)

    def convert_to_pg_coordinates(self, pos):
        """Converts pymunk coordinates to pygame coordinates"""
        return int(pos.x), int(-pos.y+SCREEN_SIZE[1])


class Control(object):
    """Controls the game"""
    def __init__(self):
        self.screen = self.setup_pygame()
        self.screen_rect = self.screen.get_rect()
        self.space = pk.Space()
        self.space.gravity = GRAVITY
        self.done = False
        self.fps = 60
        self.current_time = 0.0
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.add_ramps_to_space()
        self.add_ball_to_space()

    def setup_pygame(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        pg.display.set_caption('Balls and Ramps')
        screen = pg.display.set_mode(SCREEN_SIZE)

        return screen

    def add_ramps_to_space(self):
        """Add the ramps to build the level and space for physics"""
        ramp1 = Ramp('ramp 1')
        ramp2 = Ramp('ramp 2')
        ramp3 = Ramp('ramp 3')
        ramp4 = Ramp('ramp 4')
        ramp5 = Ramp('ramp 5')
        ramp6 = Ramp('ramp 6')
        self.ramps = [ramp1, ramp2, ramp3, ramp4, ramp5, ramp6]

        for ramp in self.ramps:
            self.space.add(ramp.shape)

    def add_ball_to_space(self):
        """Add the ball to the level and space for physics"""
        self.ball = Ball(START_X, START_Y)
        self.space.add(self.ball.body, self.ball.shape)

    def update(self):
        """Updates game"""
        while not self.done:
            self.get_user_input()
            self.current_time = pg.time.get_ticks()
            self.screen.fill((255, 255, 255))
            self.space.step(1/50.0)
            self.ball.update()
            self.draw()
            self.check_if_ball_off_screen()
            pg.display.update()
            self.clock.tick(self.fps)

    def get_user_input(self):
        """Get user events and keys pressed"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def draw(self):
        """Draws all sprites"""
        self.ball.draw(self.screen)
        for ramp in self.ramps:
            ramp.draw(self.screen)

    def check_if_ball_off_screen(self):
        """Checks if ball is no longer on screen.  If so,
        the ball is deleted, and a new one is created"""
        if self.ball.x > SCREEN_SIZE[0] or self.ball.x < 0:
            self.reset_ball_position()
        elif self.ball.y > SCREEN_SIZE[1] or self.ball.y < 0:
            self.reset_ball_position()

    def reset_ball_position(self):
        """Deletes ball and resets it to original position"""
        self.space.remove(self.ball.shape, self.ball.body)
        self.ball = Ball(START_X, START_Y)
        self.space.add(self.ball.body, self.ball.shape)



if __name__ == '__main__':
    game = Control()
    game.update()
    pg.quit()
    sys.exit()












