class Game:
    def __init__(self, id):
        self.id = id
        self.player_1_selected = False
        self.player_2_selected = False
        self.ready = False
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.player_index = {0: self.player_1_selected, 1: self.player_2_selected}

        self.selection_to_index = {'ROCK': 0, 'PAPER': 1, 'SCISSORS': 2}
        self.game_table = [['t', 1, 0],
                            [0, 't', 1],
                            [1, 0, 't']]

    def get_player_move(self, player):
        """
        :param player: [0, 1] 0 : player one | 1: player two
        :return: Move
        """
        return self.moves[player]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.player_1_selected = True
        elif player == 1:
            self.player_2_selected = True

    def connected(self):
        return self.ready

    def both_players_selected(self):
        return self.player_1_selected and self.player_2_selected

    def results(self, player_1_selection, player_2_selection):
        """
        :param player_1_selection: String, "ROCK"
        :param player_2_selection: String, "PAPER"
        :return: 0 or 1 for winner, 't' for tie
        """
        player_1_selection_index = self.selection_to_index[player_1_selection]
        player_2_selection_index = self.selection_to_index[player_2_selection]
        return self.game_table[player_1_selection_index][player_2_selection_index]

    def set_ready(self, bool):
        self.ready = bool

    def winner(self):
        return self.results(self.moves[0], self.moves[1])

    def reset_selected(self):
        self.player_1_selected = False
        self.player_2_selected = False
