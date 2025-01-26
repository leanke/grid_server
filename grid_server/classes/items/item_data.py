from grid_server.classes.items.item import Item
from grid_server.classes.items.armor import Armor
from grid_server.classes.items.weapons import Weapon
from grid_server.classes.items.resources import Resource

# resources
logs = {
    'log': Resource.create_resource('Logs', 'Logs', 1).to_dict(),
    'oak': Resource.create_resource('Oak Logs', 'Oak Logs', 2).to_dict(),
    'willow': Resource.create_resource('Willow Logs', 'Willow Logs', 3).to_dict(),
    'maple': Resource.create_resource('Maple Logs', 'Maple Logs', 4).to_dict(),
    'yew': Resource.create_resource('Yew Logs', 'Yew Logs', 5).to_dict(),
    'magic': Resource.create_resource('Magic Logs', 'Magic Logs', 6).to_dict(),
    'redwood': Resource.create_resource('Redwood Logs', 'Redwood Logs', 7).to_dict(),
    'elder': Resource.create_resource('Elder Logs', 'Elder Logs', 8).to_dict(),
    'crystal': Resource.create_resource('Crystal Logs', 'Crystal Logs', 9).to_dict(),
    'dragon': Resource.create_resource('Dragon Logs', 'Dragon Logs', 10).to_dict(),
}
ores = {
    'stone': Resource.create_resource('Stone', 'Stone', 1).to_dict(),
    'tin': Resource.create_resource('Tin Ore', 'Tin Ore', 2).to_dict(),
    'copper': Resource.create_resource('Copper Ore', 'Copper Ore', 3).to_dict(),
    'iron': Resource.create_resource('Iron Ore', 'Iron Ore', 4).to_dict(),
    'coal': Resource.create_resource('Coal', 'Coal', 5).to_dict(),
    'gold': Resource.create_resource('Gold Ore', 'Gold Ore', 6).to_dict(),
    'mithril': Resource.create_resource('Mithril Ore', 'Mithril Ore', 7).to_dict(),
    'adamant': Resource.create_resource('Adamantite Ore', 'Adamantite Ore', 8).to_dict(),
    'rune': Resource.create_resource('Runite Ore', 'Runite Ore', 9).to_dict(),
    'dragon': Resource.create_resource('Dragonite Ore', 'Dragonite Ore', 10).to_dict(),
}
leather = {
    'leather': Resource.create_resource('Leather', 'Leather', 1).to_dict(),
    'hardened': Resource.create_resource('Hardened Leather', 'Hardened Leather', 2).to_dict(),
    'studded': Resource.create_resource('Studded Leather', 'Studded Leather', 3).to_dict(),
    'snakeskin': Resource.create_resource('Snakeskin Leather', 'Snakeskin Leather', 4).to_dict(),
    'green_dhide': Resource.create_resource('Green Dragonhide Leather', 'Green Dragonhide Leather', 5).to_dict(),
    'blue_dhide': Resource.create_resource('Blue Dragonhide Leather', 'Blue Dragonhide Leather', 6).to_dict(),
    'red_dhide': Resource.create_resource('Red Dragonhide Leather', 'Red Dragonhide Leather', 7).to_dict(),
    'black_dhide': Resource.create_resource('Black Dragonhide Leather', 'Black Dragonhide Leather', 8).to_dict(),
    'royal_dhide': Resource.create_resource('Royal Dragonhide Leather', 'Royal Dragonhide Leather', 9).to_dict(),
    'elder_dhide': Resource.create_resource('Elder Dragonhide Leather', 'Elder Dragonhide Leather', 10).to_dict(),
}

resources = {
    'log': logs,
    'ore': ores,
    'leather': leather,
}

# melee armor
melee_helmet = { # head
    'helmet': Armor.create_armor('Helmet', 'A Helmet', 1, 'head', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Helmet', 'A Bronze Helmet', 2, 'head', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Helmet', 'An Iron Helmet', 3, 'head', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Helmet', 'A Steel Helmet', 4, 'head', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Helmet', 'A Mithril Helmet', 5, 'head', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Helmet', 'An Adamantite Helmet', 6, 'head', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Helmet', 'A Rune Helmet', 7, 'head', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Helmet', 'A Dragon Helmet', 8, 'head', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Helmet', 'A Crystal Helmet', 9, 'head', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Helmet', 'An Elder Helmet', 10, 'head', 'melee').to_dict(),
}
melee_chestplate = { # body
    'chestplate': Armor.create_armor('Chestplate', 'A Chestplate', 1, 'body', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Chestplate', 'A Bronze Chestplate', 2, 'body', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Chestplate', 'An Iron Chestplate', 3, 'body', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Chestplate', 'A Steel Chestplate', 4, 'body', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Chestplate', 'A Mithril Chestplate', 5, 'body', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Chestplate', 'An Adamantite Chestplate', 6, 'body', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Chestplate', 'A Rune Chestplate', 7, 'body', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Chestplate', 'A Dragon Chestplate', 8, 'body', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Chestplate', 'A Crystal Chestplate', 9, 'body', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Chestplate', 'An Elder Chestplate', 10, 'body', 'melee').to_dict(),
}
melee_platelegs = { # legs
    'plateleg': Armor.create_armor('Platelegs', 'A Platelegs', 1, 'legs', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Platelegs', 'A Bronze Platelegs', 2, 'legs', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Platelegs', 'An Iron Platelegs', 3, 'legs', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Platelegs', 'A Steel Platelegs', 4, 'legs', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Platelegs', 'A Mithril Platelegs', 5, 'legs', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Platelegs', 'An Adamantite Platelegs', 6, 'legs', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Platelegs', 'A Rune Platelegs', 7, 'legs', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Platelegs', 'A Dragon Platelegs', 8, 'legs', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Platelegs', 'A Crystal Platelegs', 9, 'legs', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Platelegs', 'An Elder Platelegs', 10, 'legs', 'melee').to_dict(),
}
melee_gauntlets = { # hands
    'gauntlet': Armor.create_armor('Gauntlets', 'A Gauntlets', 1, 'hands', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Gauntlets', 'A Bronze Gauntlets', 2, 'hands', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Gauntlets', 'An Iron Gauntlets', 3, 'hands', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Gauntlets', 'A Steel Gauntlets', 4, 'hands', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Gauntlets', 'A Mithril Gauntlets', 5, 'hands', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Gauntlets', 'An Adamantite Gauntlets', 6, 'hands', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Gauntlets', 'A Rune Gauntlets', 7, 'hands', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Gauntlets', 'A Dragon Gauntlets', 8, 'hands', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Gauntlets', 'A Crystal Gauntlets', 9, 'hands', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Gauntlets', 'An Elder Gauntlets', 10, 'hands', 'melee').to_dict(),
}
melee_boots = { # feet
    'boots': Armor.create_armor('Boots', 'A Boots', 1, 'feet', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Boots', 'A Bronze Boots', 2, 'feet', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Boots', 'An Iron Boots', 3, 'feet', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Boots', 'A Steel Boots', 4, 'feet', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Boots', 'A Mithril Boots', 5, 'feet', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Boots', 'An Adamantite Boots', 6, 'feet', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Boots', 'A Rune Boots', 7, 'feet', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Boots', 'A Dragon Boots', 8, 'feet', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Boots', 'A Crystal Boots', 9, 'feet', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Boots', 'An Elder Boots', 10, 'feet', 'melee').to_dict(),
}
swords = { # right_hand
    'sword': Weapon.create_weapon('Sword', 'A Sword', 1, 'right_hand', 'melee').to_dict(),
    'bronze': Weapon.create_weapon('Bronze Sword', 'A Bronze Sword', 2, 'right_hand', 'melee').to_dict(),
    'iron': Weapon.create_weapon('Iron Sword', 'An Iron Sword', 3, 'right_hand', 'melee').to_dict(),
    'steel': Weapon.create_weapon('Steel Sword', 'A Steel Sword', 4, 'right_hand', 'melee').to_dict(),
    'mithril': Weapon.create_weapon('Mithril Sword', 'A Mithril Sword', 5, 'right_hand', 'melee').to_dict(),
    'adamant': Weapon.create_weapon('Adamantite Sword', 'An Adamantite Sword', 6, 'right_hand', 'melee').to_dict(),
    'rune': Weapon.create_weapon('Rune Sword', 'A Rune Sword', 7, 'right_hand', 'melee').to_dict(),
    'dragon': Weapon.create_weapon('Dragon Sword', 'A Dragon Sword', 8, 'right_hand', 'melee').to_dict(),
    'crystal': Weapon.create_weapon('Crystal Sword', 'A Crystal Sword', 9, 'right_hand', 'melee').to_dict(),
    'elder': Weapon.create_weapon('Elder Sword', 'An Elder Sword', 10, 'right_hand', 'melee').to_dict(),
}
shields = { # left_hand
    'shield': Armor.create_armor('Shield', 'A Shield', 1, 'left_hand', 'melee').to_dict(),
    'bronze': Armor.create_armor('Bronze Shield', 'A Bronze Shield', 2, 'left_hand', 'melee').to_dict(),
    'iron': Armor.create_armor('Iron Shield', 'An Iron Shield', 3, 'left_hand', 'melee').to_dict(),
    'steel': Armor.create_armor('Steel Shield', 'A Steel Shield', 4, 'left_hand', 'melee').to_dict(),
    'mithril': Armor.create_armor('Mithril Shield', 'A Mithril Shield', 5, 'left_hand', 'melee').to_dict(),
    'adamant': Armor.create_armor('Adamantite Shield', 'An Adamantite Shield', 6, 'left_hand', 'melee').to_dict(),
    'rune': Armor.create_armor('Rune Shield', 'A Rune Shield', 7, 'left_hand', 'melee').to_dict(),
    'dragon': Armor.create_armor('Dragon Shield', 'A Dragon Shield', 8, 'left_hand', 'melee').to_dict(),
    'crystal': Armor.create_armor('Crystal Shield', 'A Crystal Shield', 9, 'left_hand', 'melee').to_dict(),
    'elder': Armor.create_armor('Elder Shield', 'An Elder Shield', 10, 'left_hand', 'melee').to_dict(),
}

melee_items = {
    'head': melee_helmet,
    'body': melee_chestplate,
    'legs': melee_platelegs,
    'hands': melee_gauntlets,
    'feet': melee_boots,
    'right_hand': swords,
    'left_hand': shields,
}

# magic armor
magic_hat = { # head
    'hat': Armor.create_armor('Wizard Hat', 'A Wizard Hat', 1, 'head', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Wizard Hat', 'A Novice Wizard Hat', 2, 'head', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Wizard Hat', 'An Apprentice Wizard Hat', 3, 'head', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Wizard Hat', 'An Adept Wizard Hat', 4, 'head', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Wizard Hat', 'An Expert Wizard Hat', 5, 'head', 'magic').to_dict(),
    'master': Armor.create_armor('Master Wizard Hat', 'A Master Wizard Hat', 6, 'head', 'magic').to_dict(),
    'air': Armor.create_armor('Air Wizard Hat', 'An Air Wizard Hat', 7, 'head', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Wizard Hat', 'A Fire Wizard Hat', 8, 'head', 'magic').to_dict(),
    'water': Armor.create_armor('Water Wizard Hat', 'A Water Wizard Hat', 9, 'head', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Wizard Hat', 'An Earth Wizard Hat', 10, 'head', 'magic').to_dict(),
}
magic_robe_top = { # body
    'robe': Armor.create_armor('Robe', 'A Robe', 1, 'body', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Robe', 'A Novice Robe', 2, 'body', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Robe', 'An Apprentice Robe', 3, 'body', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Robe', 'An Adept Robe', 4, 'body', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Robe', 'An Expert Robe', 5, 'body', 'magic').to_dict(),
    'master': Armor.create_armor('Master Robe', 'A Master Robe', 6, 'body', 'magic').to_dict(),
    'air': Armor.create_armor('Air Robe', 'An Air Robe', 7, 'body', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Robe', 'A Fire Robe', 8, 'body', 'magic').to_dict(),
    'water': Armor.create_armor('Water Robe', 'A Water Robe', 9, 'body', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Robe', 'An Earth Robe', 10, 'body', 'magic').to_dict(),
}
magic_robe_bottom = { # legs
    'robe': Armor.create_armor('Robe Bottom', 'A Robe Bottom', 1, 'legs', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Robe Bottom', 'A Novice Robe Bottom', 2, 'legs', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Robe Bottom', 'An Apprentice Robe Bottom', 3, 'legs', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Robe', 'An Adept Robe Bottom', 4, 'legs', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Robe Bottom', 'An Expert Robe Bottom', 5, 'legs', 'magic').to_dict(),
    'master': Armor.create_armor('Master Robe Bottom', 'A Master Robe Bottom', 6, 'legs', 'magic').to_dict(),
    'air': Armor.create_armor('Air Robe Bottom', 'An Air Robe Bottom', 7, 'legs', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Robe Bottom', 'A Fire Robe Bottom', 8, 'legs', 'magic').to_dict(),
    'water': Armor.create_armor('Water Robe Bottom', 'A Water Robe Bottom', 9, 'legs', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Robe Bottom', 'An Earth Robe Bottom', 10, 'legs', 'magic').to_dict(),
}
magic_gloves = { # hands
    'gloves': Armor.create_armor('Gloves', 'Gloves', 1, 'hands', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Gloves', 'Novice Gloves', 2, 'hands', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Gloves', 'Apprentice Gloves', 3, 'hands', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Gloves', 'Adept Gloves', 4, 'hands', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Gloves', 'Expert Gloves', 5, 'hands', 'magic').to_dict(),
    'master': Armor.create_armor('Master Gloves', 'Master Gloves', 6, 'hands', 'magic').to_dict(),
    'air': Armor.create_armor('Air Gloves', 'Air Gloves', 7, 'hands', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Gloves', 'Fire Gloves', 8, 'hands', 'magic').to_dict(),
    'water': Armor.create_armor('Water Gloves', 'Water Gloves', 9, 'hands', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Gloves', 'Earth Gloves', 10, 'hands', 'magic').to_dict(),
}
magic_boots = { # feet
    'boots': Armor.create_armor('Boots', 'Boots', 1, 'feet', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Boots', 'Novice Boots', 2, 'feet', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Boots', 'Apprentice Boots', 3, 'feet', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Boots', 'Adept Boots', 4, 'feet', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Boots', 'Expert Boots', 5, 'feet', 'magic').to_dict(),
    'master': Armor.create_armor('Master Boots', 'Master Boots', 6, 'feet', 'magic').to_dict(),
    'air': Armor.create_armor('Air Boots', 'Air Boots', 7, 'feet', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Boots', 'Fire Boots', 8, 'feet', 'magic').to_dict(),
    'water': Armor.create_armor('Water Boots', 'Water Boots', 9, 'feet', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Boots', 'Earth Boots', 10, 'feet', 'magic').to_dict(),
}
staffs = { # right_hand
    'staff': Weapon.create_weapon('Staff', 'A Staff', 1, 'right_hand', 'magic').to_dict(),
    'oak': Weapon.create_weapon('Oak Staff', 'An Oak Staff', 2, 'right_hand', 'magic').to_dict(),
    'willow': Weapon.create_weapon('Willow Staff', 'A Willow Staff', 3, 'right_hand', 'magic').to_dict(),
    'maple': Weapon.create_weapon('Maple Staff', 'A Maple Staff', 4, 'right_hand', 'magic').to_dict(),
    'yew': Weapon.create_weapon('Yew Staff', 'A Yew Staff', 5, 'right_hand', 'magic').to_dict(),
    'magic': Weapon.create_weapon('Magic Staff', 'A Magic Staff', 6, 'right_hand', 'magic').to_dict(),
    'redwood': Weapon.create_weapon('Redwood Staff', 'A Redwood Staff', 7, 'right_hand', 'magic').to_dict(),
    'elder': Weapon.create_weapon('Elder Staff', 'An Elder Staff', 8, 'right_hand', 'magic').to_dict(),
    'crystal': Weapon.create_weapon('Crystal Staff', 'A Crystal Staff', 9, 'right_hand', 'magic').to_dict(),
    'dragon': Weapon.create_weapon('Dragon Staff', 'A Dragon Staff', 10, 'right_hand', 'magic').to_dict(),
}
orb = { # left_hand
    'orb': Armor.create_armor('Orb', 'An Orb', 1, 'left_hand', 'magic').to_dict(),
    'novice': Armor.create_armor('Novice Orb', 'A Novice Orb', 2, 'left_hand', 'magic').to_dict(),
    'apprentice': Armor.create_armor('Apprentice Orb', 'An Apprentice Orb', 3, 'left_hand', 'magic').to_dict(),
    'adept': Armor.create_armor('Adept Orb', 'An Adept Orb', 4, 'left_hand', 'magic').to_dict(),
    'expert': Armor.create_armor('Expert Orb', 'An Expert Orb', 5, 'left_hand', 'magic').to_dict(),
    'master': Armor.create_armor('Master Orb', 'A Master Orb', 6, 'left_hand', 'magic').to_dict(),
    'air': Armor.create_armor('Air Orb', 'An Air Orb', 7, 'left_hand', 'magic').to_dict(),
    'fire': Armor.create_armor('Fire Orb', 'A Fire Orb', 8, 'left_hand', 'magic').to_dict(),
    'water': Armor.create_armor('Water Orb', 'A Water Orb', 9, 'left_hand', 'magic').to_dict(),
    'earth': Armor.create_armor('Earth Orb', 'An Earth Orb', 10, 'left_hand', 'magic').to_dict(),
}

magic_items = {
    'head': magic_hat,
    'body': magic_robe_top,
    'legs': magic_robe_bottom,
    'hands': magic_gloves,
    'feet': magic_boots,
    'right_hand': staffs,
    'left_hand': orb,
}

# ranged armor
range_coif = { # head
    'leather': Armor.create_armor('Leather Coif', 'A Leather Coif', 1, 'head', 'range').to_dict(),
    'hardened': Armor.create_armor('Hardened Leather Coif', 'A Hardened Leather Coif', 2, 'head', 'range').to_dict(),
    'studded': Armor.create_armor('Studded Coif', 'A Studded Coif', 3, 'head', 'range').to_dict(),
    'snakeskin': Armor.create_armor('Snakeskin Coif', 'A Snakeskin Coif', 4, 'head', 'range').to_dict(),
    'green_dhide': Armor.create_armor('Green Dragonhide Coif', 'A Green Dragonhide Coif', 5, 'head', 'range').to_dict(),
    'blue_dhide': Armor.create_armor('Blue Dragonhide Coif', 'A Blue Dragonhide Coif', 6, 'head', 'range').to_dict(),
    'red_dhide': Armor.create_armor('Red Dragonhide Coif', 'A Red Dragonhide Coif', 7, 'head', 'range').to_dict(),
    'black_dhide': Armor.create_armor('Black Dragonhide Coif', 'A Black Dragonhide Coif', 8, 'head', 'range').to_dict(),
    'royal_dhide': Armor.create_armor('Royal Dragonhide Coif', 'A Royal Dragonhide Coif', 9, 'head', 'range').to_dict(),
    'elder_dhide': Armor.create_armor('Elder Dragonhide Coif', 'An Elder Dragonhide Coif', 10, 'head', 'range').to_dict(),
}
range_tunic = { # body
    'leather': Armor.create_armor('Leather Tunic', 'A Leather Tunic', 1, 'body', 'range').to_dict(),
    'hardened': Armor.create_armor('Hardened Leather Tunic', 'A Hardened Leather Tunic', 2, 'body', 'range').to_dict(),
    'studded': Armor.create_armor('Studded Tunic', 'A Studded Tunic', 3, 'body', 'range').to_dict(),
    'snakeskin': Armor.create_armor('Snakeskin Tunic', 'A Snakeskin Tunic', 4, 'body', 'range').to_dict(),
    'green_dhide': Armor.create_armor('Green Dragonhide Tunic', 'A Green Dragonhide Tunic', 5, 'body', 'range').to_dict(),
    'blue_dhide': Armor.create_armor('Blue Dragonhide Tunic', 'A Blue Dragonhide Tunic', 6, 'body', 'range').to_dict(),
    'red_dhide': Armor.create_armor('Red Dragonhide Tunic', 'A Red Dragonhide Tunic', 7, 'body', 'range').to_dict(),
    'black_dhide': Armor.create_armor('Black Dragonhide Tunic', 'A Black Dragonhide Tunic', 8, 'body', 'range').to_dict(),
    'royal_dhide': Armor.create_armor('Royal Dragonhide Tunic', 'A Royal Dragonhide Tunic', 9, 'body', 'range').to_dict(),
    'elder_dhide': Armor.create_armor('Elder Dragonhide Tunic', 'An Elder Dragonhide Tunic', 10, 'body', 'range').to_dict(),
}
range_chaps = { # legs
    'leather': Armor.create_armor('Leather Chaps', 'A Pair of Leather Chaps', 1, 'legs', 'range').to_dict(),
    'hardened': Armor.create_armor('Hardened Leather Chaps', 'A Pair of Hardened Leather Chaps', 2, 'legs', 'range').to_dict(),
    'studded': Armor.create_armor('Studded Chaps', 'A Pair of Studded Chaps', 3, 'legs', 'range').to_dict(),
    'snakeskin': Armor.create_armor('Snakeskin Chaps', 'A Pair of Snakeskin Chaps', 4, 'legs', 'range').to_dict(),
    'green_dhide': Armor.create_armor('Green Dragonhide Chaps', 'A Pair of Green Dragonhide Chaps', 5, 'legs', 'range').to_dict(),
    'blue_dhide': Armor.create_armor('Blue Dragonhide Chaps', 'A Pair of Blue Dragonhide Chaps', 6, 'legs', 'range').to_dict(),
    'red_dhide': Armor.create_armor('Red Dragonhide Chaps', 'A Pair of Red Dragonhide Chaps', 7, 'legs', 'range').to_dict(),
    'black_dhide': Armor.create_armor('Black Dragonhide Chaps', 'A Pair of Black Dragonhide Chaps', 8, 'legs', 'range').to_dict(),
    'royal_dhide': Armor.create_armor('Royal Dragonhide Chaps', 'A Pair of Royal Dragonhide Chaps', 9, 'legs', 'range').to_dict(),
    'elder_dhide': Armor.create_armor('Elder Dragonhide Chaps', 'A Pair of Elder Dragonhide Chaps', 10, 'legs', 'range').to_dict(),
}
range_vambraces = { # hands
    'leather': Armor.create_armor('Leather Vambraces', 'A Pair of Leather Vambraces', 1, 'hands', 'range').to_dict(),
    'hardened': Armor.create_armor('Hardened Leather Vambraces', 'A Pair of Hardened Leather Vambraces', 2, 'hands', 'range').to_dict(),
    'studded': Armor.create_armor('Studded Vambraces', 'A Pair of Studded Vambraces', 3, 'hands', 'range').to_dict(),
    'snakeskin': Armor.create_armor('Snakeskin Vambraces', 'A Pair of Snakeskin Vambraces', 4, 'hands', 'range').to_dict(),
    'green_dhide': Armor.create_armor('Green Dragonhide Vambraces', 'A Pair of Green Dragonhide Vambraces', 5, 'hands', 'range').to_dict(),
    'blue_dhide': Armor.create_armor('Blue Dragonhide Vambraces', 'A Pair of Blue Dragonhide Vambraces', 6, 'hands', 'range').to_dict(),
    'red_dhide': Armor.create_armor('Red Dragonhide Vambraces', 'A Pair of Red Dragonhide Vambraces', 7, 'hands', 'range').to_dict(),
    'black_dhide': Armor.create_armor('Black Dragonhide Vambraces', 'A Pair of Black Dragonhide Vambraces', 8, 'hands', 'range').to_dict(),
    'royal_dhide': Armor.create_armor('Royal Dragonhide Vambraces', 'A Pair of Royal Dragonhide Vambraces', 9, 'hands', 'range').to_dict(),
    'elder_dhide': Armor.create_armor('Elder Dragonhide Vambraces', 'A Pair of Elder Dragonhide Vambraces', 10, 'hands', 'range').to_dict(),
}
range_boots = { # feet
    'leather': Armor.create_armor('Leather Boots', 'A Pair of Leather Boots', 1, 'feet', 'range').to_dict(),
    'hardened': Armor.create_armor('Hardened Leather Boots', 'A Pair of Hardened Leather Boots', 2, 'feet', 'range').to_dict(),
    'studded': Armor.create_armor('Studded Boots', 'A Pair of Studded Boots', 3, 'feet', 'range').to_dict(),
    'snakeskin': Armor.create_armor('Snakeskin Boots', 'A Pair of Snakeskin Boots', 4, 'feet', 'range').to_dict(),
    'green_dhide': Armor.create_armor('Green Dragonhide Boots', 'A Pair of Green Dragonhide Boots', 5, 'feet', 'range').to_dict(),
    'blue_dhide': Armor.create_armor('Blue Dragonhide Boots', 'A Pair of Blue Dragonhide Boots', 6, 'feet', 'range').to_dict(),
    'red_dhide': Armor.create_armor('Red Dragonhide Boots', 'A Pair of Red Dragonhide Boots', 7, 'feet', 'range').to_dict(),
    'black_dhide': Armor.create_armor('Black Dragonhide Boots', 'A Pair of Black Dragonhide Boots', 8, 'feet', 'range').to_dict(),
    'royal_dhide': Armor.create_armor('Royal Dragonhide Boots', 'A Pair of Royal Dragonhide Boots', 9, 'feet', 'range').to_dict(),
    'elder_dhide': Armor.create_armor('Elder Dragonhide Boots', 'A Pair of Elder Dragonhide Boots', 10, 'feet', 'range').to_dict(),
}
bows = { # right_hand
    'short_bow': Weapon.create_weapon('Short Bow', 'A Short Bow', 2, 'right_hand', 'range').to_dict(),
    'long_bow': Weapon.create_weapon('Long Bow', 'A Long Bow', 3, 'right_hand', 'range').to_dict(),
    'oak_short': Weapon.create_weapon('Oak Short Bow', 'An Oak Short Bow', 2, 'right_hand', 'range').to_dict(),
    'oak_long': Weapon.create_weapon('Oak Long Bow', 'An Oak Long Bow', 3, 'right_hand', 'range').to_dict(),
    'willow_short': Weapon.create_weapon('Willow Short Bow', 'A Willow Short Bow', 2, 'right_hand', 'range').to_dict(),
    'willow_long': Weapon.create_weapon('Willow Long Bow', 'A Willow Long Bow', 3, 'right_hand', 'range').to_dict(),
    'maple_short': Weapon.create_weapon('Maple Short Bow', 'A Maple Short Bow', 2, 'right_hand', 'range').to_dict(),
    'maple_long': Weapon.create_weapon('Maple Long Bow', 'A Maple Long Bow', 3, 'right_hand', 'range').to_dict(),
    'yew_short': Weapon.create_weapon('Yew Short Bow', 'A Yew Short Bow', 2, 'right_hand', 'range').to_dict(),
    'yew_long': Weapon.create_weapon('Yew Long Bow', 'A Yew Long Bow', 3, 'right_hand', 'range').to_dict(),
    'magic_short': Weapon.create_weapon('Magic Short Bow', 'A Magic Short Bow', 2, 'right_hand', 'range').to_dict(),
    'magic_long': Weapon.create_weapon('Magic Long Bow', 'A Magic Long Bow', 3, 'right_hand', 'range').to_dict(),
    'redwood_short': Weapon.create_weapon('Redwood Short Bow', 'A Redwood Short Bow', 2, 'right_hand', 'range').to_dict(),
    'redwood_long': Weapon.create_weapon('Redwood Long Bow', 'A Redwood Long Bow', 3, 'right_hand', 'range').to_dict(),
    'elder_short': Weapon.create_weapon('Elder Short Bow', 'An Elder Short Bow', 2, 'right_hand', 'range').to_dict(),
    'elder_long': Weapon.create_weapon('Elder Long Bow', 'An Elder Long Bow', 3, 'right_hand', 'range').to_dict(),
    'crystal_short': Weapon.create_weapon('Crystal Short Bow', 'A Crystal Short Bow', 2, 'right_hand', 'range').to_dict(),
    'crystal_long': Weapon.create_weapon('Crystal Long Bow', 'A Crystal Long Bow', 3, 'right_hand', 'range').to_dict(),
    'dragon_short': Weapon.create_weapon('Dragon Short Bow', 'A Dragon Short Bow', 2, 'right_hand', 'range').to_dict(),
    'dragon_long': Weapon.create_weapon('Dragon Long Bow', 'A Dragon Long Bow', 3, 'right_hand', 'range').to_dict(),
}


range_items = {
    'head': range_coif,
    'body': range_tunic,
    'legs': range_chaps,
    'hands': range_vambraces,
    'feet': range_boots,
    'right_hand': bows,
}


items = {
    'melee_items': melee_items,
    'magic_items': magic_items,
    'range_items': range_items,
    'resources': resources,
}
