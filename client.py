import pygame
from network import Network
import pickle

pygame.font.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.font = pygame.font.SysFont('Arial', 40)
        self.text_surface = self.font.render(self.text, True, pygame.Color('black'))

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        window.blit(self.text_surface, (self.x + self.width // 2 - self.text_surface.get_width() // 2,
                                        self.y + self.height // 2 - self.text_surface.get_height() // 2))

    def click(self, pos):
        x, y = pos[0], pos[1]
        print(self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height)
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


def draw(game, player):
    window.fill(pygame.Color("White"))
    if not (game.connected()):
        font = pygame.font.SysFont("Arial", 80)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        window.blit(text, (window_width / 2 - text.get_width() / 2, window_height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("Your Move", True, (0, 255, 255))
        window.blit(text, (80, 200))

        text = font.render("Opponent's Move", True, (0, 255, 255))
        window.blit(text, (380, 200))
        player_1_selection = game.get_player_move(0)
        player_2_selection = game.get_player_move(1)
        if game.both_players_selected():
            text1 = font.render(player_1_selection, True, (0, 0, 0))
            text2 = font.render(player_2_selection, True, (0, 0, 0))
        else:
            if game.player_1_selected and player == 0:
                text1 = font.render(player_1_selection, True, (0, 0, 0))
            elif game.player_1_selected:
                text1 = font.render("Locked In", True, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", True, (0, 0, 0))

            if game.player_2_selected and player == 1:
                text2 = font.render(player_2_selection, True, (0, 0, 0))
            elif game.player_2_selected:
                text2 = font.render("Locked In", True, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (0, 0, 0))

        if player == 0:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))
        else:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))

        for button in buttons:
            button.draw(window)


def draw_winner(text, window):
    font = pygame.font.SysFont('Arial', 40)
    text_surface = font.render(text, True, pygame.Color("Black"))
    (x, y) = (window_width / 2 - text_surface.get_width() / 2, window_height / 2 - text_surface.get_height() / 2)
    window.blit(text_surface, (x, y))


buttons = [Button("ROCK", 50, 500, (0, 0, 0)), Button("SCISSORS", 250, 500, pygame.Color("Red")),
           Button("PAPER", 450, 500, pygame.Color("Green"))]


def determine_winner(game_winner, player):
    if game_winner == player:
        return "You Won!"
    elif game_winner == "t":
        return "Tie!"
    else:
        return "You Lost"


def determine_button_clicked(mouse_position, game, player, network):
    for button in buttons:
        if button.click(mouse_position) and game.connected():
            # if we are the player who has not selected yet, allow us to select a button
            if player == 0:
                if not game.player_1_selected:
                    network.send(button.text)
            else:
                if not game.player_2_selected:
                    network.send(button.text)


def main():
    running = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_player())
    print(f"You are player {player}")
    while running:
        clock.tick(60)
        try:
            game = network.send("get")
        except:
            running = False
            print("Error: No game received ( get ) ")
            break
        if game.both_players_selected():
            draw(game, player)
            pygame.time.delay(500)
            try:
                network.send("reset")
            except Exception as e:
                print(e)
                print("Error: No game received ( reset ) ")
                break

            text = determine_winner(game.winner(), player)
            draw_winner(text, window)
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                determine_button_clicked(mouse_position, game, player, network)

        draw(game, player)
        pygame.display.update()


def menu_screen():
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 60)
    while running:
        clock.tick(60)
        window.fill((128, 128, 128))
        text = font.render("Click to Play!", True, (255,0,0))
        window.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

    main()


while True:
    menu_screen()

