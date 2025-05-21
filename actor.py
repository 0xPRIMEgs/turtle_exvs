import sys, pygame, math, time, random, csv
class Actor:
    def __init__(self, x, y, size, team, target):
        self.x = x
        self.y = y
        self.angle = 0
        self.direction = 0
        self.size = size
        self.bullets = []
        self.beams = []
        self.missiles = []
        self.flames = []
        self.team = team
        self.speed = 8

        self.target = target
        self.lock_type = 0

        self.weapon_ammo_a = 25
        self.weapon_ammo_max_a = 25
        self.reload_timer_a = 1
        self.last_reload_a = 0 

        self.weapon_ammo_b = 5
        self.weapon_ammo_max_b = 5
        self.cool_down_b = 0.5
        self.last_shot_b = 0
        self.reload_timer_b = 2
        self.last_reload_b = 0 

        self.weapon_ammo_c = 1
        self.weapon_ammo_max_c = 1
        self.reload_timer_c = 3
        self.last_reload_c = 0 

        self.bot_timer = 0.5
        self.bot_last_movement = [False,False,False,False]
        self.bot_last_update_time = 0
        self.bot_shot_choice = 0

    def pos(self):
        return (self.x, self.y)

    def get_tile_occupied(self, arena_map_array):
        one_over_tile_size = 1/32
        tile_x, tile_y = math.floor((self.x) * one_over_tile_size),math.floor((self.y) * one_over_tile_size)

        if tile_y < len(arena_map_array):
            if tile_x < len(arena_map_array[tile_y]):
                return (tile_x, tile_y)

        return (-1,-1)
    
    def shoot_a(self, add_bullet):
         if self.weapon_ammo_a > 0:
            spread = 1
            na = self.angle + (random.randrange(-10, 10) * spread)
            add_bullet(self.bullets, self.pos(), na, 5, 3)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
            self.weapon_ammo_a -= 1
            if self.weapon_ammo_a == 0:
                self.last_reload_a = time.time()

    def shoot_b(self, add_bullet):
         if time.time() - self.last_shot_b > self.cool_down_b:
            if self.weapon_ammo_b > 0:
                for i in range(10):
                    add_bullet(self.beams, self.pos(), self.angle, 5 - (i * 0.1), 3)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
                self.weapon_ammo_b -= 1
                self.last_shot_b = time.time()
                if self.weapon_ammo_b == 0:
                    self.last_reload_b = time.time()

    def shoot_c(self, add_bullet):
         if self.weapon_ammo_c > 0:
            for i in range(8):
                add_bullet(self.missiles, self.pos(), (self.angle - 40) + (10 * i), 6, 5)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
            self.weapon_ammo_c -= 1
            if self.weapon_ammo_c == 0:
                self.last_reload_c = time.time()

    def map_collision_check(self, arena_map_array, move_array, speed):
        result = 1
        prev_x, prev_y = self.x, self.y

        if move_array[2]:
            self.x -= speed
        elif move_array[3]:
            self.x += speed

        if move_array[0]:
            self.y -= speed
        elif move_array[1]:
            self.y += speed

        
        tile_x, tile_y = self.get_tile_occupied(arena_map_array)

        if tile_x >= 0 and tile_y >= 0:
            if arena_map_array[tile_y][tile_x] != 0:
                result = 9

        #print(f"Checking movement: {move_array}, arena value: {arena_map_array[tile_y][tile_x] if tile_x >= 0 and tile_y >= 0 else 'out of bounds'}")

        self.x = prev_x
        self.y = prev_y

        return result


    def move(self, arena_map_array, move_array):
        ppx, ppy = self.x, self.y
        if move_array[2]:
            self.direction = 2
            self.x -= self.speed
        elif move_array[3]:
            self.direction = 3
            self.x += self.speed

        tile_x, tile_y = self.get_tile_occupied(arena_map_array)

        if tile_x >= 0 and tile_y >= 0:
            if arena_map_array[tile_y][tile_x] != 0:
                self.x = ppx

        if move_array[0]:
            self.direction = 0
            self.y -= self.speed
        elif move_array[1]:
            self.direction = 1
            self.y += self.speed

        tile_x, tile_y = self.get_tile_occupied(arena_map_array)

        if tile_x >= 0 and tile_y >= 0:
            if arena_map_array[tile_y][tile_x] != 0:
                self.y = ppy

    def update(self):
        if self.weapon_ammo_a == 0:
            if time.time() - self.last_reload_a > self.reload_timer_a:
                self.weapon_ammo_a = self.weapon_ammo_max_a

        if self.weapon_ammo_b == 0:
            if time.time() - self.last_reload_b > self.reload_timer_b:
                self.weapon_ammo_b = self.weapon_ammo_max_b

        if self.weapon_ammo_c == 0:
            if time.time() - self.last_reload_c > self.reload_timer_c:
                self.weapon_ammo_c = self.weapon_ammo_max_c

        dist = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
        if dist < 360:
            self.lock_type = 1
        else:
            self.lock_type = 0

    def center(self):
        return (self.x + (self.size * 0.5), self.y + (self.size * 0.5))

    def lock_on(self, actor, index):
        x,y = self.center()
        target_x, target_y = actor[index].center()
        dist_x = target_x - x
        dist_y = target_y - y

        angle = math.atan2(dist_x, dist_y)
        angle_degrees = math.degrees(angle)

        self.angle = angle_degrees + 180

    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime