from .datagen import *
from .dataproc import *
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def get_heatmap(results: pd.DataFrame = None, by_tricks: bool = True) -> None:
    """
    Creates the heatmaps for the simulation's results by tricks and by score.
    Arguments: 
        - results (DataFrame): The results of a simulation
        - by_tricks (bool): Flag to generate based on tricks
    Returns:
        - None
    """
    PATH_HM = Path('./figures')
    PATH_HM.mkdir(parents=True,exist_ok=True)
    SEQ_LABELS = np.array(['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR'])
    win_pcts = pd.DataFrame(np.zeros((8, 8)))
    map_labels = pd.DataFrame("",index=range(8), columns=range(8))
    vers_col = 4
    vers_str = 'Cards'
    if by_tricks:
        vers_col = 1
        vers_str = 'Tricks' # set to score by tricks or cards
    num_sims = results.iloc[0, 0] + results.iloc[0, 1] + results.iloc[0, 2]

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
                win_pcts.iloc[i, j] = round(pct * 100,2)
                curr_result += 1
                map_labels.iloc[i, j] = f'{round(pct * 100)}\n({round((row.iloc[vers_col + 1] / num_sims) * 100)})'
    plt.figure(figsize=(10,8))
    ax = sns.heatmap(
        data = win_pcts, vmin = 0, vmax = 100,
        cmap = 'Blues',
        xticklabels = SEQ_LABELS,
        yticklabels = SEQ_LABELS,
        annot = map_labels,
        fmt = '',
        linewidths = 1,
        linecolor = 'white',
    )
    ax.set_facecolor('lightgrey')
    plt.xlabel('My Choice')
    plt.ylabel('Opponent Choice')
    plt.title(f'My Probability of Win (Tie) \nScoring by {vers_str}\nN = {num_sims}')
    filename = PATH_HM/f'heatmap_n_{num_sims}_by_{"tricks" if by_tricks else "cards"}.png'
    plt.savefig(filename, dpi=300)

    plt.show()
    return


