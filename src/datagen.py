import numpy as np
from pathlib import Path
import datetime as dt


def create_shuffled_deck(seed: int = None) -> np.ndarray:
    '''
    Creates a representation of a standard 52 deck of cards (color only).
    Arguments:
        - seed (int): The random seed for the deck, default None
    Returns:
        - deck (NumPy array): The shuffled deck
    '''
    generator = np.random.default_rng(seed=seed)

    deck = np.array(['B'] * 26 + ['R'] * 26)
    generator.shuffle(deck)

    return deck

def generate_shuffled_decks(n_decks: int, n_cards = 52, base_seed: int = None) -> tuple[np.ndarray,np.ndarray]:
    '''
    Generates shuffled decks of shape (n_decks, 52).
    Arguments:
        - n_decks (int): The number of decks to generate
        - n_cards (int): The number of cards in each deck (default 52)
        - seed (int): The random starting seed for the deck, default None
    Returns:
        - deck_arr (NumPy array): The array of shuffled decks
        - seeds_arr (NumPy array): The seed for each deck
    
    '''
    if base_seed is None:
        base_seed = 1
    seeds = np.arange(base_seed,base_seed+n_decks)

    deck_arr = np.empty((n_decks,n_cards),dtype='U1')

    for i,seed in enumerate(seeds):
        deck_arr[i] = create_shuffled_deck(seed)

    return deck_arr,seeds

def save_decks(decks:np.ndarray, seeds: int) -> Path:
    '''
    Saves the generated shuffled decks 
    Arguments:
        - decks (NumPy array): The decks that were shuffled
    Returns:
        - filename (Path): The path of the file the saved decks exist at 

    '''
    PATH_DECKS = Path('../data/decks/raw/')
    PATH_DECKS.mkdir(parents=True,exist_ok=True)

    n_decks = decks.shape[0]
    n_cards = decks.shape[1]

    filename = PATH_DECKS/f'decks_{n_decks}x{n_cards}_startingseed_{seeds[0]}.npz'
    np.savez(filename,decks=decks,seeds=seeds)
    return filename


    
if __name__=="__main__":
    ### Initial test sequences before simulating
    decks,seeds = generate_shuffled_decks(n_cards=52,n_decks=100,base_seed=1)
    filename = save_decks(decks,seeds)
    data = np.load(filename)
    print(data['decks'][0])
    print(data['seeds'][1])
    print(len(data['decks']))
    for deck in data['decks']:
        print(deck)
