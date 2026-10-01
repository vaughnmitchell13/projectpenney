import numpy as np
from pathlib import Path
import datetime as dt


def generate_shuffled_decks(n_decks: int, n_cards = 52, seed: int = None) -> np.ndarray | int:
    '''
    Creates a representation of a standard 52 deck of cards (color only).
    Arguments:
        - n_decks (int): The number of decks
        - n_cards (int): The number of cards
        - seed (int): The random seed for the deck, default None
    Returns:
        - deck_arr (NumPy array): The shuffled deck
        - seed (int): The random seed for the deck
    '''
    # Create a new Generator 
    generator = np.random.default_rng(seed=seed)

    # Assemble the deck array
    deck_arr = np.empty((n_decks,n_cards),dtype='U1') 

    # Fill the deck array with shuffled decks
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
        - seed (int): The random seed for the deck
    Returns:
        - filename (Path): The path of the file the saved decks exist at 

    '''
    PATH_DECKS = Path('./data/decks/')
    PATH_DECKS.mkdir(parents=True,exist_ok=True)

    n_decks = decks.shape[0] # (decks, cards)
    n_cards = decks.shape[1] # (decks,cards)

    filename = PATH_DECKS/f'decks_{n_decks}x{n_cards}_seed{seed}.npz'
    np.savez(filename,decks=decks,seed=seed)
    return filename
