from assets.scripts.core_funcs import *
def level_1_obj(player):
    if player.coins == 1:
        return True
def level_2_obj(player):
    pass
class ObjectiveManager:
    def __init__(self):
        self.objective_funcs_dict = {0: level_1_obj, 1:level_2_obj}
    def update(self, renderer):
        return self.objective_funcs_dict[renderer.level](renderer.queue[0])
