from assets.scripts.core_funcs import *
class Shop:
    def  __init__(self, renderer):
        self.tiles = [117, 129, 138, 139, 118, 136, 137, 135, 121, 116]
        self.tile_names_dict = {117: "Spike (Up)", 129: "Spike (Down)", 138: "Spike (Right)", 139: "Spike (Left)", 118: "Hidden Spike (Up)", 135: "Hidden Spike (Down)", 136: "Hidden Spike (Right)", 137: "Hidden Spike (Left)", 121: "Swinging Axe", 116: "Fire platform"}
        self.tile_images = [i.copy() for i in renderer.spikesheet.sheet[0]]
        for i in renderer.spikesheet.sheet[0]:
            self.tile_images.append(i.copy())
        
    def update(self, renderer):
        pass