from assets.scripts.core_funcs import *
class Psycho:
    def __init__(self, position, orig_tile, spikesheet):
        self.pos = position
        self.cur_tile = [orig_tile[0]*1, orig_tile[1]*1]
        self.orig_tile = [orig_tile[0]*1, orig_tile[1]*1]
        self.spikesheet = spikesheet
        self.spike_frame = 0
