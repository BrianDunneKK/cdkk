from PyGameApp import *

### --------------------------------------------------

class Sprite_Ball(Sprite_Shape):
    def __init__(self, limits, obstacle):
        super().__init__("")        
        rect = pygame.Rect(100, limits.bottom-100, 50, 50)
        self.setup_shape(rect, shape_colours=["red3"], shape="Ellipse")

        # Test 1: Keep Inside
        # self.rect.set_velocity(5,-10)
        # self.rect.set_velocity(5,-5)    # Hit bottom limit
        # self.rect.set_velocity(5,-15)   # Hit top limit
        # self.rect.set_velocity(10,-10)  # Hit right limit
        # self.rect.set_velocity(-5,-10)     # Hit left limit
        # self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_X_HOLD_POS_X + AT_LIMIT_Y_HOLD_POS_Y))
        # self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_X_CLEAR_VEL_X + AT_LIMIT_Y_HOLD_POS_Y))
        # self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_XY_CLEAR_VEL_XY))
        self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_BOUNCE))

        # Test 2: Keep Outside
        self.rect.set_velocity(5,-15)
        # self.rect.add_limit(Physics_Limit(obstacle, LIMIT_KEEP_OUTSIDE, AT_LIMIT_Y_HOLD_POS_Y+AT_LIMIT_Y_CLEAR_VEL_Y))
        self.rect.add_limit(Physics_Limit(obstacle, LIMIT_KEEP_OUTSIDE, AT_LIMIT_BOUNCE))

        # Test 3: Overlap (destination)
        # destination = pygame.Rect(850, 460, 0, 0)
        # self.rect.add_limit(Physics_Limit(destination, LIMIT_OVERLAP, AT_LIMIT_XY_CLEAR_VEL_XY))

        # Test 2: Inexact
        # destination = pygame.Rect(limits.width/2, limits.height/2, 0, 0)
        # self.rect.add_limit(Physics_Limit(destination, LIMIT_OVERLAP, AT_LIMIT_X_HOLD_POS_X+AT_LIMIT_Y_HOLD_POS_Y))

        # Test 3: Inexact
        # self.rect.destination= pygame.Rect(650, 450, 0, 0)

        self.rect.set_acceleration(0, self.rect.gravity)
        self.rect.go()
    
    def update(self):
        super().update()
        self.rect.move_physics()

### --------------------------------------------------

class Manager_Ball(SpriteManager):
    def __init__(self, limits, name = "Ball Manager"):
        super().__init__(name)
        self._limits = limits

        obstacle = Sprite_Shape("Obstacle")
        obstacle.setup_shape(pygame.Rect(0,0,50,250), ["black"])

        # Hit top
        # obstacle.rect.left = limits.width/2
        # obstacle.rect.top = limits.height/2

        # Hit bottom
        # obstacle.rect.left = 200
        # obstacle.rect.top = 200

        # Hit left
        obstacle.rect.left = 700
        obstacle.rect.top = 100

        self.add(obstacle)

        ball = Sprite_Ball(self._limits, obstacle.rect)
        self.add(ball)

### --------------------------------------------------

class TestPhysicsApp(PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Ball(self.boundary))

    def event(self, event):
        dealt_with = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_q):  # Press Q to Quit
                self.exit_app()
        if not dealt_with:
            super().event(event)

### --------------------------------------------------

theApp = TestPhysicsApp()
theApp.execute()
