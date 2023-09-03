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
                    renderer.queue[0].tiles_unlocked.append(6)
                    if saved["spike_bought"]:
                        renderer.queue[0].tiles_unlocked.append(117)
                    if saved["hiddenspike_bought"]:
                        renderer.queue[0].tiles_unlocked.append(118)
                    if saved["swing_bought"]:
                        renderer.queue[0].tiles_unlocked.append(121)
                    if saved["fire_bought"]:
                        renderer.queue[0].tiles_unlocked.append(116)
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
                    renderer.queue[0].tiles_unlocked.append(6)
                    if saved["spike_bought"]:
                        renderer.queue[0].tiles_unlocked.append(117)
                    if saved["hiddenspike_bought"]:
                        renderer.queue[0].tiles_unlocked.append(118)
                    if saved["swing_bought"]:
                        renderer.queue[0].tiles_unlocked.append(121)
                    if saved["fire_bought"]:
                        renderer.queue[0].tiles_unlocked.append(116)
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
        spike_bought = "false"
        hiddenspike_bought = "false"
        swing_bought = "false"
        fire_bought = "false"
        if 117 in renderer.queue[0].tiles_unlocked:
            spike_bought = "true"
        if 118 in renderer.queue[0].tiles_unlocked:
            hiddenspike_bought = "true"
        if 121 in renderer.queue[0].tiles_unlocked:
            swing_bought = "true"
        if 116 in renderer.queue[0].tiles_unlocked:
            fire_bought = "true"
        tiles_unlocked_str = '"spike_bought":'+str(spike_bought)+","+'"hiddenspike_bought":'+str(hiddenspike_bought)+","+'"swing_bought":'+str(swing_bought)+","+'"fire_bought":'+str(fire_bought)+","
        print(renderer.queue[0].tiles_unlocked)
        dat = '{"coins":'+str(0)+","+'"level":'+str(renderer.level)+","+'"deaths":'+str(renderer.queue[0].deaths)+","+tiles_unlocked_str+'"volume":'+str(renderer.coin_channel.get_volume())+","+'"fps":'+str(renderer.def_frame)+"}"
        b = base64.b64encode(bytes(dat, 'utf-8'))
        base64_str = b.decode('utf-8')
        if web:
            platform.window.localStorage.setItem("dat", base64_str)
        else:
            f = open(self.file_path, "w")
            f.write(base64_str)
            f.close()