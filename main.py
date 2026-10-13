import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ленские Столбы: редкие растения")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((30, 40, 30))  # тёмно-зелёный фон
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()