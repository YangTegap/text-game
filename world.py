"""
World definition - all rooms, objects, NPCs, and their properties.
This is where the game content lives!
"""


def get_world_data():
    """
    Returns the complete world definition.

    Structure:
    - rooms: dict of room_id -> room data
    - start_room: where the player begins

    Each room has:
    - name: display name
    - description: what the player sees
    - exits: dict of direction -> destination room_id (or dict with locked/hidden info)
    - objects: list of interactive objects

    Each object has:
    - name: primary name
    - aliases: list of alternative names
    - description: what you see when examining it
    - takeable: can it be picked up?
    - visible: is it visible in room description?
    - interactions: dict of action -> response
    - room_description: how it appears in the room
    """

    return {
        'start_room': 'bedroom',
        'rooms': {
            # ===== STARTING AREA: THE HOUSE =====
            'bedroom': {
                'name': 'Your Bedroom',
                'description': 'You wake up in your small but cozy bedroom. Morning light filters through faded curtains. Your bed is unmade, and your belongings are scattered about. A wooden door leads north to the hallway.',
                'exits': {
                    'north': 'hallway'
                },
                'objects': [
                    {
                        'name': 'bed',
                        'aliases': ['beds', 'cot', 'mattress'],
                        'description': 'A simple wooden bed with rumpled sheets. Nothing interesting underneath.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You search under the bed and find nothing but dust.',
                            'use': 'You\'re not tired right now.',
                        }
                    },
                    {
                        'name': 'journal',
                        'aliases': ['diary', 'notebook', 'book'],
                        'description': 'A leather-bound journal. The last entry reads: "The old mansion holds secrets. The key to everything is in the study. But first, I must find a way in."',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'Your journal lies on the bedside table.',
                        'interactions': {
                            'read': 'The last entry reads: "The old mansion holds secrets. The key to everything is in the study. But first, I must find a way in."',
                        }
                    },
                    {
                        'name': 'curtains',
                        'aliases': ['curtain', 'drapes', 'window'],
                        'description': 'Faded blue curtains covering a small window. Through them you can see the garden outside.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'open': 'You pull the curtains open. Sunlight floods the room.',
                            'close': 'You draw the curtains closed.',
                        }
                    }
                ]
            },

            'hallway': {
                'name': 'Hallway',
                'description': 'A narrow hallway with worn wooden floorboards that creak underfoot. Doors lead south back to your bedroom, west to the kitchen, and east to the living room. The front door to the north leads outside.',
                'exits': {
                    'north': 'garden',
                    'south': 'bedroom',
                    'west': 'kitchen',
                    'east': 'living_room'
                },
                'objects': [
                    {
                        'name': 'painting',
                        'aliases': ['picture', 'portrait', 'frame'],
                        'description': 'An old painting of the mansion that stands in the forest. It looks foreboding even in the painting.',
                        'takeable': False,
                        'visible': True,
                        'room_description': 'A dusty painting hangs crooked on the wall.',
                        'interactions': {
                            'take': 'It\'s firmly attached to the wall.',
                        }
                    }
                ]
            },

            'kitchen': {
                'name': 'Kitchen',
                'description': 'A small, cluttered kitchen. Dishes are piled in the sink, and the air smells faintly of stale coffee. A window looks out onto the garden. The hallway is to the east.',
                'exits': {
                    'east': 'hallway'
                },
                'objects': [
                    {
                        'name': 'knife',
                        'aliases': ['kitchen knife', 'blade'],
                        'description': 'A sharp kitchen knife. It might be useful for cutting things.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A kitchen knife sits on the counter.',
                        'interactions': {}
                    },
                    {
                        'name': 'bread',
                        'aliases': ['loaf', 'food'],
                        'description': 'A half-eaten loaf of bread. Still edible.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A loaf of bread sits on the cutting board.',
                        'interactions': {
                            'eat': 'You eat some bread. It\'s stale but filling.',
                        }
                    },
                    {
                        'name': 'cabinet',
                        'aliases': ['cupboard', 'cabinets'],
                        'description': 'A wooden cabinet with several drawers and doors.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'open': 'You open the cabinet. Just some old dishes inside.',
                            'search': 'You search the cabinet thoroughly but find nothing useful.',
                        }
                    }
                ]
            },

            'living_room': {
                'name': 'Living Room',
                'description': 'A cozy living room with an old sofa and a fireplace. Bookshelves line one wall. The room has a musty smell of old paper and wood smoke. The hallway is to the west.',
                'exits': {
                    'west': 'hallway'
                },
                'objects': [
                    {
                        'name': 'sofa',
                        'aliases': ['couch', 'seat'],
                        'description': 'A worn but comfortable-looking sofa with faded upholstery.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You search between the cushions and find some old coins and lint.',
                        }
                    },
                    {
                        'name': 'bookshelf',
                        'aliases': ['shelf', 'bookshelves', 'books'],
                        'description': 'Shelves packed with old books on various subjects. Most look untouched for years.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You browse the books. Mostly classics and reference books. One title catches your eye: "Legends of the Forest Mansion."',
                            'read': 'You browse the books. Mostly classics and reference books.',
                        }
                    },
                    {
                        'name': 'flashlight',
                        'aliases': ['torch', 'light', 'lamp'],
                        'description': 'A sturdy flashlight. The batteries still work.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A flashlight rests on the mantle above the fireplace.',
                        'interactions': {
                            'use': 'You turn on the flashlight. It casts a bright beam.',
                        }
                    }
                ]
            },

            # ===== OUTSIDE AREA =====
            'garden': {
                'name': 'Front Garden',
                'description': 'You stand in an overgrown garden. Wildflowers and weeds compete for space among forgotten flowerbeds. A gravel path leads north toward the forest. Your house is to the south.',
                'exits': {
                    'south': 'hallway',
                    'north': 'forest_path'
                },
                'objects': [
                    {
                        'name': 'flowers',
                        'aliases': ['flower', 'wildflowers', 'roses'],
                        'description': 'Wild roses growing among the weeds. They smell lovely.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'smell': 'The roses smell wonderful.',
                        }
                    },
                    {
                        'name': 'stone',
                        'aliases': ['rock', 'stones', 'rocks'],
                        'description': 'A smooth, heavy stone from the garden path.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'Several decorative stones line the garden path.',
                        'interactions': {}
                    }
                ]
            },

            'forest_path': {
                'name': 'Forest Path',
                'description': 'A winding dirt path through dense forest. Trees tower overhead, their branches forming a canopy that blocks most of the sunlight. The path continues north deeper into the woods, or south back to the garden.',
                'exits': {
                    'south': 'garden',
                    'north': 'mansion_gate'
                },
                'objects': [
                    {
                        'name': 'trees',
                        'aliases': ['tree', 'forest', 'woods'],
                        'description': 'Tall oak and pine trees. The forest is thick here.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {}
                    },
                    {
                        'name': 'mushrooms',
                        'aliases': ['mushroom', 'fungi'],
                        'description': 'Strange glowing mushrooms growing at the base of a tree. They pulse with a faint blue light.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'Strange glowing mushrooms grow at the base of a nearby tree.',
                        'interactions': {
                            'eat': 'You\'re not sure if these are safe to eat. Best not to risk it.',
                        }
                    }
                ]
            },

            # ===== THE MANSION =====
            'mansion_gate': {
                'name': 'Mansion Gate',
                'description': 'You stand before a towering iron gate. Beyond it, a decrepit mansion looms against the darkening sky. The gate is locked with a heavy chain and padlock. The forest path leads south.',
                'exits': {
                    'south': 'forest_path',
                    'north': {
                        'destination': 'mansion_entrance',
                        'locked': True,
                        'locked_message': 'The gate is locked with a heavy padlock. You need to find a way to open it.'
                    }
                },
                'objects': [
                    {
                        'name': 'gate',
                        'aliases': ['iron gate', 'gates'],
                        'description': 'A tall iron gate with ornate, rusted bars. It\'s locked with a heavy chain and padlock.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'open': 'The gate is locked with a padlock.',
                        }
                    },
                    {
                        'name': 'padlock',
                        'aliases': ['lock', 'chain'],
                        'description': 'A rusty but sturdy padlock securing the gate. It looks old but functional.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {}
                    }
                ]
            },

            'mansion_entrance': {
                'name': 'Mansion Entrance Hall',
                'description': 'A grand entrance hall, now fallen into decay. A magnificent staircase curves upward to the second floor. Dust motes dance in the dim light filtering through grimy windows. Doorways lead east and west, and the front door is south.',
                'exits': {
                    'south': 'mansion_gate',
                    'east': 'dining_room',
                    'west': 'library',
                    'up': 'upstairs_hallway'
                },
                'objects': [
                    {
                        'name': 'chandelier',
                        'aliases': ['light', 'lights'],
                        'description': 'A massive crystal chandelier hangs precariously from the ceiling, covered in cobwebs.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {}
                    },
                    {
                        'name': 'rug',
                        'aliases': ['carpet', 'mat'],
                        'description': 'An ornate Persian rug, faded and worn.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You lift the edge of the rug. Nothing but dust underneath.',
                        }
                    }
                ]
            },

            'library': {
                'name': 'Library',
                'description': 'Floor-to-ceiling bookshelves dominate this room, filled with ancient tomes. A reading desk sits by the window. The air is thick with the smell of old leather and paper. The entrance hall is to the east.',
                'exits': {
                    'east': 'mansion_entrance'
                },
                'objects': [
                    {
                        'name': 'desk',
                        'aliases': ['table', 'reading desk'],
                        'description': 'An old wooden desk with several drawers.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You search the desk drawers. In one, you find a small silver key!',
                        }
                    },
                    {
                        'name': 'ancient tome',
                        'aliases': ['tome', 'book', 'ancient book'],
                        'description': 'A massive leather-bound book. The title is in Latin: "De Mysteriis Arcanum"',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A particularly large ancient tome sits on the desk.',
                        'interactions': {
                            'read': 'The text is in Latin. You can make out references to "hidden chambers" and "eternal treasures."',
                        }
                    }
                ]
            },

            'dining_room': {
                'name': 'Dining Room',
                'description': 'A long dining table stretches down the center of the room, set for a feast that never happened. Plates are covered in dust, and cobwebs drape the chairs. The entrance hall is to the west, and a door leads north to the kitchen.',
                'exits': {
                    'west': 'mansion_entrance',
                    'north': 'mansion_kitchen'
                },
                'objects': [
                    {
                        'name': 'table',
                        'aliases': ['dining table'],
                        'description': 'A long mahogany table, still set with dusty china and silverware.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You examine the table settings. All that remains is dust and decay.',
                        }
                    },
                    {
                        'name': 'silverware',
                        'aliases': ['silver', 'utensils', 'fork', 'spoon'],
                        'description': 'Tarnished silver utensils. They might be valuable if cleaned.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'Tarnished silverware sits on the table.',
                        'interactions': {}
                    }
                ]
            },

            'mansion_kitchen': {
                'name': 'Mansion Kitchen',
                'description': 'A large but deteriorated kitchen. An old iron stove sits cold and dark. Pots and pans hang from hooks, and a pantry door stands ajar to the east. The dining room is south.',
                'exits': {
                    'south': 'dining_room',
                    'east': 'pantry'
                },
                'objects': [
                    {
                        'name': 'stove',
                        'aliases': ['oven', 'iron stove'],
                        'description': 'A massive iron stove, cold and covered in rust.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You open the stove. Inside are just ashes.',
                        }
                    }
                ]
            },

            'pantry': {
                'name': 'Pantry',
                'description': 'A small pantry with empty shelves. Whatever food was stored here long ago is gone. The kitchen is to the west.',
                'exits': {
                    'west': 'mansion_kitchen'
                },
                'objects': [
                    {
                        'name': 'jar',
                        'aliases': ['glass jar', 'container'],
                        'description': 'An empty glass jar, surprisingly intact.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'An old glass jar sits on a shelf.',
                        'interactions': {}
                    }
                ]
            },

            # ===== UPSTAIRS =====
            'upstairs_hallway': {
                'name': 'Upstairs Hallway',
                'description': 'A long hallway with several doors. Portraits of stern-looking people line the walls, their eyes seeming to follow you. Stairs lead down to the entrance hall. Doors lead north to the master bedroom and east to the study.',
                'exits': {
                    'down': 'mansion_entrance',
                    'north': 'master_bedroom',
                    'east': {
                        'destination': 'study',
                        'locked': True,
                        'locked_message': 'The study door is locked. You need a key.'
                    }
                },
                'objects': [
                    {
                        'name': 'portraits',
                        'aliases': ['portrait', 'painting', 'pictures'],
                        'description': 'Oil paintings of the mansion\'s former residents. They all look rather grim.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {}
                    }
                ]
            },

            'master_bedroom': {
                'name': 'Master Bedroom',
                'description': 'A large bedroom with a four-poster bed draped in rotting curtains. A wardrobe stands against one wall, and a dresser sits beneath a cracked mirror. The hallway is to the south.',
                'exits': {
                    'south': 'upstairs_hallway'
                },
                'objects': [
                    {
                        'name': 'wardrobe',
                        'aliases': ['closet', 'cabinet'],
                        'description': 'A large oak wardrobe. The doors are slightly ajar.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'open': 'You open the wardrobe. Old moth-eaten clothes hang inside.',
                            'search': 'You search through the clothes and find a small brass key hidden in a coat pocket!',
                        }
                    },
                    {
                        'name': 'mirror',
                        'aliases': ['looking glass', 'glass'],
                        'description': 'A large mirror with a crack running through it. Your reflection looks distorted.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {}
                    },
                    {
                        'name': 'four-poster bed',
                        'aliases': ['bed', 'four poster bed'],
                        'description': 'A grand bed with decaying curtains. It must have been magnificent once.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You check under the bed. Nothing but dust and cobwebs.',
                        }
                    }
                ]
            },

            'study': {
                'name': 'Study',
                'description': 'A private study lined with bookshelves and filing cabinets. A large desk dominates the center of the room, and a safe is built into the wall behind it. This is clearly where the mansion\'s master conducted important business. The hallway is to the west.',
                'exits': {
                    'west': 'upstairs_hallway'
                },
                'objects': [
                    {
                        'name': 'safe',
                        'aliases': ['vault', 'strongbox'],
                        'description': 'A heavy iron safe built into the wall. It has a combination lock.',
                        'takeable': False,
                        'visible': True,
                        'room_description': 'A large safe is built into the wall behind the desk.',
                        'interactions': {
                            'open': 'The safe is locked. It requires a combination.',
                        }
                    },
                    {
                        'name': 'study desk',
                        'aliases': ['desk'],
                        'description': 'An imposing mahogany desk with many drawers.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You search the desk. In one drawer, you find a note: "The combination is the year this mansion was built: 1847"',
                        }
                    },
                    {
                        'name': 'filing cabinet',
                        'aliases': ['cabinet', 'files'],
                        'description': 'Metal filing cabinets filled with old documents and records.',
                        'takeable': False,
                        'visible': False,
                        'room_description': '',
                        'interactions': {
                            'search': 'You rifle through old papers. Mostly mundane business records.',
                        }
                    }
                ]
            }
        }
    }
