import sys, pygame, math, time, random, csv

class Bullet:
    def __init__(self, x, y, angle, speed, lifetime):
        self.x = x
        self.y = y
        self.angle = math.radians(angle - 90)  # Convert to radians for movement
        self.speed = speed
        self.creation_time = time.time()
        self.lifetime = lifetime
        self.target = None

    def move(self, arena_arr, angle_to_point):
        locked_on = False
        if self.target != None:
            if time.time() - self.creation_time > (self.lifetime * 0.25):
                locked_on = True
                

            dist = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if dist > 360:
                locked_on = False



        if locked_on:
            #todo: figure out why this didn't work
            #self.angle = angle_to_point((self.x,self.y),(self.target.x,self.target.y))
            if self.x < self.target.x: self.x += self.speed
            if self.x > self.target.x: self.x -= self.speed
            if self.y < self.target.y: self.y += self.speed
            if self.y > self.target.y: self.y -= self.speed
        else:
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
