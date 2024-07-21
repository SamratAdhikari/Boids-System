import pygame
import random
import math

# constants
WHITE = (200, 200, 200)
RADIUS = 5
PERCEPTION_RADIUS = 100

class Boid:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.pos = pygame.math.Vector2(random.uniform(0, self.width), random.uniform(0, self.height))
        self.vel = self.getRandomVelocity()
        self.acc = pygame.math.Vector2()
        self.maxForce = 0.2
        self.maxSpeed = 4

    def align(self, boids):
        steer = pygame.math.Vector2()
        n_boids = 0
        
        for boid in boids:
            if boid != self:
                distance = self.pos.distance_to(boid.pos)
                if distance < PERCEPTION_RADIUS:
                    steer += boid.vel
                    n_boids += 1

        if n_boids > 0:
            steer /= n_boids
            steer -= self.vel
            if steer.length() > 0:
                steer.clamp_magnitude(self.maxSpeed)
                try:
                    steer.scale_to_length(self.maxForce)
                except:
                    pass

        return steer

    def flock(self, boids):
        alignment = self.align(boids)
        self.acc = alignment

    def getRandomVelocity(self):
        angle = random.uniform(0, 2*math.pi)
        magnitude = random.uniform(2, 4)
        vel_vector = (magnitude * math.cos(angle), magnitude * math.sin(angle))
        
        return pygame.math.Vector2(*(vel_vector))

    def handleBoundaryCollision(self):
        if self.pos.x > self.width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.width
        if self.pos.y > self.height:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.height

    def update(self):
        self.pos += self.vel
        self.vel += self.acc
        self.handleBoundaryCollision()
        self.acc = pygame.math.Vector2()


    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (self.pos.x, self.pos.y), RADIUS)