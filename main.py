import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cozy Tea Cup & Rising Steam Simulator")
clock = pygame.time.Clock()

# Couleurs (Thème Cosy Nocturne & Pastel)
BG_COLOR = (18, 20, 32)
TABLE_COLOR = (30, 26, 42)
CUP_COLOR = (245, 238, 248)
CUP_SHADOW = (210, 198, 220)
SAUCER_COLOR = (228, 218, 236)
TEXT_COLOR = (245, 242, 255)
GRAY = (135, 130, 155)

TEA_TYPES = [
    {"name": "Miel Doré", "color": (235, 165, 55), "accent": (255, 225, 120)},
    {"name": "Matcha Doux", "color": (135, 205, 110), "accent": (195, 245, 165)},
    {"name": "Hibiscus Rose", "color": (225, 85, 130), "accent": (255, 165, 195)},
    {"name": "Lavande Nuit", "color": (145, 120, 225), "accent": (205, 190, 255)}
]

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

class SteamParticle:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-1.6, -0.8)
        self.radius = random.uniform(4.0, 8.0)
        self.phase = random.uniform(0, math.pi * 2)
        self.life = random.randint(90, 150)
        self.max_life = self.life

    def update(self, mouse_pos):
        self.phase += 0.06
        swirl = math.sin(self.phase) * 0.45

        # Légère interaction avec le curseur de la souris
        if mouse_pos[1] > 80:
            dx = self.x - mouse_pos[0]
            dy = self.y - mouse_pos[1]
            dist = math.hypot(dx, dy)
            if 0 < dist < 95:
                push = (95 - dist) / 95 * 0.18
                self.vx += (dx / dist) * push
                self.vy += (dy / dist) * push * 0.5

        self.x += self.vx + swirl
        self.y += self.vy
        self.vx *= 0.96
        self.radius += 0.035
        self.life -= 1

class Topping:
    def __init__(self, x, y, kind):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind  # "mint" ou "lemon"
        self.angle = random.uniform(0, math.pi * 2)
        self.spin_speed = random.uniform(-0.03, 0.03)
        self.bob_phase = random.uniform(0, math.pi * 2)

    def update(self, surface_x, surface_y):
        self.bob_phase += 0.05
        self.angle += self.spin_speed
        target_x = surface_x + math.sin(self.bob_phase) * 14
        target_y = surface_y + math.cos(self.bob_phase * 0.8) * 3
        self.x += (target_x - self.x) * 0.08
        self.y += (target_y - self.y) * 0.08

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        if self.kind == "mint":
            pygame.draw.ellipse(surface, (95, 215, 125), (ix - 9, iy - 5, 18, 10))
            pygame.draw.line(surface, (55, 155, 85), (ix - 7, iy), (ix + 7, iy), 2)
        else:
            pygame.draw.circle(surface, (255, 225, 85), (ix, iy), 8)
            pygame.draw.circle(surface, (255, 245, 175), (ix, iy), 5)

# Position de la tasse
cup_center_x = WIDTH // 2
cup_base_y = HEIGHT - 155
tea_index = 0

steam_particles = []
toppings = [
    Topping(cup_center_x - 22, cup_base_y - 45, "mint"),
    Topping(cup_center_x + 25, cup_base_y - 43, "lemon")
]

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mouse_pos[1] > 80:
                kind = "mint" if len(toppings) % 2 == 0 else "lemon"
                toppings.append(Topping(mouse_pos[0], mouse_pos[1], kind))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                tea_index = (tea_index + 1) % len(TEA_TYPES)
            elif event.key == pygame.K_r:
                tea_index = 0
                steam_particles = []
                toppings = [
                    Topping(cup_center_x - 22, cup_base_y - 45, "mint"),
                    Topping(cup_center_x + 25, cup_base_y - 43, "lemon")
                ]

    current_tea = TEA_TYPES[tea_index]
    tea_surface_y = cup_base_y - 45

    # Générer de nouvelles particules de vapeur au-dessus du thé
    if random.random() < 0.65:
        spawn_x = cup_center_x + random.uniform(-42, 42)
        steam_particles.append(SteamParticle(spawn_x, tea_surface_y - 5))

    # Mettre à jour la vapeur
    for p in steam_particles[:]:
        p.update(mouse_pos)
        if p.life <= 0:
            steam_particles.remove(p)

    # Mettre à jour les garnitures flottantes
    for top in toppings:
        top.update(cup_center_x, tea_surface_y)

    # --- RENDU GRAPHIQUE ---
    screen.fill(BG_COLOR)

    # Table cosy en bas de l'écran
    pygame.draw.rect(screen, TABLE_COLOR, (0, HEIGHT - 115, WIDTH, 115))
    pygame.draw.line(screen, (65, 55, 85), (0, HEIGHT - 115), (WIDTH, HEIGHT - 115), 2)

    # Soucoupe
    pygame.draw.ellipse(screen, SAUCER_COLOR, (cup_center_x - 115, cup_base_y + 36, 230, 34))
    pygame.draw.ellipse(screen, (190, 178, 205), (cup_center_x - 82, cup_base_y + 42, 164, 20))

    # Anse de la tasse
    pygame.draw.arc(screen, CUP_SHADOW, (cup_center_x + 58, cup_base_y - 28, 48, 52), -math.pi * 0.45, math.pi * 0.45, 10)

    # Corps de la tasse
    pygame.draw.rect(screen, CUP_COLOR, (cup_center_x - 72, cup_base_y - 45, 144, 88), border_bottom_left_radius=36, border_bottom_right_radius=36)
    pygame.draw.ellipse(screen, CUP_SHADOW, (cup_center_x - 72, cup_base_y - 55, 144, 22))

    # Surface du thé chaud
    pygame.draw.ellipse(screen, current_tea["color"], (cup_center_x - 62, tea_surface_y - 7, 124, 16))
    pygame.draw.ellipse(screen, current_tea["accent"], (cup_center_x - 42, tea_surface_y - 4, 84, 8))

    # Garnitures (menthe / citron)
    for top in toppings:
        top.draw(screen)

    # Vapeur montante
    for p in steam_particles:
        alpha = max(0, min(140, int((p.life / p.max_life) * 130)))
        r = max(2, int(p.radius))
        s_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(s_surf, (235, 240, 255, alpha), (r + 2, r + 2), r)
        screen.blit(s_surf, (int(p.x) - r - 2, int(p.y) - r - 2))

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("COZY TEA CUP — VAPEUR & INFUSION DOUCE", True, TEXT_COLOR)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    stats_txt = font_small.render(f"Infusion : {current_tea['name']} | Garnitures : {len(toppings)}", True, current_tea["accent"])
    screen.blit(stats_txt, (40, 42))

    inst_txt = font_small.render("CLIC GAUCHE : Ajouter menthe/citron | T : Changer d'infusion | SOURIS : Brasser la vapeur | R : Reset", True, GRAY)
    screen.blit(inst_txt, (WIDTH - inst_txt.get_width() - 40, 42))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()