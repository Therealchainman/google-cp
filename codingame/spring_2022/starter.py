import sys
import math
from heapq import heappush, heappop, heapify, nsmallest, nlargest
from collections import defaultdict
from itertools import product

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

# game loop
while True:
    for i in range(2):
        health, mana = [int(j) for j in input().split()]
    entity_count = int(input()) 
    entities = defaultdict(dict)
    spiders = dict()
    my_player = []
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        entities[_type][_id] = {
          'x' : x,
          'y' : y,
          'shield_life' : shield_life,
          'is_controlled' : is_controlled,
          'health' : health,
          'vx' : vx,
          'vy' : vy,
          'near_base' : near_base,
          'threat_for' : threat_for
        }
        if _type == 0:
          spiders[_id] = entities[_type][_id]
        elif _type == 1:
          my_player.append(entities[_type][_id])
    # rank the spider threats and have my 3 warriors attack the 3 closest spiders
    spiders_rank = []
    for spider in spiders.values():
      threat = 0
      if spider['near_base'] == 1 == spider['threat_for']:
        threat -= 1000
      threat += math.hypot(abs(base_x - spider['x']), abs(base_y - spider['y']))
      spiders_rank.append((threat, (spider['x'], spider['y'])))
    heapify(spiders_rank)
    spiders = nsmallest(3, spiders_rank)
    print("\n".join(map(str,spiders)), file=sys.stderr, flush=True)
    movements = [(base_x, base_y) for _ in range(3)]
    used = [0]*3
    for i in range(len(spiders)):
      closest = math.inf
      x_spider, y_spider = spiders[i][1]
      player = -1
      for j in range(len(spiders)):
        if used[j]: continue
        x, y = my_player[j]['x'], my_player[j]['y']
        dist = math.hypot(abs(x - x_spider), abs(y - y_spider))
        if dist < closest:
          closest = dist
          movements[j] = (x_spider, y_spider)
          player = j
      if player != -1:
        used[player] = 1


    for i in range(heroes_per_player):
        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        x, y = movements[i]
        if x==base_x and y==base_y:
            print(f"WAIT {i}")
        else:
            print(f"MOVE {x} {y} {i}")

