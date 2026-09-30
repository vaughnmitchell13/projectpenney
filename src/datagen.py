import numpy as np
from pathlib import Path
import datetime as dt


def generate_shuffled_decks(n_decks: int, n_cards = 52, seed: int = None) -> np.ndarray:
    '''
    Creates a representation of a standard 52 deck of cards (color only).
    Arguments:
        - seed (int): The random seed for the deck, default None
    Returns:
        - deck (NumPy array): The shuffled deck
        - seed (int): The random seed for the deck, used to generate the batch and file-naming
    '''
    generator = np.random.default_rng(seed=seed)

    deck_arr = np.empty((n_decks,n_cards),dtype='U1')

    for i in range(n_decks):
        deck = np.array(['B'] * 26 + ['R'] * 26)
        generator.shuffle(deck)
        deck_arr[i] = deck

    return deck_arr, seed


def save_decks(decks:np.ndarray, seed: int) -> Path:
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

    filename = PATH_DECKS/f'decks_{n_decks}x{n_cards}_seed{seed}.npz'
    np.savez(filename,decks=decks,seed=seed)
    return filename
