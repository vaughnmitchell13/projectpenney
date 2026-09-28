from datagen, dataproc import *
import seaborn as sns
import numpy as np

num_sims = 10000

# generate game results
results = simulate(n_decks = 1000)

print(results[0:10])

# generate heat map
def get_heatmap(results, by_tricks = True):
    # results from simulate
    # by_tricks is true for scoring by tricks won, false for scoring by cards won
    
    # convert results to the data format we need
    # currently returns a_wins_tricks, b_wins_tricks, a_wins_cards, b_wins_cards, ties_tricks, ties_cards
    # heatmap must be based on a_wins_tricks or a_wins_cards as a percentage of total sum
    # what we want to create: 8x8 matrix containing strictly win a_wins_tricks or a_wins_cards over total
    win_pcts = pd.DataFrame(np.zeros((8, 8)))
    return 9
    
