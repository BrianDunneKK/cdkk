import sys
sys.path.append("..\cdkk")

import cdkk
import pygame

### --------------------------------------------------

class Sprite_Ball(cdkk.Sprite_Shape):
    default_style = {"fillcolour":"red3", "outlinecolour":None, "shape":"Ellipse"}

    def __init__(self, posx, posy, velx, vely, *limits):
        super().__init__(name="Ball", rect=cdkk.cdkkRect(posx, posy, 50, 50), style=Sprite_Ball.default_style)
        self.rect.set_velocity(velx, vely)
        self.rect.set_acceleration(0, self.rect.gravity)
        for l in limits:
            self.rect.add_limit(l)
        self.rect.go()

    def update(self):
        super().update()
        self.rect.move_physics()

### --------------------------------------------------

class Sprite_Obstacle(cdkk.Sprite_Shape):
    default_style = {"fillcolour":"green4", "outlinecolour":None, "shape":"Rectangle"}

    def __init__(self, rect):
        super().__init__(name="Obstacle", rect=rect, style=Sprite_Obstacle.default_style)

### --------------------------------------------------

class Manager_Tests(cdkk.SpriteManager):

    def __init__(self, limits, name="Ball Manager"):
        super().__init__(name)
        self._limits = limits
        self._balls = cdkk.SpriteGroup()
        self._timer = cdkk.Timer()
        self._next_test = 1
        self._timer = cdkk.Timer()
        tt_style={"fillcolour":None, "align_horiz":"L", "textformat":"Test: {0} Time Left: {1:0.1f}"}
        self._test_time = cdkk.Sprite_DynamicText("Test+Time", rect=cdkk.cdkkRect(10, 10, 300, 40), style=tt_style)
        self._test_time.set_text(self._next_test, 0)
        self.add(self._test_time)
        cdkk.EventManager.post_game_control("NextTest")

    def run_test(self):
        if self._next_test == 1:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(700,100,50,250))
            ball = Sprite_Ball(100, 500, 5, -13,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))
            self._timer = cdkk.Timer(10, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)
        elif self._next_test == 2:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(100,100,50,250))
            ball = Sprite_Ball(700, 500, -5, -13,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))
            self._timer = cdkk.Timer(5, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)
        elif self._next_test == 3:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(320,160,300,50))
            ball = Sprite_Ball(100, 500, 10, -20,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))
            self._timer = cdkk.Timer(10, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)
        elif self._next_test == 4:
            obstacle1 = Sprite_Obstacle(cdkk.cdkkRect(320,160,300,50))
            obstacle2 = Sprite_Obstacle(cdkk.cdkkRect(500,350,250,50))
            ball = Sprite_Ball(100, 500, 6, -20,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle1.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle2.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))
            self._timer = cdkk.Timer(10, cdkk.EVENT_GAME_TIMER_1)
            self.add(ball, obstacle1, obstacle2)
            self._balls.add(ball)
        elif self._next_test == 5:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(700,100,50,250))
            ball = Sprite_Ball(100, 500, 5, -13,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_X_CLEAR_VEL_X))
            self._timer = cdkk.Timer(5, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)
        elif self._next_test == 6:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(100,100,50,250))
            ball = Sprite_Ball(700, 500, -5, -14,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_XY_CLEAR_VEL_XY))
            self._timer = cdkk.Timer(5, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)
        elif self._next_test == 7:
            obstacle = Sprite_Obstacle(cdkk.cdkkRect(700,100,50,250))
            ball = Sprite_Ball(100, 500, 20, -12,
                cdkk.Physics_Limit(self._limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE),
                cdkk.Physics_Limit(obstacle.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))
            ball.rect.bounce_cor = 0.5
            self._timer = cdkk.Timer(6, cdkk.EVENT_GAME_TIMER_1)
            self.add(obstacle, ball)
            self._balls.add(ball)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "NextTest":
                self.kill_sprites(self.find_sprites_by_name("Ball"))
                self.kill_sprites(self.find_sprites_by_name("Obstacle"))
                self._balls.empty()
                self.run_test()
                self._next_test = self._next_test + 1
                dealt_with = True
        return dealt_with

    def update(self):
        super().update()
        self._test_time.set_text(self._next_test-1, self._timer.time_left)

### --------------------------------------------------

class TestPhysicsApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball = Manager_Tests(self.boundary)
        self.add_sprite_mgr(self._ball)
        key_map = { pygame.K_q : "Quit" }
        user_event_map = { cdkk.EVENT_GAME_TIMER_1 : "NextTest" }
        self.event_mgr.event_map(key_event_map=key_map, user_event_map=user_event_map)

### --------------------------------------------------

app_config = {
    "width":800, "height":600,
    "background_fill":"burlywood",
    "caption":"Test Physics"
    }
theApp = TestPhysicsApp(app_config)
theApp.execute()

class Sprite_Ball_Old(cdkk.Sprite_Shape):
    def __init__(self, limits, obstacle):
        super().__init__("")        
        rect = cdkk.cdkkRect(100, limits.bottom-100, 50, 50)
        self.setup_shape(rect, shape_colours=["red3"], shape="Ellipse")

        # Test 1: Keep Inside
        # self.rect.set_velocity(5,-10)
        # self.rect.set_velocity(5,-5)    # Hit bottom limit
        # self.rect.set_velocity(5,-15)   # Hit top limit
        # self.rect.set_velocity(10,-10)  # Hit right limit
        # self.rect.set_velocity(-5,-10)     # Hit left limit
        # self.rect.add_limit(cdkk.Physics_Limit(limits, cdkk.LIMIT_KEEP_INSIDE, AT_LIMIT_X_HOLD_POS_X + AT_LIMIT_Y_HOLD_POS_Y))
        # self.rect.add_limit(cdkk.Physics_Limit(limits, cdkk.LIMIT_KEEP_INSIDE, AT_LIMIT_X_CLEAR_VEL_X + AT_LIMIT_Y_HOLD_POS_Y))
        # self.rect.add_limit(cdkk.Physics_Limit(limits, cdkk.LIMIT_KEEP_INSIDE, AT_LIMIT_XY_CLEAR_VEL_XY))
        self.rect.add_limit(cdkk.Physics_Limit(limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE))

        # Test 2: Keep Outside
        self.rect.set_velocity(5,-15)
        # self.rect.add_limit(cdkk.Physics_Limit(obstacle, cdkk.LIMIT_KEEP_OUTSIDE, AT_LIMIT_Y_HOLD_POS_Y+AT_LIMIT_Y_CLEAR_VEL_Y))
        self.rect.add_limit(cdkk.Physics_Limit(obstacle, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_BOUNCE))

        # Test 3: Overlap (destination)
        # destination = cdkkRect(850, 460, 0, 0)
        # self.rect.add_limit(cdkk.Physics_Limit(destination, LIMIT_OVERLAP, AT_LIMIT_XY_CLEAR_VEL_XY))

        # Test 2: Inexact
        # destination = cdkkRect(limits.width/2, limits.height/2, 0, 0)
        # self.rect.add_limit(cdkk.Physics_Limit(destination, LIMIT_OVERLAP, AT_LIMIT_X_HOLD_POS_X+AT_LIMIT_Y_HOLD_POS_Y))

        # Test 3: Inexact
        # self.rect.destination= cdkkRect(650, 450, 0, 0)
