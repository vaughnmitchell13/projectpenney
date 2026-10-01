# projectpenney
Uses the Monte Carlo method to simulate and visualize two versions of the Humble-Nishiyama (H-N) Randomness game, which is a variation of the Penney's Game using a standard 52-deck of cards.

## Context: Penney's Game
The Penney's Game was created by Walter Penney, and it consists of two players who choose a sequence of heads/tails of 3 coins or longer. Coins are tossed until the first or second player's sequence appears in the flipped outcomes, and the player whose sequence appears first wins the game. At first glance, the game appears to be fair, but the second player can optimize their strategy with another sequence that has a higher probability of occurring first based on the sequence chosen by the first player. This strategy is also applicable to two variations of the game we simulated in this repo, and it will be discussed in [Strategy and Purpose](#strategy-and-purpose).

## This repo: Humble-Nishiyama (H-N) Randomness Game
The H-N Randomness Game is a variation of the Penney's Game and can be played with a standard 52-deck of cards. Each player chooses a sequence of red and black cards, and the cards are turned over and placed in the order they're dealt until one of the chosen sequences occurs. Whichever players' sequence occurs first wins a "trick" and they take all the upturned cards. At the end of the game, the player with the most tricks won has won the game. The game is described as non-transitive. This means that if Player A beats Player B and Player B beats Player C, but Player A does not beat Player C, then the relation that transitivity requires is broken. 

## This repo: Ron's Version
Ron's version uses the exact same rules as the H-N Randomness Game with one caveat. When a game is finished, the score is compared by the total cards accumulated from winning tricks. The player with the most cards on hand has won the game.

## Strategy and Purpose
The purpose of this Monte Carlo simulation is to understand how simulated probabilities can partially verify the optimal strategy for the H-N Randomness Game. As mentioned, the second player can always optimize their sequence based on the sequence of the first player. Consider this table from [Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game):
|1st player's choice| 2nd player's choice | Probability 1st player wins | Probability 2nd player wins | Probability of a draw |
|-------------------|---------------------|-----------------------------|-----------------------------|-----------------------|
|BBB|RBB|0.11%|99.49%|0.40%|
|BBR|RBB|2.62%|93.54%|3.84%|
|BRB|BBR|11.61%|80.11%|8.28%|
|BRR|BBR|5.18%|88.29%|6.53%|
|RBB|RRB|5.18%|88.29%|6.53%|
|RBR|RRB|11.61%|80.11%|8.28%|
|RRB|BRR|2.62%|93.54%|3.84%|
|RRR|BRR|0.11%|99.49%|0.40%|

\
The strategy for Player B is summarized like this: "take the opposite of Player A's second card, and tag on Player A's two cards as-is to your sequence."

## Findings
In our heatmaps, we found that for tiles where the theorized strategy applies, the second player had the highest probability of winning by both tricks and scores. For instance, when the opponent selected 'RRR' and we selected 'BRR', the simulation carried a 99% chance of victory by tricks and a 100% chance of victory by cards (percents were rounded). Similarly, when an opponent chose 'BBB' and we chose 'RBB', the simulation also carried a 99% chance of victory by tricks and an 100% chance of victory by cards. We believe the strategy works because if Player A's second card does not hit, then Player B's first card will if they choose the optimal strategy [above](#strategy-and-purpose). Player B can basically "steal" Player A's sequence. 

What we found interesting was that for matchups where a player chooses the same color for their whole sequence ('RRR' vs. 'BBB'), the tie rate for games scored by cards was 3% while the tie rate for games scored by tricks was 35%. We are not sure why this is, but scoring by cards might be more sensitive to determine a winner after an entire deck is dealt. In other words, a player can win one trick and accumulate tons of cards.

If you look at the simulated matchup win probabilities in the table above and cross-reference with the tiles in our heatmap, you'll find that the numbers are almost one-to-one. Even though the baseline simulation uses 1,000,000 decks, you can try the simulation with even more decks and create a heatmap of the results for yourself. 

## Repository Guidance
- `src/datagen.py`: Handles data generation and storage
- `src/dataproc.py`: Does processing, scoring, and tabulation of results
- `src/datavis.py`: Creates heatmaps from simulated data
- `data/processed`: Contains 1,000,000 sims of scoring by cards and tricks
- `main.py`: The entry point to the project (visualize the heatmap from the simulation, or add a new batch of decks with your own seed)
- `figures`: Contains heatmaps from the simulation

## Try it yourself
1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone the repository to your system:
```
git clone https://github.com/vaughnmitchell13/projectpenney.git
```
3. From the project root, run:
```
uv sync
```
4. To start the program, run:
```
uv run main.py
```


