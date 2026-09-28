from datagen import *
from dataproc import *
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

num_sims = 20

# generate game results
results_test = simulate(n_decks = num_sims)

seq_labels = np.array(['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR'])

# generate heat map
def get_heatmap(results = None, by_tricks = True):
    # results from simulate
    # by_tricks is true for scoring by tricks won, false for scoring by cards won
    
    # convert results to the data format we need
    # currently results returns a_wins_tricks, b_wins_tricks, a_wins_cards, b_wins_cards, ties_tricks, ties_cards
    # heatmap based on a_wins_tricks or a_wins_cards as a percentage of total sum
    # what we want to create: 8x8 matrix containing strictly win a_wins_tricks or a_wins_cards over total
    win_pcts = pd.DataFrame(np.zeros((8, 8)))
    map_labels = pd.DataFrame(np.zeros((8, 8)))
    vers_col = 2
    vers_str = 'Cards'
    if by_tricks:
        vers_col = 0
        vers_str = 'Tricks' # set to score by tricks or cards
    num_sims = results.iloc[0, 0] + results.iloc[0, 1] + results.iloc[0, 4]

    curr_result = 0
    for i in range(8):
        for j in range(8):
            if i == j:
                win_pcts.iloc[i, j] = None # skip over both sides picking same sequence
                map_labels.iloc[i, j] = None
            else:
                # get total win values from current result
                # calculate percent
                # place percentage in win_pcts
                row = results.iloc[curr_result]
                pct = row.iloc[vers_col] / num_sims
                win_pcts.iloc[i, j] = round(pct * 100)
                curr_result += 1
                # formula where 0 => 4 and 2 => 5 is x/2 + 4
                map_labels.iloc[i, j] = f'{round(pct * 100)} ({round((row.iloc[vers_col//2 + 4] / num_sims) * 100)})'

    print(map_labels)
    ax = sns.heatmap(
        data = win_pcts, vmin = 0, vmax = 100,
        cmap = 'Blues',
        xticklabels = seq_labels,
        yticklabels = seq_labels,
        annot = map_labels,
        fmt = '',
        linewidths = 1,
        linecolor = 'white',
    )
    ax.set_facecolor('lightgrey')
    plt.xlabel('My Choice')
    plt.ylabel('Opponent Choice')
    plt.title(f'My Probability of Win (Tie) \nScoring by {vers_str}\nN = {num_sims}')

    plt.show()

get_heatmap(results_test)
        
