# Miguel Angel Astor Romero. Created on 7-1-2012. #
###################################################

# Valid game states.
VALID_STATES = { 'INTRO':0, 'MENU':1, 'IN_GAME':2, 'SCORE':3, 'STAY':4, 'QUIT':89}

# Parent class for game states.
class BaseState:
    def input(self):
        """ Empty. Should handle PyGame input. """
        pass

    def update(self):
        """ Empty. Should update the state. Returns a state to transition to. """
        return VALID_STATES['STAY']

    def render(self, canvas):
        """ Empty. Should render this state on the canvas. """
        pass
