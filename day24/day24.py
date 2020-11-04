import re
from copy import deepcopy

class Group:
    def __init__(self, hp, im, dmg, dmg_type, init, wkns, u, tp):
        self.TYPE = tp
        self.hit_points = hp
        self.immunities = im
        self.damage = dmg
        self.damage_type = dmg_type
        self.initiative = init
        self.weaknesses = wkns
        self.units = u
        self.target = None

    def __str__(self):
        return str((self.hit_points, self.immunities, self.damage,
                    self.damage_type, self.initiative, self.weaknesses,
                    self.units, self.TYPE))

    def __repr__(self):
        return str(self)

    def effective_power(self):
        return self.damage*self.units

    def set_target(self, group):
        self.target = group

ims, inf = open("test.txt").read().split("Infection:")
ims = ims.strip()
ims_groups = ims.split("\n")
ims_groups.pop(0)
inf = inf.strip()
inf_groups = inf.split("\n")

inf_army = []
ims_army = []

def create_group(groups, TYPE):
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
            disp1 = [d.strip(",") for d in disp1]
            if disp1[0] == "immune":
                immunities = disp1[2:]
            elif disp1[0] == "weak":
                weak = disp1[2:]
        if disp2:
            disp2 = disp2[0].split(" ")  # ["immune", "to" ...]
            disp2 = [d.strip(",") for d in disp2]
            if disp2[0] == "immune":
                immunities = disp2[2:]
            elif disp2[0] == "weak":
                weak = disp2[2:]
        units, hp, dmg, initiative = map(int, re.findall(r"\d+", grp))
        dmg_type = re.search("\d+ \w* damage", grp)[0].split(" ")[1]
        army.append(Group(hp, immunities, dmg, dmg_type, initiative,
                                   weak, units, TYPE))
    return army

ims_army = create_group(ims_groups, TYPE="ims")
inf_army = create_group(inf_groups, TYPE="inf")

def damage_potential(attacker, defender):
    """ returns damage potential for attacker on defender """
    if attacker.damage_type in defender.weaknesses:
        print(attacker.damage*attacker.units*2)
        return attacker.damage * attacker.units * 2
    elif attacker.damage_type in defender.immunities:
        return 0
    else:
        print(attacker.damage*attacker.units)
        return attacker.damage * attacker.units

def target_selection(ims_army_or, inf_army_or):
    all_grps = []
    ims_army = deepcopy(ims_army_or)
    inf_army = deepcopy(inf_army_or)
    for grp in ims_army_or:
        all_grps.append(grp)
    for grp in inf_army_or:
        all_grps.append(grp)
    order = []
    for group in all_grps:
        order.append([group, group.effective_power(), group.initiative])
    order.sort(key=lambda x: (x[1], x[2]))  # effective power then initiative
    order.reverse() # for looping
    for attacker in order:
        grp = attacker[0]
        if grp.TYPE == "inf":
            target = None
            target_i = None
            for i, ims_grp in enumerate(ims_army):
                if target is None or \
                   damage_potential(grp, ims_grp) >\
                   damage_potential(grp, target):
                    target = ims_grp
                    target_i = i
                elif damage_potential(grp, ims_grp) \
                    == damage_potential(grp, target):
                    if ims_grp.effective_power() > target.effective_power():
                        target = ims_grp
                        target_i = i
                    elif ims_grp.effective_power() == target.effective_power():
                        if ims_grp.initiative > target.initiative:
                            target = ims_grp
                            target_i = i
            if damage_potential(grp, target) == 0:
                target = None
            grp.set_target(target)
            ims_army.pop(target_i)
        elif grp.TYPE == "ims":
            target = None
            target_i = None
            for i, inf_grp in enumerate(inf_army):
                if target is None or \
                   damage_potential(grp, inf_grp) >\
                   damage_potential(grp, target):
                    target = inf_grp
                    target_i = i
                elif damage_potential(grp, inf_grp) \
                    == damage_potential(grp, target):
                    if inf_grp.effective_power() > target.effective_power():
                        target = inf_grp
                        target_i = i
                    elif inf_grp.effective_power() == target.effective_power():
                        if inf_grp.initiative > target.initiative:
                            target = inf_grp
                            target_i = i
            if damage_potential(grp, target) == 0:
                target = None
            grp.set_target(target)
            inf_army.pop(target_i)


target_selection(ims_army, inf_army)
print(inf_army)
for grp in inf_army:
    print(grp.target)

print(ims_army)
for grp in ims_army:
    print(grp.target)















