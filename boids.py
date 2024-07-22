import pygame
import pygame.gfxdraw
import random
import math

# constants
RADIUS = 5
SEPARATION_RADIUS = 30
ALIGN_RADIUS = 100
COHESION_RADIUS = 40

COLORS = [
    pygame.Color(102, 123, 198, 200),  # Purple
    pygame.Color(163, 67, 67, 200),  # Red
    pygame.Color(70, 133, 133, 200)   # Green
]

class Boids:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.pos = pygame.math.Vector2(random.uniform(0, self.width), random.uniform(0, self.height))
        self.vel = self.getRandomVelocity()
        self.acc = pygame.math.Vector2()
        self.maxForce = 0.1  # Max steering force
        self.maxSpeed = 4    # Max speed
        self.color = random.choice(COLORS)

    def align(self, boids):
        steer = pygame.math.Vector2()
        total = 0
        
        for boid in boids:
            if boid != self:
                distance = self.pos.distance_to(boid.pos)
                if distance < ALIGN_RADIUS:
                    steer += boid.vel
                    total += 1

        if total > 0:
            steer /= total
            steer = steer.normalize() * self.maxSpeed - self.vel
            if steer.length() > self.maxForce:
                steer = steer.normalize() * self.maxForce

        return steer

    def cohesion(self, boids):
        center_of_mass = pygame.math.Vector2()
        total = 0
        
        for boid in boids:
            if boid != self:
                distance = self.pos.distance_to(boid.pos)
                if distance < COHESION_RADIUS:
                    center_of_mass += boid.pos
                    total += 1

        if total > 0:
            center_of_mass /= total
            steer = center_of_mass - self.pos
            if steer.length() > self.maxForce:
                steer = steer.normalize() * self.maxSpeed - self.vel
                steer = steer.normalize() * self.maxForce

            return steer
        return pygame.math.Vector2()

    def separation(self, boids):
        steer = pygame.math.Vector2()
        total = 0
        
        for boid in boids:
            if boid != self:
                distance = self.pos.distance_to(boid.pos)
                if distance < SEPARATION_RADIUS:
                    diff = self.pos - boid.pos
                    if distance > 0:  # Avoid division by zero
                        diff /= distance  # Weight by distance
                    steer += diff
                    total += 1

        if total > 0:
            steer /= total
            if steer.length() > 0:  # Avoid normalization of zero vector
                steer = steer.normalize() * self.maxSpeed - self.vel
                if steer.length() > self.maxForce:
                    steer = steer.normalize() * self.maxForce

        return steer

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        self.acc = alignment + cohesion + separation

    def getRandomVelocity(self):
        angle = random.uniform(0, 2*math.pi)
        magnitude = random.uniform(2, 4)
        vel_vector = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * magnitude
        
        return vel_vector

    def handleBoundaryCollision(self):
        if self.pos.x > self.width:
            self.pos.x = 0
            self.color = random.choice(COLORS)

        elif self.pos.x < 0:
            self.pos.x = self.width
            self.color = random.choice(COLORS)

        if self.pos.y > self.height:
            self.pos.y = 0
            self.color = random.choice(COLORS)

        elif self.pos.y < 0:
            self.pos.y = self.height
            self.color = random.choice(COLORS)


    def setColor(self, boids):
        color_counts = [0] * len(COLORS)

        for boid in boids:
            if boid != self:
                distance = self.pos.distance_to(boid.pos)
                if distance < ALIGN_RADIUS:
                    if boid.color in COLORS:
                        color_index = COLORS.index(boid.color)
                        color_counts[color_index] += 1

        max_count = max(color_counts)
        if max_count > 0:
            common_color_index = color_counts.index(max_count)
            self.color = COLORS[common_color_index]


    def update(self, boids):
        # self.flock(boids)

        self.vel += self.acc
        if self.vel.length() > self.maxSpeed:
            self.vel = self.vel.normalize() * self.maxSpeed
        self.pos += self.vel
        self.acc = pygame.math.Vector2()
        
        self.handleBoundaryCollision()
        self.setColor(boids)

    def draw(self):
        # Calculate the points of the triangle
        angle = math.atan2(self.vel.y, self.vel.x)
        p1 = self.pos + pygame.math.Vector2(math.cos(angle), math.sin(angle)) * (RADIUS * 2)
        p2 = self.pos + pygame.math.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * RADIUS
        p3 = self.pos + pygame.math.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * RADIUS
        
        # Draw the polygon with transparency
        pygame.gfxdraw.filled_polygon(self.screen, [p1, p2, p3], self.color)
        pygame.gfxdraw.aapolygon(self.screen, [p1, p2, p3], self.color)
