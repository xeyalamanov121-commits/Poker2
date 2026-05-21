import pygame
import socketio
import sys

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Texas Hold'em - Premium")
clock = pygame.time.Clock()

# Fontlar
FONT_BIG = pygame.font.SysFont("arial", 52, bold=True)
FONT_MED = pygame.font.SysFont("arial", 36)
FONT_SMALL = pygame.font.SysFont("arial", 28)

# Rənglər
BG = (5, 25, 15)
GREEN = (0, 110, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

sio = socketio.Client()
current_room = None
player_name = "Vanqa"
players_in_room = []

# ====================== GUI ELEMENTLƏR ======================
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3, border_radius=12)
    txt = FONT_MED.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))

def main_menu():
    global player_name
    input_box = pygame.Rect(WIDTH//2 - 150, 300, 300, 50)
    active = False
    name = player_name

    while True:
        screen.fill(BG)
        title = FONT_BIG.render("TEXAS HOLD'EM", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                # Buttons
                if 440 < event.pos[0] < 840:
                    if 420 < event.pos[1] < 480:   # Create Room
                        sio.connect('http://localhost:5000')
                        sio.emit("create_room", {"name": name})
                        return "waiting"
                    elif 520 < event.pos[1] < 580: # Join Room
                        sio.connect('http://localhost:5000')
                        return "join"
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    player_name = name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        pygame.draw.rect(screen, (40,40,40), input_box, border_radius=8)
        txt_surface = FONT_MED.render(name, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        draw_button("Yeni Otaq Yarat", 440, 420, 400, 60, (0, 140, 0))
        draw_button("Otağa Qoşul", 440, 520, 400, 60, (0, 100, 180))

        pygame.display.flip()
        clock.tick(60)

# ====================== ƏSAS LOOP ======================
def game_loop():
    global current_room
    running = True
    state = "menu"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG)

        if state == "menu":
            state = main_menu()
        elif state == "waiting":
            title = FONT_BIG.render("Gözləyirsiniz...", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            if current_room:
                room_txt = FONT_MED.render(f"Otaq ID: {current_room}", True, WHITE)
                screen.blit(room_txt, (WIDTH//2 - room_txt.get_width()//2, 300))

        pygame.display.flip()
        clock.tick(60)

    sio.disconnect()
    pygame.quit()

@sio.event
def room_created(data):
    global current_room
    current_room = data["room_id"]
    print(f"Otaq yaradıldı: {current_room}")

@sio.event
def update_players(data):
    global players_in_room
    players_in_room = data["players"]

if __name__ == "__main__":
    game_loop()
