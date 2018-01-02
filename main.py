from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Offense Magic
fireball = Spell("Fire", 10, 100, "Fire")
blizzard = Spell("Blizzard", 12, 170, "Ice")
thunderbolt = Spell("Thunderbolt", 10, 160, "Lightning")


# Defense Magic
cure = Spell("Cure", 10, 100, "White")

# Items
apple = Item("Apple", "potion", "Heals 50 HP", 50, 5)
potion = Item("Potion", "potion", "Heals 70 HP", 70, 5)
elixer = Item("Elixer", "potion", "Heals 100 HP", 100, 1)

grenade = Item("Grenade", "utility", "Deals 200 damage", 200, 1)

# Instantiate People
player_spells = [fireball, blizzard, thunderbolt, cure]
player_items = [apple, potion, elixer, grenade]
player = Person("Player1", 460, 65, 60, 34, player_spells, player_items)
enemy = Person("Imp", 1200, 65, 45, 25, [], [])

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=======================")
    player.choose_action()
    choice = input("Choose action: ")
    index = int(choice) - 1

    # Normal Attack
    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("\n" + "You attacked for", bcolors.WARNING, dmg, bcolors.ENDC, "points of damage.\n" + "Enemy Hp:", bcolors.WARNING, enemy.get_hp(), bcolors.ENDC)

    # Magic Attack
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose spell: ")) - 1

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_dmg()
        current_mp = player.get_mp()
        player.reducemp(spell.cost)

        # Mp check
        if spell.cost > current_mp:
            print(bcolors.FAIL + "Insufficient MP" + bcolors.ENDC)
            continue

        # Check spell type
        if spell.type == "White":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg) + bcolors.ENDC)

        else:
            enemy.take_damage(magic_dmg)
            print("\n" + spell.name + " deals", bcolors.OKBLUE, str(magic_dmg), "points of damage", bcolors.ENDC)

    # Item Usage
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: ")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]

        if item.qty <= 0:
            print(bcolors.WARNING + "Item does not exist" + bcolors.ENDC)
            continue

        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + str(item.name) + " heals for", str(item.prop), "HP" + bcolors.ENDC)
        elif item.type == "utility":
            enemy.take_damage(item.prop)
            print(bcolors.OKBLUE + "\n" + str(item.name) + " deals for", str(item.prop), "points of damage" + bcolors.ENDC)

        item.qty -= 1

    # Default enemy choice
    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print(enemy.name + " attacks for", bcolors.WARNING, enemy_dmg, bcolors.ENDC, "points of damage.\n" + bcolors.ENDC)

    # Possible to add AI for enemy
    # 1. Generate random number for enemy choice (Offense mode) eg. Normal Attack/Spells
    # 2. Switch to Defense mode when hp is under a certain threshold and use healing spells to recover (if any)

    # Summary of player and enemy state
    print("=======================")
    print(bcolors.OKGREEN + player.name + " HP", str(player.get_hp()), "/", str(player.get_maxhp()))
    print(player.name + " MP", str(player.get_mp()), "/", str(player.get_maxmp()), "\n", bcolors.ENDC)
    print(bcolors.FAIL + enemy.name + " HP", str(enemy.get_hp()), "/", enemy.get_maxhp(), bcolors.ENDC)

    # Win/lose condition
    if enemy.hp == 0:
        print(bcolors.OKGREEN + "You win!", bcolors.ENDC)
        running = False
    elif player.hp == 0:
        print(bcolors.OKGREEN + "You failed!", bcolors.ENDC)
        running = False
