# The Forgotten Mansion - Complete Walkthrough

This guide provides a complete solution to the game, including all puzzles and the location of the treasure.

**SPOILER WARNING**: This document reveals all solutions and secrets!

---

## Quick Solution (Speedrun)

If you just want to win quickly:

1. `take journal` (optional, for story)
2. `north` (to hallway)
3. `west` (to kitchen)
4. `take knife` (optional)
5. `east`, `north` (to garden)
6. `take stone`
7. `north` (to forest path)
8. `north` (to mansion gate)
9. `use stone on padlock`
10. `north` (into mansion)
11. `west` (to library)
12. `search desk`
13. `take silver key`
14. `east`, `up` (to upstairs hallway)
15. `use silver key on door`
16. `east` (to study)
17. `search desk` (get combination)
18. `north` (to master bedroom)
19. `search wardrobe`
20. `take brass key`
21. `south`, `east` (back to study)
22. `use brass key on safe` (automatically uses combination)
23. `take golden amulet`
24. **YOU WIN!**

---

## Detailed Walkthrough with Exploration

### Part 1: Your House

**Starting Room (Bedroom)**
```
> look
```
You'll see your bedroom. Notice the journal on the bedside table.

```
> take journal
> read journal
```
The journal provides story context about the mansion and hints that "the key to everything is in the study."

```
> examine bed
> search bed
```
Nothing useful under the bed, but you can interact with it.

```
> north
```

**Hallway**
```
> look
```
You're in the hallway. Exits lead to multiple rooms.

```
> examine painting
```
It's a painting of the mansion.

**Kitchen (west from hallway)**
```
> west
> look
```

You'll see a knife and bread.

```
> take knife
> take bread
```

The knife might be useful (though the stone is better for the puzzle). The bread can be eaten.

```
> eat bread
```

Optional: Explore the cabinet
```
> search cabinet
```

**Living Room (east from hallway)**
```
> east (from hallway)
> look
```

Important item here:
```
> take flashlight
```

The flashlight isn't required for the main puzzle path, but it's a useful item.

```
> search bookshelf
> search sofa
```

Explore the various objects in the room.

### Part 2: Outside to the Mansion

**Garden**
```
> north (from hallway)
> look
```

**CRITICAL ITEM:**
```
> take stone
```

The stone is essential for breaking the padlock at the mansion gate!

```
> smell flowers
```

Explore the environment.

**Forest Path**
```
> north
> look
```

Optional item:
```
> take mushrooms
```

The mushrooms are an interesting item but not required for winning.

**Mansion Gate - The First Puzzle**
```
> north
> look
```

You'll see the gate is locked with a padlock.

```
> examine gate
> examine padlock
```

**SOLUTION:**
```
> use stone on padlock
```

This breaks the padlock and unlocks the gate!

### Part 3: Inside the Mansion

**Mansion Entrance Hall**
```
> north (through the now-open gate)
> look
```

You're in the grand entrance hall. Multiple exits available.

```
> examine chandelier
> search rug
```

Explore the area.

**Library - Finding the Silver Key**
```
> west
> look
```

**CRITICAL PUZZLE:**
```
> search desk
```

This reveals a silver key!

```
> take silver key
```

The silver key unlocks the study door upstairs.

Optional:
```
> take ancient tome
> read ancient tome
```

**Dining Room & Kitchen** (Optional Exploration)
```
> east (from entrance), then east
```

Explore the dining room:
```
> search table
> take silverware
```

Continue to the mansion kitchen and pantry:
```
> north, then east
> take jar
```

These areas don't contain critical items but add to the world.

### Part 4: Upstairs - The Study Puzzle

**Upstairs Hallway**
```
> (from entrance hall) up
> look
```

Notice the study door to the east is locked.

**Master Bedroom - Finding the Brass Key**
```
> north
> look
```

**CRITICAL PUZZLE:**
```
> search wardrobe
```

This reveals a brass key hidden in a coat pocket!

```
> take brass key
```

This key is needed for the safe in the study.

Optional exploration:
```
> examine mirror
> search bed
```

**The Study - Final Puzzle**

First, unlock the door:
```
> south (back to hallway)
> use silver key on door
```

or just:
```
> south
> use silver key
```

The door unlocks!

```
> east
> look
```

You'll see the safe built into the wall.

**Get the combination:**
```
> search desk
```

This reveals a note: "The combination is the year this mansion was built: 1847"

Now you have both the key and the combination!

**Open the safe:**
```
> use brass key on safe
```

The game automatically uses the combination you found. The safe opens!

**GET THE TREASURE:**
```
> take golden amulet
```

**CONGRATULATIONS! YOU WIN!**

---

## Complete Item List

### Takeable Items by Location

**Bedroom:**
- journal

**Kitchen:**
- knife
- bread

**Living Room:**
- flashlight

**Garden:**
- stone ⭐ (required for gate)

**Forest Path:**
- mushrooms

**Library:**
- ancient tome
- silver key ⭐ (required for study - appears after searching desk)

**Dining Room:**
- silverware

**Pantry:**
- jar

**Master Bedroom:**
- brass key ⭐ (required for safe - appears after searching wardrobe)

**Study (after opening safe):**
- golden amulet 🏆 (THE TREASURE - winning item!)

⭐ = Required for winning
🏆 = Winning item

---

## Puzzle Solutions Summary

### Puzzle 1: Getting Into the Mansion
**Problem:** Gate is locked with a padlock
**Solution:** Use stone on padlock (breaks it open)
**Required Item:** Stone (from garden)

### Puzzle 2: Getting Into the Study
**Problem:** Study door is locked
**Solution:** Use silver key on door
**Required Item:** Silver key (hidden in library desk - must search)

### Puzzle 3: Opening the Safe
**Problem:** Safe requires both a key and a combination
**Solution:**
1. Get combination by searching study desk (1847)
2. Use brass key on safe
**Required Items:**
- Brass key (hidden in master bedroom wardrobe - must search)
- Combination (from searching study desk)

---

## Alternative Approaches

### Can you use the knife instead of the stone?
No! If you try:
```
> use knife on padlock
```
The game responds: "The knife isn't strong enough to cut through the padlock."

This demonstrates the rule-based nature - you can't just use any sharp object.

### Can you break down the gate?
No. You can try:
```
> push gate
> pull gate
```
But only the stone-on-padlock solution works.

### Can you pick the locks?
No. The game doesn't have a lockpicking mechanic. You need the actual keys.

---

## Easter Eggs & Optional Content

### Readable Items
- Journal (your bedroom) - Provides story context
- Ancient tome (library) - References hidden chambers in Latin

### Interactive Objects (not critical to winning)
- Bed - Can examine and search
- Curtains - Can open and close
- Cabinet - Can search
- Sofa - Can search (find coins and lint)
- Bookshelf - Can search and read
- Various furniture pieces throughout

### Sensory Commands
Try these in different locations:
- `listen` - Different responses per room
- `smell` - Different responses per room
- `smell flowers` (in garden) - Special response

### Food Items
- Bread - Can be eaten
- Mushrooms - Can be examined, but game warns against eating them

---

## Scoring

The game tracks your score based on:
- Finding important items (points per item)
- Opening the safe (+50 bonus points)
- Getting the golden amulet (+100 points)

Your final score is shown when you win!

---

## Common Mistakes

1. **Not searching the desk in the library** - You'll miss the silver key!
2. **Not searching the wardrobe** - You'll miss the brass key!
3. **Trying to open the safe before searching the study desk** - You need the combination!
4. **Forgetting to take the stone** - It's the only way to open the gate!

---

## Speed Tips

- You can abbreviate directions: `n` instead of `north`
- You can chain movements mentally but must enter one at a time
- The minimal required inventory is: stone, silver key, brass key
- Everything else is optional!

---

Happy adventuring! 🏚️✨
