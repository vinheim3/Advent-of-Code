from util import get_fname

fname = get_fname(__file__)


class Planet:
    def __init__(self, name):
        self.name = name
        self.orbits = None
        self.orbit_list = None

    def get_orbitted(self):
        if self.orbit_list is not None:
            return self.orbit_list

        if self.orbits is None:
            self.orbit_list = []
        else:
            self.orbit_list = [self.orbits, *self.orbits.get_orbitted()]
        return self.orbit_list


def load_orbit_map():
    with open(fname) as f:
        data = f.read().split('\n')

    planet_map = {}

    for row in data:
        orbitted, orbitter = row.split(')')
        planet_map.setdefault(orbitted, Planet(orbitted))
        planet_map.setdefault(orbitter, Planet(orbitter))

        planet_map[orbitter].orbits = planet_map[orbitted]

    return planet_map


def solve_pt1():
    orbit_map = load_orbit_map()
    print(sum([len(pl.get_orbitted()) for pl in orbit_map.values()]))


def solve_pt2():
    orbit_map = load_orbit_map()
    you_orbits = orbit_map['YOU'].get_orbitted()

    san_orbits_dict = {}
    cnt_san = 0
    for planet in orbit_map['SAN'].get_orbitted():
        san_orbits_dict[planet.name] = cnt_san
        cnt_san += 1

    cnt_you = 0
    for planet in you_orbits:
        if planet.name in san_orbits_dict:
            print(cnt_you + san_orbits_dict[planet.name])
            return
        cnt_you += 1
