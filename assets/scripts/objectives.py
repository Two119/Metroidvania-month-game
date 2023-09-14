from assets.scripts.dialogue import *
def level_1_obj(player):
    if player.coins == 1:
        return True
def level_2_obj(player):
    pass
class ObjectiveManager:
    def __init__(self):
        self.objective_funcs_dict = {0: level_1_obj, 1:level_2_obj, 1:level_2_obj}
        self.rect = pygame.Rect(780/2, 520, 500, 200)
        self.texts = ["Hello and welcome to Shiftania! This is the tutorial level. Click on this box to show full text instantly and then press enter to move on to next instruction. Read them all!", "Move left and right using A and D, jump using the spacebar. You can jump two blocks far and two blocks high.", "The core mechanic of this game is shapeshifting, that is changing tiles into other types of tiles.", "Your inventory below has the tiles you can shapeshift other tiles into. Select an item in inventory by clicking on it or pressing numbers 1-5.", "To shapeshift, press shift and then right click on the tile you want to shapeshift. It will be transformed into the tile selected in your inventory.", "Remember, you have a limited number of times you can shapeshift tiles! Go to the shop to buy more shapeshifts or to buy new tiles or shields.", "Lastly, you can collect coins in the game and use them in the shop to buy stuff as mentioned before. You can go to the shop from the pause menu or main menu.", "Also, you can open pause menu by clicking on the top right button or pressing escape. Enjoy the game!"]
        self.current = 0
        self.dialogue_channel = pygame.Channel(6)
        self.dialogue_sfx = pygame.mixer.Sound("assets/Audio/dialogue.ogg")
    def update(self, renderer):
        if renderer.level == 0:
            if not hasattr(self, "dialogues"):
                self.dialogues = [Dialogue(renderer.font, text, 4, 500, 125) for text in self.texts]
            if self.current != -1:
                self.dialogues[self.current].update(renderer)
                if self.dialogues[self.current].finished:
                    self.dialogue_channel.fadeout(1000)
                else:
                    if not self.dialogue_channel.get_busy():
                        self.dialogue_channel.set_volume(renderer.coin_channel.get_volume())
                        self.dialogue_channel.play(self.dialogue_sfx)
            if self.dialogues[self.current].done and self.current != -1:
                self.current += 1
            if self.current >= len(self.dialogues):
                self.current = -1
        return False
