import sys
sys.path.insert(0, "cdkk")
import pygame
import math
import cdkk


# --------------------------------------------------


class Manager_TestSprite(cdkk.SpriteManager):
    def __init__(self, limits, name="Test PyGame App Manager"):
        super().__init__(name)

        image_sprite = cdkk.Sprite()
        image_sprite.load_image_from_file("beachball.png")
        image_sprite.rect.topleft = (10, 10)
        self.add(image_sprite)

        image_sprite2 = cdkk.Sprite()
        image_sprite2.load_image_from_file("beachball.png",
                                           scale_to=(30, 30))
        image_sprite2.rect.topleft = (10, 200)
        self.add(image_sprite2)

        image_sprite3 = cdkk.Sprite()
        image_sprite3.load_image_from_file("beachball.png",
                                           crop=(30, 10, 30, 10))
        image_sprite3.rect.topleft = (10, 300)
        self.add(image_sprite3)

        image_sprite4 = cdkk.Sprite()
        process4 = img_cmds = [
            ("crop", (30, 10, 30, 10)),
            ("scale", (50, 50))
        ]
        image_sprite4.load_image_from_file("beachball.png",
                                           img_process=process4)
        image_sprite4.rect.topleft = (10, 400)
        self.add(image_sprite4)

        image_sprite5 = cdkk.Sprite()
        process5 = img_cmds = [
            ("scale", (50, 50)),
            ("crop", (30, 10, 30, 10))
        ]
        image_sprite5.load_image_from_file("beachball.png", process5)
        image_sprite5.rect.topleft = (10, 500)
        self.add(image_sprite5)

        image_sprite6 = cdkk.Sprite()
        image_sprite6.load_image_from_file("beachball.png", img_process=("flip", (True, False)), scale_to=(100,100))
        image_sprite6.rect.topleft = (300, 300)
        self.add(image_sprite6)

        image_sprite7 = cdkk.Sprite()
        process7 = img_cmds = [
            ("flip", (True, True)),
            ("scale", (100, 100))
        ]
        image_sprite7.load_image_from_file("beachball.png", img_process=process7)
        image_sprite7.rect.topleft = (300, 400)
        self.add(image_sprite7)

        image_sprite8 = cdkk.Sprite()
        image_sprite8.load_image_from_file("beachball.png", img_process=("rotate", 45))
        image_sprite8.rect.topleft = (300, 500)
        self.add(image_sprite8)

        image_sprite9 = cdkk.Sprite()
        image_sprite9.load_image_from_file("beachball.png")
        image_sprite9.cdkkimage.create_copy()
        image_sprite9.rect.topleft = (500, 300)
        self.add(image_sprite9)

        image_sprite10 = cdkk.Sprite()
        image_sprite10.load_image_from_file("beachball.png")
        image_sprite10.cdkkimage.create_copy()
        for i in range(5):
            image_sprite10.cdkkimage.process("rotate", 36)
        # image_sprite10.cdkkimage.restore_copy()
        image_sprite10.rect.topleft = (500, 500)
        self.add(image_sprite10)

        anim_sprite = cdkk.Sprite_Animation()
        anim_sprite.load_spritesheet("Explode", "ExplosionCount.png",
                                     4, 4, set_anim=True, img_process=("scale", (200,200)))
        anim_sprite.rect.topleft = (300, 10)
        self.add(anim_sprite)

        image_from_ss1 = cdkk.Sprite()
        image_from_ss1.cdkkimage.set_spritesheet("ExplosionCount.png", 4, 4)
        image_from_ss1.cdkkimage.spritesheet_image(6)
        image_from_ss1.rect.topleft = (650, 10)
        self.add(image_from_ss1)

        image_from_ss2 = cdkk.Sprite()
        image_from_ss2.cdkkimage.set_spritesheet("ExplosionCount.png", 4, 4,
                                              [("scale", (200, 100)), ("crop", (30, 10, 30, 10))])
        image_from_ss2.cdkkimage.spritesheet_image(6)
        image_from_ss2.rect.topleft = (650, 100)
        self.add(image_from_ss2)

        self._car = cdkk.Sprite()
        self._car.load_image_from_file("car.png")
        self._car.rect.topleft = (800, 400)
        self._car.cdkkimage.create_copy(info=self._car.rect.center)
        self.add(self._car)

        pipe_up = cdkk.Sprite(filename="pipe.png")
        process_pipe = [
            ("scale", (50, 50)),
            ("flip", (False, True)),
            ("stretch", [0,0,350,0])
        ]
        pipe_up.process_image(process_pipe)
        pipe_up.rect.topleft = (150, 300)
        self.add(pipe_up)

        pipe_dn = cdkk.Sprite(filename="pipe.png")
        process_pipe = [
            ("scale", (50, 50)),
            ("stretch", [0,0,0,350])
        ]
        pipe_dn.process_image(process_pipe)
        pipe_dn.rect.topleft = (250, 300)
        self.add(pipe_dn)

        pipe_lr = cdkk.Sprite(filename="pipe.png")
        process_pipe = [
            ("scale", (50, 50)),
            ("rotate", 90),
            ("stretch", [100,200,0,0])
        ]
        pipe_lr.process_image(process_pipe)
        pipe_lr.rect.topleft = (50, 500)
        self.add(pipe_lr)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "MouseMotion":
                x, y = e.info["pos"]
                cx, cy = self._car.rect.center
                if x == cx: x = x + 1
                angle = math.degrees(math.atan2(cy-y, x-cx))

                self._car.cdkkimage.process("rotate", angle)

                # center = self._car.cdkkimage.restore_copy()
                # size = self._car.cdkkimage.process("rotate", (angle, False, False))
                # self._car.rect.size = size
                # self._car.rect.center = center
                dealt_with = True

        return dealt_with

# --------------------------------------------------


class TestPyGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Test cdkkSprite")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_TestSprite(self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

# --------------------------------------------------


app_config = {
    "width": 1200, "height": 800,
    "background_fill": "burlywood",
    "caption": "Test PyGame - Sprite",
    "image_path": "cdkk\\TestSuite\\"
}
theApp = TestPyGameApp(app_config)
theApp.execute()
