## Goal
The assignment is to make a small console-based Pokemon Game. The goal of the game is to
allow a player to select a Pokemon from a range of choices and to initiate a fighting sequence with
another Pokemon. The fighting happens turn-based. Each Pokemon gets a turn to attack, until one
Pokemon’s health is depleted. The complexity of the game mechanics is secondary, our main
interest is what you have built under the hood.

## Requirements
1. Main menu so the user can initiate actions.
2. List all available Pokemon and be able to choose one as your main Pokemon. Create as
many Pokemon as you like, with a minimum of 5.
3. Being able to change your main Pokemon at any time.
4. Ability to initiate a fighting sequence. Before actually fighting, we pick an opposing
Pokemon.
5. An overview of what happens during the fight. Who is attacking who, what are the current
health stats, etc.

## Feature list
- 1.1 Main menu screen
- 1.2 Actions: Pick pokemon, start fight
- 2.1 Display all available pokemon
- 2.2 Select main pokemon
- 3.1 Swap main pokemon
- 3.2 Swap pokemon for current fight only
- 4.1 Initiate fight
- 4.2 Pick opponent
- 4.3 Determine order
- 5.1 Fight screen
- 5.2 Pick battle action: Fight, Swap pokemon, (Optional) Special, Defend
- 5.3 Process battle results
- 5.4 Declare & display victory

##Todo
- [x] Setup main template (1.1, 2.1, 5.1, 5.4)
- [x] Create menu buttons (1.1, 1.2)
- [x] Setup DB (SQLite?) (2.1)
- [x] Add pokemon to DB (2.1)
- [x] Load pokemon from DB (2.1, 2.2, 3.1, 3.2, 4.2)
- [x] Pick pokemon template (2.2, 3.1, 3.2)
- [x] Fight layout (5.1)
- [x] Fight status report (5.1)
- [x] Fight actions (5.1)
- [x] Game engine: Session storage (2.2, 3.1, 3.2, 4.1, 4.2, 5.2)
- [x] Game engine: Fight mechanics (4.1, 5.2, 5.3, 5.4)
- [x] Battle results template (5.4)
- [ ] \(Optional) Battle music! (5.1)
- [ ] \(Optional) Battle statistics (5.3, 5.4)
- [ ] \(Optional) Element mechanics (5.3)
- [ ] \(Optional) Different attacks (5.3)
- [ ] \(Future feature) Opponent AI 
