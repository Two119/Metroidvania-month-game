from assets.scripts.core_funcs import *
class Camera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, win.get_width()-((12*4)+15), win.get_height()-(80+((16*4)+17)))
        self.window_rect = pygame.Rect(0, 0, win.get_width(), win.get_height())
        self.bigger_window_rect = pygame.Rect(-320, -320, win.get_width()+320, win.get_height()+320)
        self.transition_vel = [0, 0]
        self.cam_change = [0, 0]
        self.checking = True
        self.cycles = 0
        self.dir = -1
        self.spawn_pos = [[64, 5*64], [64, 4.5*64], [104, 360]]
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            self.transition_frames = 30*renderer.dt
            self.transition_speed = (self.rect.w/renderer.def_frame)*(renderer.dt)
            if hasattr(renderer.queue[0], "rect"):
                if self.rect.collidepoint(renderer.queue[0].rect.x, 10):
                    pass
                else:
                    if renderer.queue[0].pos[0] > 0:
                        renderer.init_render_pos[renderer.level][0] -= ((self.rect.w-self.spawn_pos[renderer.level][0])/64)
                        for obj in renderer.queue:
                            if obj != None:
                                obj.pos[0] -= (self.rect.w-self.spawn_pos[renderer.level][0])
                        for fireball in renderer.bullet_manager.bullets:
                            fireball[0][0]-= (self.rect.w-self.spawn_pos[renderer.level][0])
                        for spike in renderer.spikes:
                            spike[renderer.attr_dict["pos"]][0] -= (self.rect.w-self.spawn_pos[renderer.level][0])
                        self.cam_change[0] -= (self.rect.w-self.spawn_pos[renderer.level][0])
                        renderer.queue[0].dust_pos[0] -= (self.rect.w-self.spawn_pos[renderer.level][0])
                    else:
                        renderer.init_render_pos[renderer.level][0] += ((self.rect.w-self.spawn_pos[renderer.level][0])/64)
                        for obj in renderer.queue:
                            if obj != None:
                                obj.pos[0] += (self.rect.w-self.spawn_pos[renderer.level][0])
                        for fireball in renderer.bullet_manager.bullets:
                            fireball[0][0]+=(self.rect.w-self.spawn_pos[renderer.level][0])
                        for spike in renderer.spikes:
                            spike[renderer.attr_dict["pos"]][0] += (self.rect.w-self.spawn_pos[renderer.level][0])
                        self.cam_change[0] += (self.rect.w-self.spawn_pos[renderer.level][0])
                        renderer.queue[0].dust_pos[0] += (self.rect.w-self.spawn_pos[renderer.level][0])
                if self.rect.collidepoint(10, renderer.queue[0].rect.y):
                    pass
                else:        
                    if renderer.queue[0].pos[1] > 0:
                        renderer.init_render_pos[renderer.level][1] -= ((self.rect.h)/64)
                        for obj in renderer.queue:
                                obj.pos[1] -= (self.rect.h)
                        for fireball in renderer.bullet_manager.bullets:
                            fireball[0][1] -= (self.rect.h)
                        for spike in renderer.spikes:
                            spike[renderer.attr_dict["pos"]][1] -= (self.rect.h)
                        self.cam_change[1] -= (self.rect.h)
                        renderer.queue[0].dust_pos[1] -= (self.rect.h)
                    else:
                        renderer.init_render_pos[renderer.level][1] += ((self.rect.h)/64)
                        for obj in renderer.queue:
                            obj.pos[1] += (self.rect.h)
                        for fireball in renderer.bullet_manager.bullets:
                            fireball[0][1] += (self.rect.h)
                        for spike in renderer.spikes:
                            spike[renderer.attr_dict["pos"]][1] += (self.rect.h)
                        self.cam_change[1] += (self.rect.h)
                        renderer.queue[0].dust_pos[1] += (self.rect.h)