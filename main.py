import pygame
import json
import sys

pygame.init()
W, H = 1600, 900
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Ленские Столбы: прототип')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

map_park_img = pygame.image.load('assets/map_park.png').convert()
menu_bg_img = pygame.image.load('assets/menu_bg.png').convert()
stats_bg_img = pygame.image.load('assets/stats_bg.png').convert()
map_park_img = pygame.transform.scale(map_park_img, (W, H))
menu_bg_img = pygame.transform.scale(menu_bg_img, (W, H))
stats_bg_img = pygame.transform.scale(stats_bg_img, (W, H))

zone_images = {
    1: pygame.image.load('assets/zone_1.png').convert(),
    2: pygame.image.load('assets/zone_2.png').convert(),
    3: pygame.image.load('assets/zone_3.png').convert(),
    4: pygame.image.load('assets/zone_4.png').convert(),
    5: pygame.image.load('assets/zone_5.png').convert(),
}
zone_images = {
    i: pygame.transform.scale(
        pygame.image.load(f'assets/zone_{i}.png').convert(), (W, H)
    )
    for i in range(1, 6)
}

with open('plants.json', 'r', encoding='utf-8') as f:
    plants = json.load(f)
zones = [
    {'id': 1, 'name': 'Тропа к столбам', 'rect': pygame.Rect(360, 480, 100, 100)},
    {'id': 2, 'name': 'Долина Туймаада', 'rect': pygame.Rect(485, 300, 100, 100)},
    {'id': 3, 'name': 'Берег Лены', 'rect': pygame.Rect(725, 285, 100, 100)},
    {'id': 4, 'name': 'Смотровая площадка', 'rect': pygame.Rect(1050, 140, 100, 100)},
    {'id': 5, 'name': 'Пик Чекановского', 'rect': pygame.Rect(685, 575, 100, 100)},
]
btn_start = pygame.Rect(150, 335, 300, 70)
btn_exit = pygame.Rect(150, 480, 175, 70)

btn_park_back = pygame.Rect(30, H - 100, 200, 60)

btn_zone_back = pygame.Rect(0, H - 140, 350, 90)

btn_save = pygame.Rect(150, 620, 300, 70)
btn_cancel = pygame.Rect(500, 620, 300, 70)

btn_restart = pygame.Rect(200, 640, 350, 120)
btn_to_menu = pygame.Rect(610, 640, 350, 120)
btn_exit_stats = pygame.Rect(1050, 640, 350, 120)

state = 'menu'
current_zone = None
selected = None
saved = []


def draw_park():
    screen.blit(map_park_img, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    for z in zones:
        zone_plants = [p for p in plants if p['zone'] == z['id']]
        zone_saved = [p for p in zone_plants if p['id'] in saved]
        done = len(zone_plants) > 0 and len(zone_saved) == len(zone_plants)

        r = z['rect']
        if r.collidepoint(mouse_pos) or done:
            color = (80, 200, 80) if done else (255, 255, 255)

    draw_button(btn_park_back, 'В меню', mouse_pos, base_color=(0, 39, 3), hover_color=(51, 71, 26))

def draw_zone():
    z_img = zone_images.get(current_zone)
    if z_img:
        screen.blit(z_img, (0, 0))
    else:
        screen.fill((40, 60, 40))

    zone_plants = [p for p in plants if p['zone'] == current_zone]
    mouse_pos = pygame.mouse.get_pos()
    radius = 75

    for p in zone_plants:
        dx, dy = mouse_pos[0] - p['x'], mouse_pos[1] - p['y']
        is_hovered = (dx ** 2 + dy ** 2) <= radius ** 2

        base_color = (100, 200, 100) if p['id'] in saved else (200, 100, 100)

        alpha = 180 if is_hovered else 100

        surf_size = radius * 2
        button_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)

        pygame.draw.circle(button_surf, (*base_color, alpha), (radius, radius), radius)

        if is_hovered:
            pygame.draw.circle(button_surf, base_color, (radius, radius), radius, width=4)

        screen.blit(button_surf, (p['x'] - radius, p['y'] - radius))


def draw_card():
    screen.fill((33, 65, 22))
    mouse_pos = pygame.mouse.get_pos()
    p = selected

    name = font.render(p['name'], True, (255, 255, 255))
    screen.blit(name, (150, 150))

    fact = font.render('Факт: ' + p['fact'], True, (150, 255, 150))
    screen.blit(fact, (150, 280))

    if p['id'] in saved:
        status = font.render('Уже спасено', True, (255, 220, 100))
        screen.blit(status, (150, 380))
        draw_button(btn_cancel, 'Назад', mouse_pos, base_color=(0, 39, 3), hover_color=(51, 71, 26))
    else:
        draw_button(btn_save, 'Спасти растение', mouse_pos, base_color=(0, 39, 3), hover_color=(51, 71, 26))
        draw_button(btn_cancel, 'Назад', mouse_pos, base_color=(0, 39, 3), hover_color=(51, 71, 26))


def draw_stats():
    screen.blit(stats_bg_img, (0, 0))

    line = font.render(f'Найдено растений: {len(saved)} из {len(plants)}', True, (255, 255, 255))
    screen.blit(line, (W // 2 - line.get_width() // 2, 290))

    mouse_pos = pygame.mouse.get_pos()
    for btn in (btn_restart, btn_to_menu, btn_exit_stats):
        if btn.collidepoint(mouse_pos):
            pass


def draw_menu():
    screen.blit(menu_bg_img, (0, 0))

    btn_start = pygame.Rect(150, 335, 300, 70)
    btn_exit = pygame.Rect(150, 490, 185, 70)
    pygame.draw.rect(screen, (30, 50, 80), (180, 410, 200, 75))

    mouse_pos = pygame.mouse.get_pos()

    for btn in [btn_start, btn_exit]:
        if btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), btn, 2, border_radius=10)


def draw_button(rect, label, mouse_pos, base_color=(50, 90, 140), hover_color=(80, 140, 200)):
    hover = rect.collidepoint(mouse_pos)
    color = hover_color if hover else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
    text = font.render(label, True, (255, 255, 255))
    tx = rect.x + rect.width // 2 - text.get_width() // 2
    ty = rect.y + rect.height // 2 - text.get_height() // 2
    screen.blit(text, (tx, ty))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == 'card':
                    state = 'zone'
                elif state == 'zone':
                    state = 'park'
                elif state == 'park':
                    state = 'menu'
                elif state == 'stats':
                    state = 'menu'
                elif state == 'menu':
                    running = False

            if event.key == pygame.K_SPACE and state == 'card':
                if selected and selected['id'] not in saved:
                    saved.append(selected['id'])
                state = 'zone'
                selected = None

            if event.key == pygame.K_r and state == 'stats':
                saved = []
                selected = None
                current_zone = None
                state = 'park'

            if event.key == pygame.K_m and state == 'stats':
                saved = []
                selected = None
                current_zone = None
                state = 'menu'

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if state == 'menu':
                if btn_start.collidepoint(mx, my):
                    saved = []
                    selected = None
                    current_zone = None
                    state = 'park'
                elif btn_exit.collidepoint(mx, my):
                    running = False


            elif state == 'park':
                if btn_park_back.collidepoint(mx, my):
                    state = 'menu'
                else:
                    for z in zones:
                        if z['rect'].collidepoint(mx, my):
                            current_zone = z['id']
                            state = 'zone'
                            break

            elif state == 'zone':
                if btn_zone_back.collidepoint(mx, my):
                    state = 'park'
                else:
                    zone_plants = [p for p in plants if p['zone'] == current_zone]
                    radius = 75

                    for p in zone_plants:
                        dx, dy = mx - p['x'], my - p['y']
                        if (dx**2 + dy**2) <= radius**2:
                            selected = p
                            state = 'card'
                            break

            elif state == 'card':
                if btn_cancel.collidepoint(mx, my):
                    state = 'zone'
                    selected = None
                elif btn_save.collidepoint(mx, my) and selected and selected['id'] not in saved:
                    saved.append(selected['id'])
                    state = 'zone'
                    selected = None

            elif state == 'stats':
                if btn_restart.collidepoint(mx, my):
                    saved = []
                    selected = None
                    current_zone = None
                    state = 'park'
                elif btn_to_menu.collidepoint(mx, my):
                    saved = []
                    selected = None
                    current_zone = None
                    state = 'menu'
                elif btn_exit_stats.collidepoint(mx, my):
                    running = False

    if state in ('park', 'zone') and len(saved) == len(plants):
        state = 'stats'

    if state == 'menu':
        draw_menu()
    elif state == 'park':
        draw_park()
    elif state == 'zone':
        draw_zone()
    elif state == 'card':
        draw_card()
    elif state == 'stats':
        draw_stats()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
