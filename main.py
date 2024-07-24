import pygame
import random
from boids import Boids

# constants
BG = (236, 242, 255)
FPS = 60
WIDTH, HEIGHT = 1000, 800
N_BOIDS = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Flocking Simulation')
pygame.display.set_icon(pygame.image.load('./assets/icon.png'))
clock = pygame.time.Clock()

boids = []
for _ in range(N_BOIDS):
    boids.append(Boids(screen, WIDTH, HEIGHT))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = not start


    screen.fill(BG)
 
    for boid in boids:
        boid.flock(boids)
        boid.update(boids)
        boid.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()