import re

class Group:
    def __init__(self, hp, im, dmg, dmg_type, init, wkns, u):
        self.hit_points = hp
        self.immunities = im
        self.damage = dmg
        self.damage_type = dmg_type
        self.initiative = init
        self.weaknesses = wkns
        self.units = u
    def __str__(self):
        return str((self.hit_points, self.immunities, self.damage,
                    self.damage_type, self.initiative, self.weaknesses,
                    self.units))
    def __repr__(self):
        return str(self)


ims, inf = open("test.txt").read().split("Infection:")
ims = ims.strip()
ims_groups = ims.split("\n")
ims_groups.pop(0)
inf = inf.strip()
inf_groups = inf.split("\n")

inf_army = []
ims_army = []

def create_group(groups):
    """ creates Group classes of all groups """
    army = []
    for grp in groups:
        immunities = []
        weak = []
        disp = re.search('\(([^)]+)\)', grp)[0]
        disp1 = re.search('immune to[^;)]+', disp)
        disp2 = re.search('weak to[^;)]+', disp)
        if disp1:
            disp1 = disp1[0].split(" ")  # ["immune", "to" ...]
            if disp1[0] == "immune":
                immunities = disp1[2:]
            elif disp1[0] == "weak":
                weak = disp1[2:]
        if disp2:
            disp2 = disp2[0].split(" ")  # ["immune", "to" ...]
            if disp2[0] == "immune":
                immunities = disp2[2:]
            elif disp2[0] == "weak":
                weak = disp2[2:]
        print(immunities, weak)
        units, hp, dmg, initiative = map(int, re.findall(r"\d+", grp))
        dmg_type = re.search("\d+ \w* damage", grp)[0].split(" ")[1] 
        army.append(Group(hp, immunities, dmg, dmg_type, initiative,
                                   weak, units))
    return army

ims_army = create_group(ims_groups)
inf_army = create_group(inf_groups)
print(inf_army)
print(ims_army)






















