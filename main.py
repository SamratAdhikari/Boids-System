import pygame
from Boid import Boid


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# constants
BLACK = (0, 0, 0)
FPS = 60
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
N_BOIDS = 200

boids = []
for _ in range(N_BOIDS):
    boids.append(Boid(screen, WIDTH, HEIGHT))

while True:
    [exit() for _ in pygame.event.get() if _.type == pygame.KEYDOWN and _.key == pygame.K_ESCAPE]

    screen.fill(BLACK)

    for boid in boids:
        boid.flock(boids)
        boid.update()
        boid.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()