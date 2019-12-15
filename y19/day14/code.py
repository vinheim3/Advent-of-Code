import math

from util import get_fname

fname = get_fname(__file__)


class Material:
    def __init__(self, name):
        self.name = name
        self.provides = 0
        self.reqs = []  # list of [cnt, material]
        self.parents = []
        self.children = []

    def __repr__(self):
        return self.name

    def remove_child(self, child):
        idx = -1
        for i, c in enumerate(self.children):
            if c == child:
                idx = i
                break
        self.children.pop(idx)


def load_reactions():
    with open(fname) as f:
        data = f.read().split('\n')

    mapping = {}

    def get_material_cnt(string):
        _cnt, material = string.split(' ')
        _cnt = int(_cnt)
        mapping.setdefault(material, Material(material))
        return material, _cnt

    # load
    for reaction in data:
        mats_in_full, mat_out_full = reaction.split(' => ')

        # for out, set how much it provides
        mat_out, cnt = get_material_cnt(mat_out_full)
        mapping[mat_out].provides = cnt

        for req in mats_in_full.split(', '):
            mat_in, cnt = get_material_cnt(req)
            # material's parent is the stuff that comes out of it
            # material's children is the requirements
            mapping[mat_out].reqs.append((cnt, mapping[mat_in]))
            mapping[mat_in].parents.append(mapping[mat_out])
            mapping[mat_out].children.append(mapping[mat_in])

    return mapping


def load_hierarchy(mapping):  # TODO: do I need a hierarchy?
    # child ------------------------- parent
    # [[ORE], [A, B], [C], [D], [E], [FUEL]]
    mats = set(mapping.values())
    base = mapping['ORE']
    mats -= {base}
    layers = [[base]]
    for parent in base.parents:
        parent.remove_child(base)
    while len(mats) > 0:
        layer = []
        for mat in mats:
            if not mat.children:
                layer.append(mat)
        layers.append(layer)
        for mat in layer:
            for parent in mat.parents:
                parent.remove_child(mat)
        mats -= set(layer)
    return layers


def get_cost(mat_cost, hierarchy):
    spare_mats = {}

    for layer in list(reversed(hierarchy))[:-1]:
        for ele in layer:
            if ele.name not in mat_cost:
                continue

            required = mat_cost[ele.name]
            spare_mats.setdefault(ele.name, 0)
            have = math.ceil((required - spare_mats[ele.name]) / ele.provides)
            spare_mats[ele.name] = spare_mats[ele.name] + (have * ele.provides) - required

            for cnt, mat in ele.reqs:
                mat_cost.setdefault(mat.name, 0)
                mat_cost[mat.name] += have * cnt
    return mat_cost


def solve_pt1():
    reactions = load_reactions()
    hierarchy = load_hierarchy(reactions)
    mat_cost = {'FUEL': 1}

    cost = get_cost(mat_cost, hierarchy)
    print(cost['ORE'])


def solve_pt2():
    reactions = load_reactions()
    hierarchy = load_hierarchy(reactions)

    max_ore = 1000000000000

    left, right = 1, max_ore

    while right != left + 1:
        mid = (right - left) // 2 + left
        cost = get_cost({'FUEL': mid}, hierarchy)
        if cost['ORE'] > max_ore:
            right = mid
        else:
            left = mid

    print(left)
