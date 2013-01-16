############################################
# Created on 1-16-2013. Miguel Angel Astor #
############################################
import constants

class Player:
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.alive = True
        self.clamp_to_zero = True

    def get_id():
        return self.id

    def is_alive(self):
        return self.alive

    def set_alive(self, alive):
        self.alive = alive

    def revive(self):
        self.alive = True

    def kill(self):
        self.alive = False

    def clamps_to_zero(self):
        return self.clamp_to_zero

    def set_clamp_to_zero(self, clamp):
        self.clamp_to_zero = clamp

    def get_score(self):
        return self.score

    def inc_score(self, amount):
        self.score += amount

    def inc_score_by_one(self):
        self.score += 1

    def dec_score(self, amount):
        if self.clamp_to_zero:
            self.score = max(self.score - amount, 0)
        else:
            self.score -= amount

    def dec_score_by_one(self):
        self.dec_score(1)

    def set_score(self, value):
        self.score = value

    def reset_score(self):
        self.score = 0

PLAYERS = {}
for i in range(constants.NUM_PLAYERS):
    PLAYERS[i + 1] = Player(i + 1)
