from core_funcs import *
class Camera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, win_size[0], win_size[1])
        self.checking = True
        self.cycles = 0
        self.dir = -1
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            self.transition_frames = 35*renderer.dt
            self.transition_speed = (win_size[0]/renderer.def_frame)*(renderer.dt)
            if hasattr(renderer.queue[0], "rect"):
                if self.rect.contains(renderer.queue[0].rect) and self.checking:
                    pass
                
                else:
                    if self.cycles >= self.transition_frames:
                        self.checking = True
                        self.cycles = 0
                        self.dir = -1
                        for obj in renderer.queue:
                            if hasattr(obj, "moving"):
                                obj.moving = True
                                #if hasattr(obj, "vel"):
                                #    obj.vel = [0, 0]
                        return
                    if self.checking:
                        for obj in renderer.queue:
                            if hasattr(obj, "moving"):
                                obj.moving = False
                        if renderer.queue[0].pos[0] > 0:
                            self.dir = 0
                        else:
                            self.dir = 1
                    self.checking = False
                        
                    if self.dir == 0:
                        renderer.init_render_pos[renderer.level][0] -= ((win_size[0]/2)/64)/self.transition_frames
                        for obj in renderer.queue:
                            
                                obj.pos[0] -= (win_size[0]/2)/self.transition_frames
                    elif self.dir == 1:
                        renderer.init_render_pos[renderer.level][0] += ((win_size[0]/2)/64)/self.transition_frames
                        for obj in renderer.queue:
                            obj.pos[0] += (win_size[0]/2)/self.transition_frames
                    self.cycles += 1