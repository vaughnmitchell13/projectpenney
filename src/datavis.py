from datagen import *
from dataproc import *
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

num_sims = 100

# generate game results
results_test = simulate(n_decks = num_sims)

# generate heat map
def get_heatmap(results = None, by_tricks = True):
    # results from simulate
    # by_tricks is true for scoring by tricks won, false for scoring by cards won
    
    # convert results to the data format we need
    # currently results returns a_wins_tricks, b_wins_tricks, a_wins_cards, b_wins_cards, ties_tricks, ties_cards
    # heatmap based on a_wins_tricks or a_wins_cards as a percentage of total sum
    # what we want to create: 8x8 matrix containing strictly win a_wins_tricks or a_wins_cards over total
    win_pcts = pd.DataFrame(np.zeros((8, 8)))
    score_col = 2
    if by_tricks:
        score_col = 0 # set to score by tricks or cards

    curr_result = 0
    for i in range(8):
        for j in range(8):
            if i == j:
                win_pcts.iloc[i, j] = None # skip over both sides picking same sequence
            else:
                # get total win values from current result
                # calculate percent
                # place percentage in win_pcts
                row = results.iloc[curr_result]
                pct = row.iloc[score_col] / (row[0] + row[1] + row[4])
                win_pcts.iloc[i, j] = pct
                curr_result += 1
                
    # heatmap creation will have the rest done in like 30 
    ax = sns.heatmap(
        win_pcts
    )

    plt.show()
