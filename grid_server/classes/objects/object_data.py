from grid_server.classes.objects.object import TileObj

# Objects
trees = {
    1: TileObj.create_object(1, 'Tree', 'A Tree', 1, 5, 'logs').__dict__,
    2: TileObj.create_object(1, 'Oak Tree', 'An Oak Tree', 2, 10, 'oak logs').__dict__,
    3: TileObj.create_object(1, 'Willow Tree', 'A Willow Tree', 3, 15, 'willow logs').__dict__,
    4: TileObj.create_object(1, 'Maple Tree', 'A Maple Tree', 4, 20, 'maple logs').__dict__,
    5: TileObj.create_object(1, 'Yew Tree', 'A Yew Tree', 5, 25, 'yew logs').__dict__,
    6: TileObj.create_object(1, 'Magic Tree', 'A Magic Tree', 6, 30, 'magic logs').__dict__,
    7: TileObj.create_object(1, 'Redwood Tree', 'A Redwood Tree', 7, 35, 'redwood logs').__dict__,
    8: TileObj.create_object(1, 'Elder Tree', 'An Elder Tree', 8, 40, 'elder logs').__dict__,
    9: TileObj.create_object(1, 'Crystal Tree', 'A Crystal Tree', 9, 45, 'crystal logs').__dict__,
    10: TileObj.create_object(1, 'Dragon Tree', 'A Dragon Tree', 10, 50, 'dragon logs').__dict__,
}

rocks = {
    1: TileObj.create_object(2, 'Rock', 'A Rock', 1, 10, 'stone').__dict__,
    2: TileObj.create_object(2, 'Tin Rock', 'Infused with Tin', 2, 15, 'tin ore').__dict__,
    3: TileObj.create_object(2, 'Copper Rock', 'Infused with Copper', 3, 20, 'copper ore').__dict__,
    4: TileObj.create_object(2, 'Iron Rock', 'Infused with Iron', 4, 25, 'iron ore').__dict__,
    5: TileObj.create_object(2, 'Coal Rock', 'Infused with Coal', 5, 30, 'coal').__dict__,
    6: TileObj.create_object(2, 'Gold Rock', 'Infused with Gold', 6, 35, 'gold ore').__dict__,
    7: TileObj.create_object(2, 'Mithril Rock', 'Infused with Mithril', 7, 40, 'mithril ore').__dict__,
    8: TileObj.create_object(2, 'Adamantite Rock', 'Infused with Adamantite', 8, 45, 'adamantite ore').__dict__,
    9: TileObj.create_object(2, 'Runite Rock', 'Infused with Runite', 9, 50, 'runite ore').__dict__,
    10: TileObj.create_object(2, 'Dragonite Rock', 'Infused with Dragonite', 10, 55, 'dragonite ore').__dict__,
}

waters = {
    1: TileObj.create_object(3, 'Water', 'Water', 1, 100, None).__dict__,
    2: TileObj.create_object(3, 'Water', 'Water', 2, 100, None).__dict__,
    3: TileObj.create_object(3, 'Water', 'Water', 3, 100, None).__dict__,
    4: TileObj.create_object(3, 'Water', 'Water', 4, 100, None).__dict__,
    5: TileObj.create_object(3, 'Water', 'Water', 5, 100, None).__dict__,
    6: TileObj.create_object(3, 'Water', 'Water', 6, 100, None).__dict__,
    7: TileObj.create_object(3, 'Water', 'Water', 7, 100, None).__dict__,
    8: TileObj.create_object(3, 'Water', 'Water', 8, 100, None).__dict__,
    9: TileObj.create_object(3, 'Water', 'Water', 9, 100, None).__dict__,
    10: TileObj.create_object(3, 'Water', 'Water', 10, 100, None).__dict__,
} 

walls = {
    1: TileObj.create_object(4, 'Wall', 'A Wall', 1, 100, None).__dict__,
    2: TileObj.create_object(4, 'Wall', 'A Wall', 2, 100, None).__dict__,
    3: TileObj.create_object(4, 'Wall', 'A Wall', 3, 100, None).__dict__,
    4: TileObj.create_object(4, 'Wall', 'A Wall', 4, 100, None).__dict__,
    5: TileObj.create_object(4, 'Wall', 'A Wall', 5, 100, None).__dict__,
    6: TileObj.create_object(4, 'Wall', 'A Wall', 6, 100, None).__dict__,
    7: TileObj.create_object(4, 'Wall', 'A Wall', 7, 100, None).__dict__,
    8: TileObj.create_object(4, 'Wall', 'A Wall', 8, 100, None).__dict__,
}

objects = {
    1: trees,
    2: rocks,
    3: waters,
    4: walls,
}
