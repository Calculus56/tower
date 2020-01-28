from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import CoreLabel    # How you draw text on the Canvas
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.config import Config
import random
import time
ran_back = random.randint(1, 100)
bg_img = ''
if ran_back < 70:  # 70%
    bg_img = "images/mBg_imgs/green.png"
elif 70 <= ran_back < 95:  # 15%
    bg_img = 'images/mBg_imgs/Lava2.jpg'
elif 95 <= ran_back <= 100:  # 5%
    bg_img = 'images/theBoys.png'
c = 0
walkCount = 0
gob_rt_cnt = 0
gob_lt_cnt = 0
money = 0
weapon = 0
person = 0
# True left, False Right
direction = True
weap_rt = 'images/throw_knfRT.png'
weap_lt = 'images/throw_knfLT.png'
lft_imgs = ['images\Main_body2\L1.png', 'images\Main_body2\L2.png', 'images\Main_body2\L3.png', 'images\Main_body2\L4.png', 'images\Main_body2\L5.png', 'images\Main_body2\L6.png', 'images\Main_body2\L7.png', 'images\Main_body2\L8.png']
rgt_imgs = ['images\Main_body2\R1.png', 'images\Main_body2\R2.png', 'images\Main_body2\R3.png', 'images\Main_body2\R4.png', 'images\Main_body2\R5.png', 'images\Main_body2\R6.png', 'images\Main_body2\R7.png', 'images\Main_body2\R8.png']
gob_rt_imgs = ['images\orc_body\R1.png', 'images\orc_body\R2.png', 'images\orc_body\R3.png', 'images\orc_body\R4.png', 'images\orc_body\R5.png', 'images\orc_body\R6.png', 'images\orc_body\R7.png', 'images\orc_body\R8.png']
gob_lt_imgs = ['images\orc_body\L1.png', 'images\orc_body\L2.png', 'images\orc_body\L3.png', 'images\orc_body\L4.png', 'images\orc_body\L5.png', 'images\orc_body\L6.png', 'images\orc_body\L7.png', 'images\orc_body\L8.png']
popupWindow = None
weap_size = [15, 15]
move_lt = False
move_rt = False
attack = False
Config.set('graphics', 'fullscreen', 1)
assassin_lives = 0
wizard_lives = 0
original_w = False
original_a = False
weap_durability = 1
pause = 1
f = open('images/saved_data.txt', 'r')
lines = f.readlines()
money = int(lines[0].strip('\n'))
assassin_lives = int(lines[1].strip('\n'))
wizard_lives = int(lines[2].strip('\n'))
weap_rt = lines[3].strip('\n')
weap_lt = lines[4].strip('\n')
w_width = int((lines[5].strip('\n'))[0:2])
w_height = int((lines[5].strip('\n'))[3:5])
weap_size = [w_width, w_height]
weap_durability = int(lines[6].strip('\n'))
f.close()
#Window.size = (700, 600)
class P(FloatLayout):
    def dismiss(self):
        del_popup()

    def sword_blue(self):
        global weapon
        weapon = 1
        ap = game
        ap.buy()
    def wizard(self):
        global person
        global wizard_lives
        wizard_lives = 1
        person = 1
        ap = game
        ap.buy()
    def assassin(self):
        global person
        global assassin_lives
        assassin_lives = 1
        person = 2
        ap = game
        ap.buy()

def del_popup():
    global popupWindow
    global pause
    pause = 1
    popupWindow.dismiss()
def show_popup(self):
    global popupWindow
    global pause
    pause = 0
    show = P()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))

    popupWindow.open()

def set_move_ltT(self):
    global move_lt
    move_lt = True
def set_move_ltF(self):
    global move_lt
    move_lt = False
def set_move_rtT(self):
    global move_rt
    move_rt = True
def set_move_rtF(self):
    global move_rt
    move_rt = False
def set_attackT(self):
    global attack
    attack = True
def set_attackF(self):
    global attack
    attack = False
def save(self):
    global money
    f = open('images/saved_data.txt', 'w')
    f.write(str(money)+'\n')
    f.write(str(assassin_lives)+'\n')
    f.write(str(wizard_lives)+'\n')
    f.write(weap_rt+'\n')
    f.write(weap_lt+'\n')
    f.write(str(weap_size[0])+' '+str(weap_size[1])+'\n')
    f.write(str(weap_durability))


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._goldLabel = CoreLabel(text="Gold: " + str(money), font_size=15)
        self._goldLabel.refresh()
        self._gold = money
        self._tHealthLabel = CoreLabel(text="Health: 100", font_size=20)
        self._tHealthLabel.refresh()
        self._tHealth = 100
        self._pHealth = 10

        self.register_event_type("on_frame")  # This is from the super thing that we are inheriting

        with self.canvas.before:
            Rectangle(source=bg_img, pos=(0, 0), size=(Window.width, Window.height))
            self._gold_instruction = Rectangle(texture=self._goldLabel.texture, pos=(0, Window.height - 100), size=self._goldLabel.texture.size)
            self._tHealth_instruction = Rectangle(texture=self._tHealthLabel.texture, pos=(Window.width / 2 - (130 / 2)+10, 260), size=self._tHealthLabel.texture.size)
        with self.canvas.after:
            Rectangle(source="images/Shop.png", pos=(0, Window.height - 75), size=(100, 50))
        btn1 = Button(text="Shop", pos=(0, Window.height - 90), background_color=(0, 0, 0, 0))
        btn1.bind(on_press=show_popup)
        self.add_widget(btn1)
        btn_save = Button(text="Save", pos=((Window.width-self.size[0]), Window.height-self.size[1]))
        btn_save.bind(on_press=save)
        self.add_widget(btn_save)

        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame, 0)

        self.sound = SoundLoader.load("Music\Ominous Music.mp3")
        self.sound.play()

        Clock.schedule_interval(self.spawn_enemies, 2)
        self.last_time_a = 0
        self.last_time_w = 0
        Clock.schedule_interval(self.check_time, 0.1)

    def check_time(self, dt):
        global original_a
        global original_w
        global pause
        if pause == 1:
            if time.time()-self.last_time_a >= 1:
                if assassin_lives == 1 and original_a:
                    self.add_entity(AssassinLT((((Window.width/2)-200), 0)))
                self.last_time_a = time.time()
            if time.time()-self.last_time_w >= 3:
                if wizard_lives == 1:
                    self.add_entity(fireball(((Window.width / 2) + 190, 5)))
                self.last_time_w = time.time()

    def spawn_enemies(self, dt):
        global pause
        if pause == 1:
            for i in range(2):
                random_spd = random.randint(25, 50)
                self.add_entity(EnemyLT((Window.width, 0), random_spd))
                self.add_entity(EnemyRT((0, 0), random_spd))


    def _on_frame(self, dt):
        self.dispatch("on_frame", dt)

    def on_frame(self, dt):
        pass

    @property
    def gold(self):    # Score getter
        return self._gold

    @gold.setter
    def gold(self, value):     # Score setter
        self._gold = value
        self._goldLabel.text = "Gold: " + str(value)
        self._goldLabel.refresh()
        self._gold_instruction.texture = self._goldLabel.texture
        self._gold_instruction.size = self._goldLabel.size

    @property
    def tHealth(self):  # Score getter
        return self._tHealth

    @tHealth.setter
    def tHealth(self, value):  # Score setter
        self._tHealth = value
        self._tHealthLabel.text = "Health: " + str(value)
        self._tHealthLabel.refresh()
        self._tHealth_instruction.texture = self._tHealthLabel.texture
        self._tHealth_instruction.size = self._tHealthLabel.size

    def set_wizard(self):
        rect1 = Rectangle(pos=(((Window.width / 2) + 150), 0), size=(50, 50), source='images/wizard frames/tile023.png')
        self.add_entity(WizardRT((((Window.width / 2) + 150), 0)))
        self.canvas.add(rect1)

    def set_assassin(self):
        rect2 = Rectangle(pos=(((Window.width / 2) - 200), 0), size=(50, 50), source='images/Bad guy frames/tile015.png')
        self.add_entity(AssassinLT((((Window.width / 2) - 200), 0)))
        self.canvas.add(rect2)

    def buy(self):
        global money
        global weapon
        global person
        global weap_rt
        global weap_lt
        global weap_size
        global durability
        if weapon == 1 and self._gold >= 10:
            global durability
            weapon = 0
            game.gold -= 10
            money -= 10
            durability = 2
            weap_rt = 'images/swordB_RT.png'
            weap_lt = 'images/swordB_LT.png'
            weap_size[0] = 30
            weap_size[1] = 30
        if person == 1 and self._gold >= 100:
            person = 0
            game.gold -= 100
            money -= 100
            #rect1 = Rectangle(pos=(((Window.width / 2) + 150), 0), size=(50, 50), source='images/wizard frames/tile023.png')
            self.add_entity(WizardRT((((Window.width/2)+150), 0)))
            #self.canvas.add(rect1)
        if person == 2 and self._gold >= 100:
            person = 0
            game.gold -= 100
            money -= 100
            rect2 = Rectangle(pos=(((Window.width/2) - 200), 0), size=(50, 50), source='images/Bad guy frames/tile015.png')
            self.add_entity(AssassinLT((((Window.width/2)-200), 0)))
            self.canvas.add(rect2)

    def add_entity(self, entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)

    def remove_entity(self, entity):
        if entity in self._entities:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)

    def collides(self, e1, e2, value):  # Gets two tuples of rectangles position and returns a boolean if they collide.
        r1x = e1.pos[0]+value
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]+value
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]
        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):  # The bottom left has the position then the height adds to the value to see if the bottom left of the second picture is collding.
            return True
        else:
            return False

    def colliding_entities(self, entity, dir):
        result = set()
        for e in self._entities:
            if self.collides(e, entity, dir) and e != entity:  # e == entry checks if the entity is colliding with itself.
                result.add(e)
        return result



    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

game = GameWidget()

class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (50, 50)
        self._source = 'images/img_blank.png'
        self._instruction = Rectangle(pos=self._pos, size=self._size, source=self._source)
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._instruction.source = self._source
class AssassinLT(Entity):
    def __init__(self, pos, speed=200):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.source = "images/Bad guy frames/tile015.png"
        self.size = (50, 50)
        self.last_time = 0
        game.bind(on_frame=self.move_step)
    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
    def move_step(self, sender, dt):
        global original_a
        global pause
        if pause == 1:
            for e in game.colliding_entities(self, -20):
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                print(e)
                if isinstance(e, EnemyRT):
                    if time.time() - self.last_time >= 0.3:
                        self.last_time = time.time()
                        self.source = "images/badGuy_punch.png"
                    else:
                        if time.time() - self.last_time >= 0.1:
                            self.source = "images/Bad guy frames/tile015.png"
class WizardRT(Entity):
    def __init__(self, pos, speed=200):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.source = "images/wizard frames/tile023.png"
        self.size = (50, 50)

class KnifeRT(Entity):
    global weap_rt
    global weap_size
    def __init__(self, pos, speed=300):
        super().__init__()
        sound = SoundLoader.load("Music/throwing noise.mp3")
        sound.play()
        self._speed = speed
        self.pos = pos
        self.size = (15, 15)
        self.source = weap_rt
        self.dur_used = 0
        game.bind(on_frame=self.move_step)
    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        self.source = weap_rt
        self.size = (weap_size[0], weap_size[1])
        global pause
        if pause == 1:
            # check for collision/out of bounds
            if self.pos[0]+Window.width < Window.width or self.pos[0] > Window.width:
                self.stop_callbacks()
                game.unbind(on_frame=self.move_step)
                game.remove_entity(self)
                return
            for e in game.colliding_entities(self, 60):
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                if isinstance(e, EnemyLT):
                    global money
                    global weap_durability
                    game.add_entity(Explosion(self.pos))
                    self.dur_used += 1
                    if self.dur_used == weap_durability:
                        self.dur_used = 0
                        self.stop_callbacks()
                        game.remove_entity(self)
                    game.gold += 1
                    money += 1
                    return
            # move
            step_size = self._speed * dt
            new_x = self.pos[0] + step_size
            new_y = self.pos[1]
            self.pos = (new_x, new_y)

class KnifeLT(Entity):
    global weap_lt
    global weap_size
    def __init__(self, pos, speed=300):
        super().__init__()
        sound = SoundLoader.load("Music/throwing noise.mp3")
        sound.play()
        self._speed = speed
        self.pos = pos
        self.size = (15, 15)
        self.source = weap_lt
        self.dur_used = 0
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        self.source = weap_lt
        self.size = (weap_size[0], weap_size[1])
        # check for collision/out of bounds
        global pause
        if pause == 1:
            if self.pos[0]+Window.width < Window.width or self.pos[0] > Window.width:
                self.stop_callbacks()
                game.unbind(on_frame=self.move_step)
                game.remove_entity(self)
                return
            for e in game.colliding_entities(self, -30):
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                if isinstance(e, EnemyRT):
                    global money
                    global weap_durability
                    game.add_entity(Explosion(self.pos))
                    self.dur_used += 1
                    if self.dur_used == weap_durability:
                        self.dur_used = 0
                        self.stop_callbacks()
                        game.remove_entity(self)
                    game.gold += 1
                    money += 1
                    return
            # move
            step_size = self._speed * dt
            new_x = self.pos[0] - step_size
            new_y = self.pos[1]
            self.pos = (new_x, new_y)
class fireball(Entity):
    def __init__(self, pos, speed=300):
        super().__init__()
        sound = SoundLoader.load("Music/throwing noise.mp3")
        sound.play()
        self._speed = speed
        self.pos = pos
        self.size = (30, 30)
        self.source = self.source = 'images/fireball.png'
        self.dur_used = 0
        self.last_time = 0
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        # check for collision/out of bounds
        global pause
        if pause == 1:
            if self.pos[0]+Window.width < Window.width or self.pos[0] > Window.width:
                self.stop_callbacks()
                game.unbind(on_frame=self.move_step)
                game.remove_entity(self)
                return
            for e in game.colliding_entities(self, 20):
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                if time.time() - self.last_time >= 0.1:
                    self.last_time = time.time()
                    if isinstance(e, EnemyLT):
                        global money
                        game.add_entity(Explosion(self.pos))
                        self.dur_used += 1
                        if self.dur_used == 3:
                            self.dur_used = 0
                            self.stop_callbacks()
                            game.remove_entity(self)
                        return
            # move
            step_size = self._speed * dt
            new_x = self.pos[0] + step_size
            new_y = self.pos[1]
            self.pos = (new_x, new_y)
class HealthLT(Entity):
    def __init__(self, pos, speed, scr):
        super().__init__()
        self.pos = (pos[0]+30, pos[1]+60)
        self.size = (25, 7)
        self._speed = speed
        self.source = scr
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
    def move_step(self, sender, dt):
        if pause == 1:
            step_size = self._speed * dt
            new_x = self.pos[0] - step_size
            new_y = self.pos[1]
            self.pos = (new_x, new_y)
class HealthRT(Entity):
    def __init__(self, pos, speed, scr):
        super().__init__()
        self.pos = (pos[0]+30, pos[1]+60)
        self.size = (25, 7)
        self._speed = speed
        self.source = scr
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
    def move_step(self, sender, dt):
        global pause
        if pause == 1:
            step_size = self._speed * dt
            new_x = self.pos[0] + step_size
            new_y = self.pos[1]
            self.pos = (new_x, new_y)
class EnemyRT(Entity):
    def __init__(self, pos, speed=200):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.size = (80, 80)
        self.source = "images/orc_body/standingD.png"
        self.health = 2
        self.last_time = 0
        self.health_rem = 0
        self.knife_time = 0
        self.sec = 0
        self.full = HealthRT((0, 0), self._speed, 'images/Healthbars/100.png')
        self.half = HealthRT((self.pos[0], self.pos[1]), self._speed, 'images/Healthbars/50.png')
        game.add_entity(self.full)
        game.bind(on_frame=self.move_step)
    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        global gob_rt_imgs
        global gob_rt_cnt
        global money
        global pause
        # check for collision/out of bounds
        if pause == 1:
            if self.pos[1] < 0:
                self.stop_callbacks()
                game.unbind(on_frame=self.move_step)
                game.remove_entity(self)
                return
            for e in game.colliding_entities(self, 40):
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                if self.health <= 0:
                    game.add_entity(Explosion(self.pos))
                    self.stop_callbacks()
                    game.remove_entity(self)
                    game.remove_entity(self.half)
                    game.gold += 1
                    money += 1
                if self.health == 1 and self.health_rem == 0:
                    self.health_rem += 1
                    game.remove_entity(self.full)
                    game.add_entity(self.half)
                if e == game.tower:
                    game.add_entity(Explosion(self.pos))
                    self.stop_callbacks()
                    game.remove_entity(self)
                    game.remove_entity(self.half)
                    game.remove_entity(self.full)
                    game.tHealth -= 2
                    return
                if isinstance(e, KnifeLT):
                    if time.time()-self.knife_time > 0.5:
                        self.knife_time = time.time()
                        self.health -= 1
                if isinstance(e, AssassinLT):
                    if time.time()-self.last_time > 1:
                        self.last_time = time.time()
                        self.health -= 1
            # move
            if gob_rt_cnt + 1 >= 24:  # Need this so we don't get an index error for the sprites
                gob_rt_cnt = 0
            step_size = self._speed * dt
            new_x = self.pos[0] + step_size
            new_y = self.pos[1]
            if time.time() - self.sec > 0.1:
                self.sec = time.time()
                self.source = gob_rt_imgs[gob_rt_cnt // 3]
            gob_rt_cnt += 1
            self.pos = (new_x, new_y)
class EnemyLT(Entity):
    def __init__(self, pos, speed=100):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.size = (80, 80)
        self.source = "images/orc_body/standingD.png"
        self.health = 2
        self.last_time = 0
        self.health_rem = 0
        self.knife_time = 0
        self.sec = 0
        game.bind(on_frame=self.move_step)
        self.full = HealthLT((Window.width, 0), self._speed, 'images/Healthbars/100.png')
        self.half = HealthLT((self.pos[0], self.pos[1]), self._speed, 'images/Healthbars/50.png')
        game.add_entity(self.full)
    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        global gob_lt_cnt
        global gob_lt_imgs
        global money
        global pause
        # check for collision/out of bounds
        if pause == 1:
            if self.health <= 0:
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                game.remove_entity(self.half)
                game.gold += 1
                money += 1
            if self.health == 1 and self.health_rem == 0:
                self.health_rem += 1
                game.remove_entity(self.full)
                game.add_entity(self.half)
            if self.pos[1] < 0:
                self.stop_callbacks()
                game.unbind(on_frame=self.move_step)
                game.remove_entity(self)
                return
            for e in game.colliding_entities(self, -20):
                print(e)
                # isinstance returns whether an object is an instance of a class or of a subclass thereof
                if e == game.tower:
                    game.add_entity(Explosion(self.pos))
                    self.stop_callbacks()
                    game.remove_entity(self)
                    game.remove_entity(self.half)
                    game.remove_entity(self.full)
                    game.tHealth -= 2
                    return
                if isinstance(e, KnifeRT):
                    print(self.health)
                    if time.time()-self.knife_time > 0.5:
                        self.knife_time = time.time()
                        self.health -= 1
                if isinstance(e, fireball):
                    if time.time()-self.last_time > 1:
                        self.last_time = time.time()
                        self.health -= 1
            # move
            if gob_lt_cnt + 1 >= 24:  # Need this so we don't get an index error for the sprites
                gob_lt_cnt = 0
            step_size = self._speed * dt
            new_x = self.pos[0] - step_size
            new_y = self.pos[1]
            if time.time() - self.sec > 0.1:
                self.sec = time.time()
                self.source = gob_lt_imgs[gob_lt_cnt // 3]
            gob_lt_cnt += 1
            self.pos = (new_x, new_y)
class Explosion(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        #sound = SoundLoader.load("Music/Hurt sound.mp3")
        #self.source = "images/tower.png"
        #sound.play()
        Clock.schedule_once(self._remove_me, 0.1)
    def _remove_me(self, dt):
        game.remove_entity(self)

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.source = "images/Main_body2/standingD.png"
        game.bind(on_frame=self.on_frame)
        self.pos = (400, 0)

    def stop_callback(self):
        game.unbind(on_frame=self.on_frame)

    def on_frame(self, sender, dt):
        global walkCount
        global direction
        global pause
        if pause == 1:
            # move
            step_size = 200 * dt
            newx = self.pos[0]
            newy = self.pos[1]
            if walkCount + 1 >= 24:  # Need this so we don't get an index error for the sprites
                walkCount = 0
            if "a" in game.keysPressed and "d" in game.keysPressed:
                self.source = 'images/Main_body2/standingD.png'
            elif "a" in game.keysPressed:
                direction = True
                newx -= step_size
                self.source = lft_imgs[walkCount // 3]
                walkCount += 1
            elif "d" in game.keysPressed:
                direction = False
                newx += step_size
                self.source = rgt_imgs[walkCount // 3]
                walkCount += 1
            else:
                self.source = 'images/Main_body2/standingD.png'
            self.pos = (newx, newy)
            # shoot
            print(game.keysPressed)
            if "spacebar" in game.keysPressed:
                global c
                if c == 0:
                    c = 1
                    x = self.pos[0]
                    y = self.pos[1]
                    if direction:
                        game.add_entity(KnifeLT((x, y + 5)))
                    else:
                        game.add_entity(KnifeRT((x+20, y+5)))
            else:
                c = 0
class Tower(Entity):
    def __init__(self):
        super().__init__()
        self.source = r'images\tower.png'
        self.pos = (Window.width / 2 - (130 / 2), 0)
        self.size = (130, 260)

if wizard_lives == 1:
    game.set_wizard()
if assassin_lives == 1:
    game.set_assassin()
game.player = Player()
game.tower = Tower()
game.add_entity(game.tower)
game.add_entity(game.player)

class MyApp(App):
    def build(self):
        self.load_kv('My.kv')
        return game
if __name__=="__main__":
    app = MyApp()
    app.run()