import pygame
import math
from collections import deque
import random

### --------------------------------------------------

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger()
# logger.critical('This is a critical message.')
# logger.error('This is an error message.')
# logger.warning('This is a warning message.')
# logger.info('This is an informative message.')
# logger.debug('This is a low-level debug message.')
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.NOTSET)

### --------------------------------------------------

# Sprite bounces on its ...
BOUNCE_LEFT = 1
BOUNCE_RIGHT = 2
BOUNCE_TOP = 4
BOUNCE_BOTTOM = 8
BOUNCE_VERTICAL = BOUNCE_LEFT + BOUNCE_RIGHT
BOUNCE_HORIZONTAL = BOUNCE_TOP + BOUNCE_BOTTOM

# Limit Types
LIMIT_KEEP_INSIDE = 1              # Keep inside the limits
LIMIT_KEEP_OUTSIDE = 2             # Keep outside the limits
LIMIT_OVERLAP = 4                  # Overlap; compare top-left corners (destination)
LIMIT_COLLISION = 8                # Collision with another moving object
LIMIT_MOVE_TO = 16                 # Move towards the limit (e.g. magnet)

# Action at Limits
AT_LIMIT_X_HOLD_POS_X = 1          # At X limit, hold X position
AT_LIMIT_Y_HOLD_POS_Y = 2          # At Y limit, hold Y position
AT_LIMIT_X_CLEAR_VEL_X = 4         # At X limit, clear X velocity
AT_LIMIT_Y_CLEAR_VEL_Y = 8         # At Y limit, clear Y velocity
AT_LIMIT_XY_CLEAR_VEL_XY = 16      # At X or Y limit, clear X & Y velocities
AT_LIMIT_X_BOUNCE_X = 32           # At X limit, negate X velocity
AT_LIMIT_Y_BOUNCE_Y = 64           # At Y limit, negate Y velocity
AT_LIMIT_BOUNCE = 32+64            # At X/Y limit, negate X/Y velocity
AT_LIMIT_X_MOVE_TO_X = 128         # At X limit, move to X
AT_LIMIT_Y_MOVE_TO_Y = 256         # At Y limit, move to Y
AT_LIMIT_MOVE_TO_XY = 128+256      # At X/Y limit, move to X/Y
AT_LIMIT_X_DO_NOTHING = 512        # At X limit, do nothing
AT_LIMIT_Y_DO_NOTHING = 1024       # At Y limit, do nothing
AT_LIMIT_XY_DO_NOTHING = 512+1024  # At Y limit, do nothing

# At Limit
AT_LIMIT_LEFT = 1
AT_LIMIT_RIGHT = 2
AT_LIMIT_TOP = 4
AT_LIMIT_BOTTOM = 8
AT_LIMIT_INSIDE_X = 16
AT_LIMIT_INSIDE_Y = 32


### --------------------------------------------------

def rect_to_debug_str(r):
    return "Left-Top=({0},{1}), Width-Height=({2},{3})".format(r.left, r.top, r.width, r.height)

### --------------------------------------------------

class Physics_Motion:
    def __init__(self):
        self._position = [0,0]
        self._velocity = [0.0, 0.0]
        self._acceleration = [0.0, 0.0]
        self.low_limit = 0.1

    @property
    def position_x(self):
        return self._position[0]

    @property
    def position_y(self):
        return self._position[1]

    @property
    def velocity_x(self):
        return self._velocity[0]

    @property
    def velocity_y(self):
        return self._velocity[1]
    @property
    def acceleration_x(self):
        return self._acceleration[0]

    @property
    def acceleration_y(self):
        return self._acceleration[1]

    @property
    def stopped(self):
        return (self.velocity_x==0 and self.velocity_y==0 and self.acceleration_x==0 and self.acceleration_y==0)

    @position_x.setter
    def position_x(self, new_position_x):
        self._position[0] = new_position_x

    @position_y.setter
    def position_y(self, new_position_y):
        self._position[1] = new_position_y

    @velocity_x.setter
    def velocity_x(self, new_velocity):
        if (abs(new_velocity) < self.low_limit):
            new_velocity = 0
        self._velocity[0] = new_velocity

    @velocity_y.setter
    def velocity_y(self, new_velocity):
        if (abs(new_velocity) < self.low_limit):
            new_velocity = 0
        self._velocity[1] = new_velocity

    @acceleration_x.setter
    def acceleration_x(self, new_acceleration):
        if (abs(new_acceleration) < self.low_limit):
            new_acceleration = 0
        self._acceleration[0] = new_acceleration

    @acceleration_y.setter
    def acceleration_y(self, new_acceleration):
        if (abs(new_acceleration) < self.low_limit):
            new_acceleration = 0
        self._acceleration[1] = new_acceleration

class Physics_Limit:
    def __init__(self, rect, limit_type, action, event=None):
        self.rect = rect.copy()
        self.limit_type = limit_type  # One of Limit Types
        self.action = action # One of Actions at Limits
        self.event = event
        self.motion = None

class Physics:
    gravity = 9.81
    perfect_bounce = 1

    def __init__(self):
        self._init_motion = Physics_Motion()
        self._curr_motion = Physics_Motion()
        self._timers = [Timer(0, None, False), Timer(0, None, False)]
        self._moving = False
        self.rect_width = 0
        self.rect_height = 0
        self._multiplier = 50
        self._bounce_timer = Timer(0)
        self.bounce_cor = 0.8  # Coefficient of Restitution
        self.bounce_time_limit = 0.5  # Minimum time between dynamic bounces (secs)
        self.negate_acc = 0.9
        self._limits = []

    @property
    def debug_str(self):
        return "Pos=({0:3.0f},{1:3.0f}), Vel=({2:5.1f},{3:5.1f}), Acc=({4:5.1f},{5:5.1f}), InitPos=({6:5.1f},{7:5.1f}), InitVel=({8:5.1f},{9:5.1f})".format(
            self.left, self.top, self.curr_vel_x, self.curr_vel_y, self.curr_acc_x, self.curr_acc_y,
            self.init_pos_x, self.init_pos_y, self.init_vel_x, self.init_vel_y)

    @property
    def init_pos_x(self):
        return self._init_motion.position_x

    @property
    def init_pos_y(self):
        return self._init_motion.position_y

    @property
    def init_vel_x(self):
        return self._init_motion.velocity_x

    @property
    def init_vel_y(self):
        return self._init_motion.velocity_y

    @property
    def curr_acc_x(self):
        return self._curr_motion.acceleration_x

    @property
    def curr_acc_y(self):
        return self._curr_motion.acceleration_y

    @property
    def curr_pos_x(self):
        return self._curr_motion.position_x

    @property
    def curr_pos_y(self):
        return self._curr_motion.position_y

    @property
    def curr_vel_x(self):
        return self._curr_motion.velocity_x

    @property
    def curr_vel_y(self):
        return self._curr_motion.velocity_y

    @property
    def speed(self):
        return math.hypot(self.curr_vel_x, self.curr_vel_y)

    @property
    def angle(self):
        if self.curr_vel_x == 0:
            return 0
        else:
            return math.degrees(math.atan(self.curr_vel_y / self.curr_vel_x))

    @property
    def angle_radians(self):
        if self.curr_vel_x == 0:
            return 0
        else:
            return math.atan(self.curr_vel_y / self.curr_vel_x)

    @property
    def stopped(self):
        return self._curr_motion.stopped

    @curr_pos_x.setter
    def curr_pos_x(self, new_pos_x):
        self._curr_motion.position_x = new_pos_x

    @curr_pos_y.setter
    def curr_pos_y(self, new_pos_y):
        self._curr_motion.position_y = new_pos_y

    @curr_vel_x.setter
    def curr_vel_x(self, new_vel_x):
        self._curr_motion.velocity_x = new_vel_x

    @curr_vel_y.setter
    def curr_vel_y(self, new_vel_y):
        self._curr_motion.velocity_y = new_vel_y

    @curr_acc_x.setter
    def curr_acc_x(self, new_acc_x):
        self._curr_motion.acceleration_x = new_acc_x

    @curr_acc_y.setter
    def curr_acc_y(self, new_acc_y):
        self._curr_motion.acceleration_y = new_acc_y

    @speed.setter
    def speed(self, new_speed):
        self.set_speed_angle(new_speed, self.angle)

    @angle.setter
    def angle(self, new_angle):
        self.set_speed_angle(self.speed, new_angle)

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier):
        self._multiplier = multiplier

    def set_velocity(self, curr_vel_x, curr_vel_y):
        self._curr_motion.velocity_x = curr_vel_x
        self._curr_motion.velocity_y = curr_vel_y
        self._init_pvt_x()
        self._init_pvt_y()

    def set_speed_angle(self, speed, angle):
        self.curr_vel_x = speed * math.cos(math.radians(angle))
        self.curr_vel_y = speed * math.sin(math.radians(angle))

    def set_acceleration(self, xacceleration, yacceleration):
        self._curr_motion.acceleration_x = xacceleration
        self._curr_motion.acceleration_y = yacceleration

    def set_initial_position(self, xpos=None, ypos=None):
        if xpos is None:
            xpos = self.curr_pos_x
        if ypos is None:
            ypos = self.curr_pos_y
        self._init_motion.position_x = xpos
        self._init_motion.position_y = ypos

    def set_initial_velocity(self, xvel=None, yvel=None):
        if xvel is None:
            xvel = self.curr_vel_x
        if yvel is None:
            yvel = self.curr_vel_y
        self._init_motion.velocity_x = xvel
        self._init_motion.velocity_y = yvel

    def set_initial_acceleration(self, xacc=None, yacc=None):
        if xacc is None:
            xacc = self.curr_acc_x
        if yacc is None:
            yacc = self.curr_acc_y
        self._init_motion.acceleration_x = xacc
        self._init_motion.acceleration_y = yacc

    def stop_here_x(self):
        self._init_motion.position_x = self.curr_pos_x
        self._init_motion.velocity_x = 0
        self.curr_acc_x = 0

    def stop_here_y(self):
        self._init_motion.position_y = self.curr_pos_y
        self._init_motion.velocity_y = 0
        self.curr_acc_y = 0

    def _init_pvt_x(self, xpos=None, xvel=None):
        if xpos is None:
            xpos = self.curr_pos_x
        if xvel is None:
            xvel = self.curr_vel_x
        self._init_motion.position_x = xpos
        self._init_motion.velocity_x = xvel
        self._start_x_timer()

    def _init_pvt_y(self, ypos=None, yvel=None):
        if ypos is None:
            ypos = self.curr_pos_y
        if yvel is None:
            yvel = self.curr_vel_y
        self._init_motion.position_y = ypos
        self._init_motion.velocity_y = yvel
        self._start_y_timer()


    def _start_x_timer(self):
        self._timers[0].start()

    def _start_y_timer(self):
        self._timers[1].start()

    @property
    def x_timer_elapsed(self):
        return self._timers[0].time

    @property
    def y_timer_elapsed(self):
        return self._timers[1].time

    def add_limit(self, limit):
        self._limits.append(limit)

    def _calculate_curr_motion(self, dx, dy, use_physics):
        if use_physics:
            self.set_initial_position(self.init_pos_x + dx, self.init_pos_y + dy)
            if (dx > 0 or dy > 0):
                self.apply_limits(self, use_curr_motion=False)

            tx = self.x_timer_elapsed
            self._curr_motion.position_x = self.init_pos_x + int((self.init_vel_x * tx + 0.5 * self.curr_acc_x * tx * tx) * self._multiplier)
            self._curr_motion.velocity_x = self.init_vel_x + self.curr_acc_x * tx
            self._curr_motion.acceleration_x = self.curr_acc_x

            ty = self.y_timer_elapsed
            self._curr_motion.position_y = self.init_pos_y + int((self.init_vel_y * ty + 0.5 * self.curr_acc_y * ty * ty) * self._multiplier)
            self._curr_motion.velocity_y = self.init_vel_y + self.curr_acc_y * ty
            self._curr_motion.acceleration_y = self.curr_acc_y
        else:
            self.set_initial_position(self.left + dx, self.top + dy)
            if (dx > 0 or dy > 0):
                self.apply_limits(self, use_curr_motion=False)
            self.curr_pos_x = self.init_pos_x
            self.curr_pos_y = self.init_pos_y


    def _test_limit(self, limit, use_curr_motion=True):
        if use_curr_motion:
            motion = self._curr_motion
        else:
            motion = self._init_motion

        at_limit_x = at_limit_y = 0

        # Calculate distance to limit
        left_to_limit_left   = motion.position_x - limit.rect.left
        right_to_limit_left  = (motion.position_x + self.rect_width) - limit.rect.left
        left_to_limit_right  = motion.position_x - limit.rect.right
        right_to_limit_right = (motion.position_x + self.rect_width) - limit.rect.right

        top_to_limit_top       = motion.position_y - limit.rect.top
        bottom_to_limit_top    = (motion.position_y + self.rect_height) - limit.rect.top
        top_to_limit_bottom    = motion.position_y - limit.rect.bottom
        bottom_to_limit_bottom = (motion.position_y + self.rect_height) - limit.rect.bottom

        centerx_to_limit_centerx = motion.position_x + self.rect_width//2 - limit.rect.centerx
        centery_to_limit_centery = motion.position_y + self.rect_height//2 - limit.rect.centery

        # Determine if at limit
        if limit.limit_type == LIMIT_KEEP_INSIDE:
            if left_to_limit_left <= 0:
                at_limit_x |= AT_LIMIT_LEFT
            if right_to_limit_right >= 0:
                at_limit_x |= AT_LIMIT_RIGHT
            if top_to_limit_top <= 0:
                at_limit_y |= AT_LIMIT_TOP
            if bottom_to_limit_bottom >= 0:
                at_limit_y |= AT_LIMIT_BOTTOM

        elif limit.limit_type == LIMIT_KEEP_OUTSIDE:
            if (right_to_limit_left >= 0) and (left_to_limit_left < 0) and (motion.position_y+self.rect_height >= limit.rect.top) and (motion.position_y <= limit.rect.bottom):
                at_limit_x |= AT_LIMIT_LEFT

            if (left_to_limit_right <= 0) and (right_to_limit_right > 0) and (motion.position_y+self.rect_height >= limit.rect.top) and (motion.position_y <= limit.rect.bottom):
                at_limit_x |= AT_LIMIT_RIGHT

            if (bottom_to_limit_top >= 0) and (top_to_limit_top < 0) and (motion.position_x+self.rect_width >= limit.rect.left) and (motion.position_x <= limit.rect.right):
                at_limit_y |= AT_LIMIT_TOP

            if (top_to_limit_bottom <= 0) and (bottom_to_limit_bottom > 0) and (motion.position_x+self.rect_width >= limit.rect.left) and (motion.position_x <= limit.rect.right):
                at_limit_y |= AT_LIMIT_BOTTOM

        elif limit.limit_type == LIMIT_OVERLAP:
            if abs(left_to_limit_left) <= abs(motion.velocity_x):
                at_limit_x |= AT_LIMIT_LEFT
            if abs(top_to_limit_top) <= abs(motion.velocity_y):
                at_limit_y |= AT_LIMIT_TOP

        elif limit.limit_type == LIMIT_MOVE_TO:
            if left_to_limit_right > 0:
                at_limit_x |= AT_LIMIT_RIGHT
            elif right_to_limit_left  < 0:
                at_limit_x |= AT_LIMIT_LEFT
            elif abs(centerx_to_limit_centerx) < limit.rect.width:
                at_limit_x |= AT_LIMIT_INSIDE_X
            if top_to_limit_bottom > 0:
                at_limit_y |= AT_LIMIT_BOTTOM
            elif bottom_to_limit_top  < 0:
                at_limit_y |= AT_LIMIT_TOP
            elif abs(centery_to_limit_centery) < limit.rect.height:
                at_limit_y |= AT_LIMIT_INSIDE_Y

        return (at_limit_x, at_limit_y)

    def _post_event_at_limit(self, limit, at_limit_x, at_limit_y, use_curr_motion=True):
        if (at_limit_x > 0 or at_limit_y > 0) and limit.event is not None and use_curr_motion:
            limit.event.at_limit_x = at_limit_x
            limit.event.at_limit_y = at_limit_y
            EventManager.post(limit.event)

    def _eval_action(self, action):
        if (action & AT_LIMIT_X_CLEAR_VEL_X) > 0 or (action & AT_LIMIT_X_BOUNCE_X) > 0:
            action |= AT_LIMIT_X_HOLD_POS_X

        if (action & AT_LIMIT_Y_CLEAR_VEL_Y) > 0 or (action & AT_LIMIT_Y_BOUNCE_Y) > 0:
            action |= AT_LIMIT_Y_HOLD_POS_Y

        if (action & AT_LIMIT_XY_CLEAR_VEL_XY) > 0:
            action |= AT_LIMIT_X_HOLD_POS_X
            action |= AT_LIMIT_Y_HOLD_POS_Y

        return action

    def _execute_action(self, limit, action, at_limit_x, at_limit_y, use_curr_motion=True):
        if use_curr_motion:
            motion = self._curr_motion
        else:
            # AT_LIMIT_X_HOLD_POS_X and AT_LIMIT_Y_HOLD_POS_Y only
            motion = self._init_motion

        # AT_LIMIT_X_HOLD_POS_X
        if (action & AT_LIMIT_X_HOLD_POS_X) > 0 and at_limit_x > 0:
            if limit.limit_type == LIMIT_KEEP_INSIDE:
                if (at_limit_x & AT_LIMIT_LEFT > 0):
                    motion.position_x = limit.rect.left
                if (at_limit_x & AT_LIMIT_RIGHT > 0):
                    motion.position_x = limit.rect.right - self.rect_width

            if limit.limit_type == LIMIT_KEEP_OUTSIDE:
                if (at_limit_x & AT_LIMIT_LEFT > 0):
                    motion.position_x = limit.rect.left - self.rect_width
                if (at_limit_x & AT_LIMIT_RIGHT > 0):
                    motion.position_x = limit.rect.left

            if limit.limit_type == LIMIT_OVERLAP:
                if (at_limit_x & AT_LIMIT_LEFT > 0) or (at_limit_x & AT_LIMIT_RIGHT > 0):
                    motion.position_x = limit.rect.left

        # AT_LIMIT_Y_HOLD_POS_Y
        if (action & AT_LIMIT_Y_HOLD_POS_Y) > 0 and at_limit_y > 0:
            if limit.limit_type == LIMIT_KEEP_INSIDE:
                if (at_limit_y & AT_LIMIT_TOP > 0):
                    motion.position_y = limit.rect.top
                if (at_limit_y & AT_LIMIT_BOTTOM > 0):
                    motion.position_y = limit.rect.bottom - self.rect_height

            if limit.limit_type == LIMIT_KEEP_OUTSIDE:
                if (at_limit_y & AT_LIMIT_TOP > 0):
                    motion.position_y = limit.rect.top - self.rect_height
                if (at_limit_y & AT_LIMIT_BOTTOM > 0):
                    motion.position_y = limit.rect.bottom

            if limit.limit_type == LIMIT_OVERLAP:
                if (at_limit_y & AT_LIMIT_TOP > 0) or (at_limit_y & AT_LIMIT_BOTTOM > 0):
                    motion.position_y = limit.rect.top

        # AT_LIMIT_X_CLEAR_VEL_X
        if (action & AT_LIMIT_X_CLEAR_VEL_X) > 0 and at_limit_x > 0:
            self.stop_here_x()

        # AT_LIMIT_Y_CLEAR_VEL_Y
        if (action & AT_LIMIT_Y_CLEAR_VEL_Y) > 0 and at_limit_y > 0:
            self.stop_here_y()

        # AT_LIMIT_XY_CLEAR_VEL_XY
        if (action & AT_LIMIT_XY_CLEAR_VEL_XY) > 0 and (at_limit_x > 0 or at_limit_y > 0):
            self.stop_here_x()
            self.stop_here_y()

        # AT_LIMIT_X_BOUNCE_X
        if (action & AT_LIMIT_X_BOUNCE_X) > 0 and at_limit_x > 0:
            self._init_pvt_x(self.curr_pos_x, self.curr_vel_x * -self.bounce_cor)

        # AT_LIMIT_Y_BOUNCE_Y
        if (action & AT_LIMIT_Y_BOUNCE_Y) > 0 and at_limit_y > 0:
            self._init_pvt_y(self.curr_pos_y, self.curr_vel_y * -self.bounce_cor)

        # AT_LIMIT_X_MOVE_TO_X
        if (action & AT_LIMIT_X_MOVE_TO_X) > 0:
                if (at_limit_x & AT_LIMIT_INSIDE_X) > 0:
                    if abs(self.curr_vel_x) > 0:
                        self.curr_pos_x = limit.rect.centerx - self.rect_width//2
                        self.stop_here_x()
                if (at_limit_x & AT_LIMIT_LEFT) > 0:
                    if self.curr_vel_x == 0:
                        self.curr_vel_x = abs(limit.motion.velocity_x)
                        self._init_pvt_x()
                if (at_limit_x & AT_LIMIT_RIGHT) > 0:
                    if self.curr_vel_x == 0:
                        self.curr_vel_x = -abs(limit.motion.velocity_x)
                        self._init_pvt_x()

        # AT_LIMIT_Y_MOVE_TO_Y
        if (action & AT_LIMIT_Y_MOVE_TO_Y) > 0:
                if (at_limit_y & AT_LIMIT_INSIDE_Y) > 0:
                    if abs(self.curr_vel_y) > 0:
                        self.curr_pos_y = limit.rect.centery - self.rect_height//2
                        self.stop_here_y()
                if (at_limit_y & AT_LIMIT_LEFT) > 0:
                    if self.curr_vel_y == 0:
                        self.curr_vel_y = abs(limit.motion.velocity_y)
                        self._init_pvt_y()
                if (at_limit_y & AT_LIMIT_RIGHT) > 0:
                    if self.curr_vel_y == 0:
                        self.curr_vel_y = -abs(limit.motion.velocity_y)
                        self._init_pvt_y()

        # AT_LIMIT_X_DO_NOTHING
        if (action & AT_LIMIT_X_DO_NOTHING) > 0:
            pass

        # AT_LIMIT_Y_DO_NOTHING
        if (action & AT_LIMIT_Y_DO_NOTHING) > 0:
            pass


    def _apply_limit(self, limit, use_curr_motion=True):
        at_limit_x, at_limit_y = self._test_limit(limit, use_curr_motion)
        if (at_limit_x > 0 or at_limit_y > 0):
            self._post_event_at_limit(limit, at_limit_x, at_limit_y, use_curr_motion)
            action = self._eval_action(limit.action)
            self._execute_action(limit, action, at_limit_x, at_limit_y, use_curr_motion)

    def apply_limits(self, use_physics=False, use_curr_motion=True):
        if not use_physics:
            self.rect_width = self.width
            self.rect_height = self.height
        for limit in self._limits:
            self._apply_limit(limit, use_curr_motion)

    def dynamic_limit(self, limit):
        if limit.limit_type == LIMIT_KEEP_INSIDE or limit.limit_type == LIMIT_KEEP_OUTSIDE or limit.limit_type == LIMIT_OVERLAP:
            # To Do: Test
            at_limit_x, at_limit_y = self._test_limit(limit)
            if (at_limit_x > 0 or at_limit_y > 0):
                self._post_event_at_limit(limit, at_limit_x, at_limit_y)
                action = self._eval_action(limit.action)
                self._execute_action(limit, action, at_limit_x, at_limit_y)

        if limit.limit_type == LIMIT_COLLISION and limit.action == AT_LIMIT_BOUNCE and self._bounce_timer.time_left == 0:
            if limit.rect.centery != self.centery: # Avoid divde by 0
                tangent_slope = (self.centerx - limit.rect.centerx) / (limit.rect.centery - self.centery)
                tangent_angle = math.degrees(math.atan(tangent_slope))
                self.angle = 2 * tangent_angle - self.angle
                self.go()
                self.move_physics()
                self._bounce_timer = Timer(self.bounce_time_limit)
                self._post_event_at_limit(limit, 1, AT_LIMIT_TOP)

### --------------------------------------------------

class MovingRect(pygame.Rect, Physics):
    def __init__(self):
        Physics.__init__(self)
        self.topleft = (0,0)
        self.size = (0,0)
        self.limits = None
        self._use_physics = False

    def go(self):
        self.set_initial_position(self.left, self.top)
        self.set_initial_velocity()
        self.rect_width = self.width
        self.rect_height = self.height
        self._start_x_timer()
        self._start_y_timer()
        self._moving = not self.stopped
        self._use_physics = True

    def move_physics(self, dx=0, dy=0):
        # logger.debug("BEFORE: "+self.debug_str)
        self._calculate_curr_motion(dx, dy, self._use_physics)
        self.apply_limits(self._use_physics)
        self.left = self.curr_pos_x
        self.top = self.curr_pos_y
        # logger.debug("AFTER : "+self.debug_str)

### --------------------------------------------------

class Timer():
    def __init__(self, timer_value=0, timer_event=None, auto_start=True):
        self._timer_value = timer_value * 1000.0
        self._start_time = pygame.time.get_ticks()
        self._stop_time = pygame.time.get_ticks()
        self._timer_event = timer_event
        if (auto_start):
                self.start()

    def start(self):
        self._start_time = pygame.time.get_ticks()
        if self._timer_event != None:
            pygame.time.set_timer(self._timer_event, int(self._timer_value))

    
    def stop(self):
        self._stop_time = pygame.time.get_ticks()
        return (self._stop_time - self._start_time)/1000.0

    def stop_event(self):
        if self._timer_event != None:
            pygame.time.set_timer(self._timer_event, 0)

    @property
    def time(self):
        time_now = pygame.time.get_ticks()
        return (time_now - self._start_time)/1000.0

    @property
    def time_msecs(self):
        return int(self.time * 1000.0)

    @property
    def time_left(self):
        time_now = pygame.time.get_ticks()
        time_left = self._timer_value - (time_now - self._start_time)
        time_left = max(time_left, 0)
        return time_left/1000.0

    def extend_timer(self, increase_secs):
        self._timer_value = self._timer_value + increase_secs * 1000.0

### --------------------------------------------------

class LoopTimer():
    def __init__(self, max_loops, auto_start=True):
        self._queue = deque([0] * max_loops, max_loops)
        self._timer = Timer(auto_start=auto_start)

    def start(self):
        self._timer.start()

    def append(self, loop_time=None):
        if loop_time is None:
            loop_time = self._timer.time_msecs
        self._queue.append(loop_time)
        self._timer.start()

    @property
    def msecs_per_loop(self):
        return sum(self._queue) / len(self._queue)

    @property
    def loops_per_sec(self):
        msecs = self.msecs_per_loop
        if msecs == 0:
            return 0
        else:
            return 1000.0 / self.msecs_per_loop

### --------------------------------------------------

EVENT_READ_KEYBOARD   = pygame.USEREVENT
EVENT_GAME_CONTROL    = pygame.USEREVENT + 1
EVENT_GAME_TIMER_1    = pygame.USEREVENT + 2
EVENT_GAME_TIMER_2    = pygame.USEREVENT + 3
EVENT_NEXT_USER_EVENT = pygame.USEREVENT + 4

# Game Control Actions
#   e.action: StartGame, GameOver, QuitGame, Board, Pass, Hint, ClearHint, Print, IncreaseScore, KillSpriteUUID,
#             MouseMotion, MouseLeftClick, MouseRightClick, MouseUnclick
#   e.info: Dictionary with additional event information, including:
#             pos   - Mouse position for MouseMotion, MouseLeftClick, MouseRightClick and MouseUnclick
#             value - Delta value for IncreaseScore

class EventManager:
    def get():
        ev_list = pygame.event.get()
        return ev_list

    def post(e):
        if (e.type >= pygame.NUMEVENTS):
            logger.error("Max value for event type is {0}".format(e.type))
        pygame.event.post(e)

    def create_event(event_type, action="", **info_items):
        if type(event_type).__name__ == "tuple":
            t, a = event_type
            return EventManager.create_event(t, a, info_items)
        else:
            info = {}
            for key, value in info_items.items():
                info[key] = value
            ev_dict = {"action": action, "info": info}
            e = pygame.event.Event(event_type, ev_dict)
            return e

    def gc_event(action, **info_items):
        return EventManager.create_event(EVENT_GAME_CONTROL, action, **info_items)
        
    def post_game_control(action, **info_items):
        ev = EventManager.create_event(EVENT_GAME_CONTROL, action, **info_items)
        EventManager.post(ev)

    def set_key_repeat(delay, interval):
        pygame.key.set_repeat(delay, interval)

    def disable_key_repeat():
        pygame.key.set_repeat()

    def __init__(self):
        self._keyboard = {}
        self._user_event = {}

    def keyboard_event(self, event_type, action):
        self._keyboard[event_type] = action

    def user_event(self, event_type, action):
        self._user_event[event_type] = action

    def event(self, e, ignore_keys=False):
        dealt_with = False
        action = None
        if e.type == pygame.MOUSEMOTION:
            action = "MouseMotion"
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                action = "MouseLeftClick"
            elif e.button == 3:
                action = "MouseRightClick"
        elif e.type == pygame.MOUSEBUTTONUP:
            action = "MouseUnclick"
        if action is not None and (e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEMOTION):
            ev = EventManager.create_event(EVENT_GAME_CONTROL, action, pos=e.pos)
            EventManager.post(ev)
            dealt_with = True
        
        if e.type == pygame.KEYDOWN and not dealt_with and not ignore_keys:
            for kb_k, kb_a in self._keyboard.items():
                if e.key == kb_k:
                    EventManager.post_game_control(kb_a)
                    dealt_with = True

        if e.type == EVENT_READ_KEYBOARD and ignore_keys:
            keys = pygame.key.get_pressed()
            for kb_k, kb_a in self._keyboard.items():
                if keys[kb_k]:
                    EventManager.post_game_control(kb_a)
            dealt_with = True

        if not dealt_with:
            for tim_t, tim_a in self._user_event.items():
                if e.type == tim_t:
                    EventManager.post_game_control(tim_a)
                    dealt_with = True

        return dealt_with

### --------------------------------------------------

class RandomQueue:
    def __init__(self, queue_len, min_val, max_val, max_change=20, max_change_rate=3, init_value=0):
        self._queue = deque([init_value] * queue_len, queue_len)
        self._min = min_val
        self._max = max_val
        self._max_change = max_change
        self._max_change_rate = max_change_rate
        self._next_value = 0
        self._next_change = 0
    
    @property
    def queue(self):
        return self._queue
    
    @property
    def next_value(self):
        return self._next_value

    @next_value.setter
    def next_value(self, new_value):
        self._next_value = new_value
    
    def append(self, dyn_max=-1):
        if dyn_max < 0:
            dyn_max = self._max

        self._queue.append(self._next_value)
        self._next_change = self._next_change + random.randint(-self._max_change_rate, self._max_change_rate) * random.randint(-self._max_change_rate, self._max_change_rate)
        self._next_change = max(self._next_change, -self._max_change)
        self._next_change = min(self._next_change,self._max_change)

        self._next_value = self._next_value + self._next_change
        if self._next_value < self._min:
            self._next_value = self._min
            self._next_change = max(self._next_change, 0)
        if self._next_value > min(self._max, dyn_max):
            self._next_value = min(self._max, dyn_max)
            self._next_change = min(self._next_change, 0)

### --------------------------------------------------

# Animation modes
ANIMATE_MANUAL       = 1
ANIMATE_LOOP         = 2
ANIMATE_SHUTTLE      = 3
ANIMATE_ONCE         = 4
ANIMATE_SHUTTLE_ONCE = 5
ANIMATE_REVERSE      = 8  # Add to other modes

class Animation_Counter:
    def __init__(self):
        self.msecs_per_image = None  # To Do
        self.setup(0, ANIMATE_LOOP, 10)

    def setup(self, total, mode, loops_per_image=10):
        self.total = total      # Total images
        self.loop = 0           # Loop counter
        if (mode & ANIMATE_REVERSE) == 0:
            self.mode = mode
            self.forward = True
            self.index = 0      # Image index
            self.step = 1
        if (mode & ANIMATE_REVERSE) > 0:
            self.mode = mode - ANIMATE_REVERSE
            self.forward = False
            self.index = total - 1
            self.step = -1
        if self.mode == ANIMATE_MANUAL:
            self.step = 0
            self.index = 0
        if loops_per_image is None:
            loops_per_image = 10
        self.loops_per_image = loops_per_image

    def next_loop(self):
        show_next_image = False
        self.loop += 1
        if (self.loop >= self.loops_per_image):
            self.loop = 0
            show_next_image = True
            self.next_image()
        return show_next_image

    @property
    def current_image(self):
        return self.index

    @current_image.setter
    def current_image(self, new_image):
        self.index = new_image

    def next_image(self):
        if self.mode == ANIMATE_MANUAL:
            if self.forward:
                self.index = min(self.index + 1, self.total - 1)
            else:
                self.index = max(self.index - 1, 0)
        else:
            self.index = self.index + self.step            
        if self.index >= self.total:
            if self.mode == ANIMATE_LOOP:
                self.index = 0
            elif self.mode == ANIMATE_SHUTTLE:
                self.step = -1
                self.index = self.total - 2
            elif self.mode == ANIMATE_ONCE:
                self.index = self.total - 1
                self.step = 0
            elif self.mode == ANIMATE_SHUTTLE_ONCE:
                if self.forward:
                    self.step = -1
                    self.index = self.total - 2
                else:
                    self.index = self.total - 1
                    self.step = 0
        if self.index < 0:
            if self.mode == ANIMATE_LOOP:
                self.index = self.total - 1
            elif self.mode == ANIMATE_SHUTTLE:
                self.step = 1
                self.index = 1
            elif self.mode == ANIMATE_ONCE:
                self.index = 0
                self.step = 0
            elif self.mode == ANIMATE_SHUTTLE_ONCE:
                if self.forward:
                    self.index = 0
                    self.step = 0
                else:
                    self.step = 1
                    self.index = 1

    def prev_image(self):
        if self.mode == ANIMATE_MANUAL:
            if self.forward:
                self.index = max(self.index - 1, 0)
            else:
                self.index = min(self.index + 1, self.total - 1)