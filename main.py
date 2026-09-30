import pandas as pd
from src.dataproc import simulate
from src.datavis import get_heatmap
from src.datagen import *
from pathlib import Path


def main():
    PATH_PROCESSED = Path('data/processed/')
    PATH_PROCESSED.mkdir(parents=True,exist_ok=True)

    print('\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('| Welcome to Project Penney! |')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print('\n(1) Show heatmap of 1,000,000 simulations')
    print('(2) Add an additional N simulations to the heatmap')
    one_million = pd.read_csv("data/processed/results_1000000x52_seed440.csv").set_index(['A','B'])
    choice = input('\nChoose an option: ')
    if choice == '1':
        get_heatmap(one_million,by_tricks=True)
        get_heatmap(one_million,by_tricks=False)
    elif choice == '2':
        N = int(input('\nHow many decks would you like to add? '))
        if N > 0:
            seed = int(input('\nWhat seed would you like for this new batch of decks? '))
            if seed is None:
                addl_results = simulate(n_decks=N, seed=None)
            else:
                addl_results = simulate(n_decks=N,seed=seed)
            result = one_million.add(addl_results)
            filename = PATH_PROCESSED/f'results_{1000000+N}x52_seed{seed}.csv'
            result.to_csv(filename)
            get_heatmap(result,by_tricks=True)
            get_heatmap(result,by_tricks=False)
        else:
            print(f"INVALID CHOICE: N must be greater than 0.")

    else:
        print(f"INVALID CHOICE: {choice} not recognized.")


if __name__ == "__main__":
    main()
