from collections import namedtuple
from heapq import heappop, heappush
import json

def make_checker(rule, items):
    consumes = ()
    requirements = ()

    if rule.get("Consumes") != None:
        consumes = itemsToTuple(rule["Consumes"], items)

    if rule.get("Requires") != None:
        requirements = itemsToTuple(rule["Requires"], items)

    def check(state):
        if contains(state, requirements) == False:
            return False

        if contains(state, consumes) == False:
            return False

        return True

    return check

def make_effector(rule, items):
    consumes = ()
    produces = ()

    if rule.get("Consumes") != None:
        consumes = itemsToTuple(rule["Consumes"], items)

    if rule.get("Produces") != None:
        produces = itemsToTuple(rule["Produces"], items)

    def effect(state):
        nextState = state;

        if consumes != () and nextState != ():
            nextState = combineTuple(nextState, consumes, "sub")

        if produces != () and nextState != ():
            nextState = combineTuple(nextState, produces, "add")

        return nextState

    return effect

def heuristic(node, nextNode, bases):
    cost = 0

    if nextNode != () and bases != ():
        for i, amount in enumerate(bases):
            if nextNode[i] >= amount:
                cost += 1000

    for i in xrange(len(node)):
        if node[i] >= nextNode[i] and node[i] != 0 and nextNode[i] != 0:
            cost -= 1

    # bench
    if nextNode[0] > 1:
        cost += float("inf")

    # furnace
    if nextNode[4] > 1:
        cost += float("inf")

    # iron_axe
    if nextNode[6] > 1:
        cost += float("inf")

    # iron_pickaxe
    if nextNode[7] > 1:
        cost += float("inf")

    # stone_axe
    if nextNode[12] > 1:
        cost += float("inf")

    # stone_pickaxe
    if nextNode[13] > 1:
        cost += float("inf")

    # wooden_axe
    if nextNode[15] > 1:
        cost += float("inf")

    # wooden_pickaxe
    if nextNode[16] > 1:
        cost += float("inf")

    # coal
    if nextNode[2] > 1:
        cost += float("inf")

    # cobble
    if nextNode[3] > 8:
        cost += float("inf")

    # ingot
    if nextNode[5] > 6:
        cost += float("inf")

    # ore
    if nextNode[8] > 1:
        cost += float("inf")

    # plank
    if nextNode[9] > 4:
        cost += 1

    # stick
    if nextNode[11] > 8:
       cost += float("inf")

    # wood
    if nextNode[14] > 1:
        cost += float("inf")

    return cost

def graph(state, recipes):
    adjacent = []

    for recipe in recipes:
        if recipe.check(state):
            adjacent.append((recipe.cost, recipe.effect(state), recipe.name))

    return adjacent


def plan(graph, state, items, goals, recipes, bases):
    dist = {}
    prev = {}
    name = {}
    initial = itemsToTuple(state, items)
    goal = itemsToTuple(goals, items)
    dist[initial] = 0
    prev[initial] = None
    name[initial] = "initial"
    heap = [(dist[initial], initial, name[initial])]

    while heap:
        node = heappop(heap)

        if contains(node[1], goal):
            break

        for nextNode in graph(node[1], recipes):
            distance = nextNode[0] + dist[node[1]]

            if nextNode[1] not in dist or distance < dist[nextNode[1]]:
                dist[nextNode[1]] = distance
                prev[nextNode[1]] = node[1]
                name[nextNode[1]] = nextNode[2]
                cost = dist[nextNode[1]] + heuristic(node[1], nextNode[1], bases)
                heappush(heap, (cost, nextNode[1], nextNode[2]))

    path = []

    if contains(node[1], goal):
        node = node[1]

        while node:
            path.append((name[node], dist[node]))
            node = prev[node]

        path.reverse()

    for i in xrange(len(path)):
        print(path[i])

    print("Length: " + str(len(path) - 1))

def itemsToTuple(inventory, items):
    return tuple(int(inventory.get(name, 0)) for i, name in enumerate(items))

def make_recipes(recipes, items):
    Recipe = namedtuple("Recipe", ["name", "check", "effect", "cost"])
    allRecipes = []

    for name, rule in recipes.items():
        checker = make_checker(rule, items)
        effector = make_effector(rule, items)
        recipe = Recipe(name, checker, effector, rule["Time"])
        allRecipes.append(recipe)

    return allRecipes

def contains(have, want):
    if have != () and want != ():
        for i, amount in enumerate(want):
            if have[i] < amount:
                return False

    return True

def combineTuple(firstTuple, secondTuple, operator):
    if operator == "add":
        return tuple(firstTuple[i] + amount for i, amount in enumerate(secondTuple))
    elif operator == "sub":
        return tuple(firstTuple[i] - amount for i, amount in enumerate(secondTuple))

def findBase(state, goals, recipes, items, iterations):
    goalList = []

    for i, name in enumerate(goals):
        goalList.append(name)

    consumes = tuple(0 for i in xrange(len(state)))

    depth = 0

    while goalList and depth < iterations:
        currentGoal = goalList.pop()

        for index, name in enumerate(recipes):
            if recipes[name]["Produces"].get(currentGoal) != None:
                if recipes[name].get("Consumes") != None:
                    requirements = itemsToTuple(recipes[name]["Consumes"], items)
                    consumes = combineTuple(consumes, requirements, "add")

                    for i, item in enumerate(recipes[name]["Consumes"]):
                        goalList.append(item)

                if recipes[name].get("Requires") != None:
                    requirements = itemsToTuple(recipes[name]["Requires"], items)
                    consumes = combineTuple(consumes, requirements, "add")

                    for i, item in enumerate(recipes[name]["Requires"]):
                        goalList.append(item)

        depth += 1

    return consumes


def planner(inputFile):
    with open(inputFile) as f:
        Crafting = json.load(f)

    inventory = Crafting["Initial"]
    items = Crafting["Items"]
    goals = Crafting["Goal"]
    recipes = make_recipes(Crafting["Recipes"], items)
    bases = findBase(itemsToTuple(inventory, items), goals, Crafting["Recipes"], items, 5)
    print(bases)

    plan(graph, inventory, items, goals, recipes, bases)

if __name__ ==  "__main__":
    import sys
    _, filename  = sys.argv
    planner(filename)
