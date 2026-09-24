from datagen import create_shuffled_decks, get_tricks, get_card_counts, score, play_game
import seaborn as sns
import numpy as np

sequences = [['B', 'B', 'B'], ['B', 'B', 'R'], ['B', 'R', 'B'], ['B', 'R', 'R'], ['R', 'B', 'B'], ['R', 'B', 'R'], ['R', 'R', 'B'], ['R', 'R', 'R']]
num_sims = 10000

# generate random sequences
rand_yous = np.random.randint(0, 8, num_sims)
rand_opps = np.random.randint(0, 8, num_sims)

results = []
# generate game results
for i in range(0, num_sims):
    if rand_yous[i] != rand_opps[i]:
        results.append(play_game(sequences[rand_yous[i]], sequences[rand_opps[i]]))

print(results[0:10])
# generate heat map
# tbd soon
