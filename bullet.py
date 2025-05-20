import sys, pygame, math, time, random, csv

class Bullet:
    def __init__(self, x, y, angle, speed, lifetime):
        self.x = x
        self.y = y
        self.angle = math.radians(angle - 90)  # Convert to radians for movement
        self.speed = speed
        self.creation_time = time.time()
        self.lifetime = lifetime

    def move(self, arena_arr):
        self.x -= math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        one_over_tile_size = 1/32
        bullet_size = 4
        
        bullet_tile_x, bullet_tile_y = math.floor((self.x) * one_over_tile_size),math.floor((self.y) * one_over_tile_size)
        if arena_arr[bullet_tile_y][bullet_tile_x] != 0:
            self.lifetime = 0

        bullet_tile_x, bullet_tile_y = math.floor((self.x + bullet_size) * one_over_tile_size),math.floor((self.y + bullet_size) * one_over_tile_size)
        if arena_arr[bullet_tile_y][bullet_tile_x] != 0:
            self.lifetime = 0


    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime
