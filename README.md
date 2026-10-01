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

## Analysis of Optimal Strategies
Though there are eight sequences available, the player effectively only has four choices. BBB and RRR are functionally identical, since there are an equal number of each color in the deck. The same is true for BBR and RRB, BRB and RBR, and BRR and RBB. We will therefore describe strategies using X and O, which represent opposite colors, but could individually represent either.
Player 2 is always at an advantage, since there is a counter for any strategy Player 1 chooses that results in a Player 2 win in the vast majority of games. Here is what our heatmaps show:

Player 1: XXX | Player 2: OXX is optimal (effectively wins 100% of the time in both formats)
Player 1: XXO | Player 2: OXX is optimal (wins 94% of the time, ties 4% of the time by tricks; wins 100% of the time by cards)
Player 1: XOO | Player 2: XXO is optimal (wins 88% of the time, ties 6% of the time by tricks; wins 96% of the time, ties 1% of the time by cards)
Player 1: XOX | Player 2: OOX or XXO is optimal (OOX wins 79% of the time, ties 9% of the time by tricks; wins 92% of the time, ties 1% of the time by cards -- XXO wins 80% of the time, ties 8% of the time by tricks; wins 86% of the time, ties 1% of the time by tricks)

### Scenario 1 (XXX, countered by OXX)
In the first scenario, as soon as an O shows up, it is impossible for a rally to be won by Player 1. Any sequence of three consecutive Xs will be preceded by an O, necessarily creating the OXX sequence. Player 2 has roughly a 7 in 8 chance of winning each rally; if the first three cards of a rally are any sequence besides XXX, Player 2 will eventually win. Player 1 has to overcome these odds repeatedly in order to win, which is extremely unlikely.

### Scenario 2 (XXO, countered by OXX)
In the second scenario, a similar scenario to the first occurs. If the initial sequence is XXO or XXX, Player 1 will win the rally. XXX creates what we will call an inevitability, where an O creates the XXO sequence and an X only delays the inevitable winning O. Given any of the six other opening sequences, any pair of Xs will be preceded by an O before it can be succeeded by an O, creating the OXX sequence and giving Player 2 the win. Player 2 therefore has roughly a 3 in 4 chance of winning each rally. Player 1 has to overcome these odds repeatedly in order to win, which is also very unlikely.

### Scenario 3 (XOO, countered by XXO)
In the third scenario, neither sequence can begin until the first X appears, so the rally does not functionally begin until this occurs. Once the first X appears, a second X will lead to a similar inevitability for Player 2 to what we saw in the second scenario. If this X is followed by an OO, Player 1's sequence is created and they win; if it is followed by an OX, we return to the situation we were in after the initial X. To summarize:
O = no progress (50%)
X => XX = Player 2 win (25%)
X => XOO = Player 1 win (12.5%)
X => XOX = X, recur back to previous two examples (12.5%)
Three of the eight scenarios create end outcomes, and Player 2 wins two of these, so Player 2 has roughly a 2 in 3 chance of winning each rally. Player 1 has to overcome these odds repeatedly in order to win, which is fairly unlikely.

### Scenario 4 (XOX, countered by OOX or XXO)
For the fourth scenario, we will analyze the first counter-play option based on the initial three card sequence we see.
Counter 1: OOX
XXX, OXX: another X does not progress either sequence. OX creates Player 1's sequence, while OO creates an inevitability for Player 2. The winner of this opening is 50/50.
XXO, OXO: an X creates Player 1's sequence, while an O creates an inevitability for Player 2. The winner of this opening is 50/50.
XOO, OOO: consecutive Os create an inevitability for Player 2, so Player 2 wins.
XOX: this is Player 1's sequence, so Player 1 wins.
OOX: this is Player 2's sequence, so Player 2 wins.
There are three scenarios where Player 2 wins, one where Player 1 wins, and four 50/50s, so Player 2 has a 5 in 8 chance of winning. Player 1 has to overcome these odds repeatedly in order to win, which is fairly unlikely.
We will analyze the second counter-play option the way we did before.
Counter 2: XXO
In the fourth scenario's second counter, XXO, neither sequence can begin until the first X appears, so the rally does not functionally begin until this occurs. Once this X occurs, a second X will create an inevitability for Player 2. If the sequence starts XOX, Player 1 will win, but if it starts XOO, we are back in our initial stalemate situation, where neither sequence has made progress. Among the combination of cards that produce a result, two of them (XXX and XXO) result in a win for Player 2, and one of them (XOX) results in a win for Player 1. Player 2 therefore has roughly a 2 in 3 chance of winning each rally. Player 1 has to overcome these odds repeatedly in order to win, which is also fairly unlikely.

Questions you may still ponder after these explanations:
1) Why are the odds expressed "roughly" and not precisely?
   These games are not drawn from an infinite deck, but from a 52 card deck. The odds will slowly shift as imbalances between red cards and black cards are established.
2) Why are the odds across one million simulations roughly the same for OOX and XXO against XOX, despite one sequence having a 5 in 8 chance of winning and the other having a superior 2 in 3 chance of winning?
   This result may initially appear surprising, as in a one-shot round of this game, XXO is more likely to beat XOX than OOX. However, a long sequence of Xs or an XOX sequence drain the deck of Xs, which leaves more Os relatively. OOX has an advantage with more Os in the deck, since two consecutive Os make its victory inevitable. Using similar circumstances, deck drainage tends to favor the side with more win conditions.


### Tricks vs. Cards
We ran through each strategy under the assumption that the game is being played scoring by tricks. However, in every scenario, Player 2 is even more likely to win scoring by cards. For example, in the first scenario, a winning rally from Player 1 will win three cards no matter what, since Player 1 can only win if the rally starts with XXX. Player 2 can win any amount of cards from winning a rally; as soon as the first O shows up, cards will keep stacking up for Player 2 to win until an XX appears. Extra cards are either won from 50/50 scenarios or from these inevitabilities, which are only ever created for Player 2 over the course of our analysis. Player 2 is much more likely to win extra cards than Player 1, so Player 2 benefits more from scoring by cards.

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


