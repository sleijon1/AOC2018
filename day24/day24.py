import re
from copy import deepcopy
from math import floor


class Group:
    def __init__(self, hp, im, dmg, dmg_type, init, wkns, u, tp, ID):
        self.TYPE = tp
        self.hit_points = hp
        self.immunities = im
        self.damage = dmg
        self.damage_type = dmg_type
        self.initiative = init
        self.weaknesses = wkns
        self.units = u
        self.target = None
        self.ID = str(ID)

    def __str__(self):
        return str(
            self.ID + self.TYPE + " - " + str(self.units) + " units each with " + str(self.hit_points) +\
            "( immune to, " + str(self.immunities) + "; weak to " + str(self.weaknesses) + ") " \
            + "with an attack that does " + str(self.damage) + " " + self.damage_type \
            + " at initiative " + str(self.initiative)
        )

    def __repr__(self):
        return str(self)

    def compact_str(self):
        return str(self.ID + self.TYPE)

    def effective_power(self):
        return self.damage*self.units

    def set_target(self, group):
        self.target = group

    def attack(self):
        dmg = damage_potential(self, self.target)
        units_dead = min(self.target.units, dmg // self.target.hit_points)
        self.target.units -= units_dead
        # print("attacker: " + self.TYPE + " " +str(self.ID) + \
        #      " defender: " + self.target.TYPE + " " + str(self.target.ID) + \
        #      " killing " + str(units_dead))
        return self.target.units

    def eq(self, other):
        return (
            self.__class__ == other.__class__ and
            self.ID == other.ID and
            self.TYPE == other.TYPE
        )


""" ---------------------------- PARSING ----------------------------  """

ims, inf = open("input.txt").read().split("Infection:")
ims = ims.strip()
ims_groups = ims.split("\n")
ims_groups.pop(0)
inf = inf.strip()
inf_groups = inf.split("\n")

def create_group(groups, TYPE, boost=0):
    """ creates Group classes of all groups """
    army = []
    for i, grp in enumerate(groups):
        immunities = []
        weak = []
        disp = re.search('\(([^)]+)\)', grp)
        if disp:
            disp = disp[0]
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
        army.append(Group(hp, immunities, dmg+boost, dmg_type, initiative,
                                   weak, units, TYPE, i+1))
    return army

""" ---------------------------- PARSING ----------------------------  """

def damage_potential(attacker, defender):
    """ returns damage potential for attacker on defender """
    if attacker.damage_type in defender.weaknesses:
        return attacker.damage * attacker.units * 2
    elif attacker.damage_type in defender.immunities:
        return 0
    else:
        return attacker.damage * attacker.units

def target_selection(ims_army, inf_army):
    groups = ims_army+inf_army
    order = [(group, group.effective_power(), group.initiative) for group in groups]
    order.sort(key=lambda x: (x[1], x[2]), reverse = True)
    opponent = {"inf": list(ims_army), "ims": list(inf_army)}
    for attacker in order:
        grp = attacker[0]
        defender = opponent[grp.TYPE]
        possibilities = [(def_grp, damage_potential(grp, def_grp),
                        def_grp.effective_power(),
                        def_grp.initiative)
                        for def_grp in defender]
        possibilities.sort(key = lambda x: (x[1], x[2], x[3]), reverse = True)
        if possibilities and damage_potential(grp, possibilities[0][0]) > 0:
            grp.set_target(possibilities[0][0])
            opponent[grp.TYPE].remove(possibilities[0][0])
        else:
            grp.set_target(None)

def war(ims_army, inf_army):
    all_grps = ims_army + inf_army
    all_grps.sort(key=lambda x: x.initiative, reverse=True)
    opponent = {"inf": ims_army, "ims": inf_army}
    while ims_army and inf_army:
        target_selection(ims_army, inf_army)
        no_target = 0
        draw = False

        for grp in all_grps:
            #print(grp)
            if grp.target is None:
                no_target += 1
                if no_target == len(all_grps):
                    draw = True
                    break
                continue
            if grp.target is not None:
                remaining_hp = grp.attack()
                if remaining_hp == 0:
                    all_grps.remove(grp.target)
                    opponent[grp.TYPE].remove(grp.target)
                grp.target = None
        if draw:
            print("draw")
            break
    # if draw:
    #     print("draw.")
    #print(all_grps)
    print("Winners type = " + all_grps[0].TYPE + " | units left = " + \
          str(sum([group.units for group in all_grps])))
    return all_grps, all_grps[0].TYPE

""" PART 1 """
all_grps, _ = war(create_group(ims_groups, TYPE="ims"), create_group(inf_groups, TYPE="inf"))
print(all_grps)
print("Solution part 1: type = " + all_grps[0].TYPE + " | units left = " + \
      str(sum([group.units for group in all_grps])))

""" PART 2 """
def boost_ims():
    """ boosts immune system until it defeats the infection """
    winner_type = None
    boost = 0
    inf_army = None
    while inf_army is None or len(inf_army):
        ims_army = create_group(ims_groups, TYPE="ims", boost=boost)
        inf_army = create_group(inf_groups, TYPE="inf")
        winners, winner_type = war(ims_army, inf_army)
        boost += 1
    print("Solution part 2: type = " + winners[0].TYPE + " | units left = " + \
          str(sum([g.units for g in winners])) + " | amount of boost: " + str(boost-1))

boost_ims()
