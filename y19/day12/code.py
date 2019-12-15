import math
import re

from util import get_fname

fname = get_fname(__file__)


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0

        self.initial_x = x
        self.initial_y = y
        self.initial_z = z

    def set_vel(self, moons):
        for moon in moons:
            if self.x < moon.x:
                self.vel_x += 1
            if self.x > moon.x:
                self.vel_x -= 1
            if self.y < moon.y:
                self.vel_y += 1
            if self.y > moon.y:
                self.vel_y -= 1
            if self.z < moon.z:
                self.vel_z += 1
            if self.z > moon.z:
                self.vel_z -= 1

    def apply_vel(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z

    @property
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self):
        return abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def __str__(self):
        return (f"pos=<x={self.x}, y={self.y}, z={self.z}>, "
                f"vel=<x={self.vel_x}, y={self.vel_y}, z={self.vel_z}>")


def load_moons():
    moon_match = re.compile(r'^<x=(.*), y=(.*), z=(.*)>$')
    moons = []
    with open(fname) as f:
        data = f.read().split('\n')
        for moon in data:
            x, y, z = moon_match.fullmatch(moon).groups()
            moons.append(Moon(int(x), int(y), int(z)))
    return moons


def step(moons):
    for moon in moons:
        moon.set_vel(moons)
    for moon in moons:
        moon.apply_vel()


def solve_pt1():
    moons = load_moons()
    for i in range(1000):
        step(moons)
    print(sum([moon.total_energy for moon in moons]))


def solve_pt2():
    moons = load_moons()
    cnt = 0
    next_same_x = 0
    next_same_y = 0
    next_same_z = 0
    while True:
        same_x = True
        same_y = True
        same_z = True
        step(moons)
        cnt += 1
        for moon in moons:
            if moon.vel_x != 0 or moon.x != moon.initial_x:
                same_x = False
            if moon.vel_y != 0 or moon.y != moon.initial_y:
                same_y = False
            if moon.vel_z != 0 or moon.z != moon.initial_z:
                same_z = False
        if next_same_x == 0 and same_x is True:
            next_same_x = cnt
        if next_same_y == 0 and same_y is True:
            next_same_y = cnt
        if next_same_z == 0 and same_z is True:
            next_same_z = cnt
        if next_same_x != 0 and next_same_y != 0 and next_same_z != 0:
            break

    def lcm(a, b):
        """Compute the lowest common multiple of a and b"""
        return int(a * b / math.gcd(a, b))

    print(lcm(lcm(next_same_x, next_same_y), next_same_z))
