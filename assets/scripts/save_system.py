from assets.scripts.core_funcs import *
class SaveSystem:
    def __init__(self):
        dir_path = '%s\\Shiftania\\' %  os.environ['APPDATA'] 
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.file_path = '%ssave.json' % dir_path
        if not os.path.exists(self.file_path):
            open(self.file_path, "x").close()
    def load(self, renderer):
        if web:
            if platform.window.localStorage.getItem("dat") != None:
                saved = base64.b64decode(platform.window.localStorage.getItem("dat")).decode()
                saved = json.loads(str(saved))
                renderer.level = int(saved["level"])
                if len(renderer.queue) > 0:
                    renderer.queue[0].coins = int(saved["coins"])
                    renderer.queue[0].deaths = int(saved["deaths"])
                    renderer.queue[0].tile_unlocked = [saved["tiles_unlocked"][i]*1 for i in range(len(saved["tiles_unlocked"]))]
                    renderer.coin_channel.set_volume(float(saved["volume"]))
                    renderer.queue[0].channel.set_volume(float(saved["volume"]))
                    renderer.def_frame = int(saved["fps"])
        else:
            if open(self.file_path, "r").readlines() == []:
                pass
            else:
                saved = base64.b64decode(open(self.file_path, "r").readlines()[0]).decode()
                saved = json.loads(str(saved))
                renderer.level = int(saved["level"])
                if len(renderer.queue) > 0:
                    renderer.queue[0].coins = int(saved["coins"])
                    renderer.queue[0].deaths = int(saved["deaths"])
                    renderer.queue[0].tile_unlocked = [saved["tiles_unlocked"][i]*1 for i in range(len(saved["tiles_unlocked"]))]
                    renderer.coin_channel.set_volume(float(saved["volume"]))
                    renderer.queue[0].channel.set_volume(float(saved["volume"]))
                    renderer.def_frame = int(saved["fps"])
    def reset(self):
        if web:
            platform.window.localStorage.clear()
        else:
            open(self.file_path, "w").close()
    def update(self, renderer):
        #if (not renderer.queue[0].is_alive):
        tiles_unlocked_list = "["
        for tile in renderer.queue[0].tiles_unlocked:
            if tile != renderer.queue[0].tiles_unlocked[len(renderer.queue[0].tiles_unlocked)-1]:
                tiles_unlocked_list = tiles_unlocked_list + str(tile) + ", "
            else:
                tiles_unlocked_list = tiles_unlocked_list + str(tile) + "]"
        dat = '{"coins":'+str(renderer.queue[0].coins)+","+'"level":'+str(renderer.level)+","+'"deaths":'+str(renderer.queue[0].deaths)+","+'"tiles_unlocked":'+tiles_unlocked_list+","+'"volume":'+str(renderer.coin_channel.get_volume())+","+'"fps":'+str(renderer.def_frame)+"}"
        b = base64.b64encode(bytes(dat, 'utf-8'))
        base64_str = b.decode('utf-8')
        if web:
            platform.window.localStorage.setItem("dat", base64_str)
        else:
            f = open(self.file_path, "w")
            f.write(base64_str)
            f.close()