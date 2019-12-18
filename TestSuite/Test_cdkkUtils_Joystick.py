import sys
sys.path.append("..\cdkk")

import pygame
import cdkk

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite_Shape):
    def __init__(self, posx, posy):
        super().__init__(name="Ball", rect=cdkk.cdkkRect(
            posx, posy, 50, 50), style={"fillcolour": "red3", "outlinecolour": None, "shape": "Ellipse"})
        self.rect.go()
        self.set_config("auto_move_physics", True)

# --------------------------------------------------


class Manager_JoystickTest(cdkk.SpriteManager):

    def __init__(self, name="Test Manager"):
        super().__init__(name)
        self._ball = Sprite_Ball(200, 200)
        self.add(self._ball)
        self._relative_mode = True

    @property
    def relative(self):
        return self._relative_mode

    @relative.setter
    def relative(self, is_relative):
        self._relative_mode = is_relative
        self._ball.rect.use_physics = is_relative
        if not is_relative:
            self._ball.rect.set_velocity(0,0)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "JoystickMotion":
                val = e.info["value"]
                pos = e.info.get("pos",0)
                if e.info["axis"] == "X":
                    if self._relative_mode:
                        self._ball.rect.set_velocity(vel_x=val * 50)
                    else:
                        self._ball.rect.centerx = pos
                if e.info["axis"] == "Y":
                    if self._relative_mode:
                        self._ball.rect.set_velocity(vel_y=val * 50)
                    else:
                        self._ball.rect.centery = pos
                dealt_with = True
            elif e.action == "JoystickButtonDown":
                if e.info["button"] == 0:
                    self._ball.rect.move_to(200,200)
                    dealt_with = True

        return dealt_with
       

# --------------------------------------------------


class TestJoystickApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._test = Manager_JoystickTest()
        self.add_sprite_mgr(self._test)
        key_map = {pygame.K_q: "Quit", pygame.K_m: "SwitchMode"}
        self.event_mgr.event_map(key_event_map=key_map)
        self._relative_mode = True
        self.config_joystick(self.boundary, self._test._ball.rect.size, 4)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL and e.action == "SwitchMode":
            if self._relative_mode:
                self.config_joystick(self.boundary, steps=0)
            else:
                self.config_joystick(None, steps=4)
            self._test.relative = self._relative_mode = not self._relative_mode


# --------------------------------------------------


app_config = {
    "width": 800, "height": 600,
    "background_fill": "burlywood",
    "caption": "Test Joystick",
    "joystick_name": "Logitech Attack 3"
}
TestJoystickApp(app_config).execute()
