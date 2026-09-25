import numpy as np
import pathlib as Path
import pandas as pd
from datagen import *

A_SEQUENCES = np.array([['B','B','B'],
                        ['B','B','R'],
                        ['B','R','B'],
                        ['B','R','R'],
                        ['R','B','B'],
                        ['R','B','R'],
                        ['R','R','B'],
                        ['R','R','R']])

B_SEQUENCES = np.array([['B','B','B'],
                        ['B','B','R'],
                        ['B','R','B'],
                        ['B','R','R'],
                        ['R','B','B'],
                        ['R','B','R'],
                        ['R','R','B'],
                        ['R','R','R']])

def get_tricks(sequence_A: np.ndarray, sequence_B: np.ndarray, deck: np.ndarray) -> dict:
    '''
    Finds the position(s) of a trick in the shuffled deck for each player. Used for the original H-N Game.
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - tricks_dict (dictionary): A dictionary keyed by the player and valued by a list of their trick positions
    '''
    tricks_A = []
    tricks_B = []
    for i in range(len(deck)-len(sequence_A)+1):
        if np.array_equal(sequence_A,deck[i:i+len(sequence_A)]):
            tricks_A.append(i)
    
        if np.array_equal(sequence_B,deck[i:i+len(sequence_B)]):
                        tricks_B.append(i)
    tricks_dict = {'A': tricks_A, 'B': tricks_B}
    return tricks_dict

def get_card_counts(sequence_A: np.ndarray, sequence_B: np.ndarray, deck: np.ndarray) -> dict:
    '''
    Counts the number of cards preceeding a sequence in the shuffled deck. Used for Ron's variation of the game.
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - total_dict (dictionary): A dictionary keyed by the player and valued by their total cards taken
    '''
    total_A = 0
    total_B = 0
    total_dict = {'A': 0,'B':0}
    i = 0
    while i <= len(deck) - len(sequence_A):
        if np.array_equal(sequence_A, deck[i:i+len(sequence_A)]):
            cards_won=i+len(sequence_A)
            total_A+=cards_won
            total_dict['A'] = total_A
            deck = deck[cards_won:]
            i=0
        if np.array_equal(sequence_B,deck[i:i+len(sequence_B)]):
            cards_won=i+len(sequence_B)
            total_B+=cards_won
            total_dict['B'] = total_B
            deck = deck[cards_won:]
            i=0
        i+=1
    return total_dict


def get_score(sequence_A:np.ndarray, sequence_B: np.ndarray, deck:np.ndarray) -> dict:
    '''
    Extracts Player A's and Player B's tricks and cards.
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - tricks_A (list): Player A's position(s) of tricks in the deck
        - cards_A (int): Player A's total cards
        - tricks_B (list): Player B's position(s) of tricks in the deck
        - cards_B (int): Player B's total cards
    
    '''
    result_tricks = get_tricks(sequence_A,sequence_B,deck)
    result_cards = get_card_counts(sequence_A,sequence_B,deck)
    tricks_A = result_tricks['A']
    tricks_B = result_tricks['B']
    cards_A = result_cards['A']
    cards_B = result_cards['B']
    return tricks_A, cards_A, tricks_B, cards_B


def get_winner(sequence_A:np.ndarray, sequence_B: np.ndarray, deck) -> list:
    '''
    Compares the scores (by tricks and cards) to find the winner of the game.
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - by_tricks_by_cards (list): The winner by tricks (indexed at [0]) and by cards (indexed at [1])
    '''
    tricks_A, cards_A, tricks_B, cards_B = get_score(sequence_A,sequence_B, deck)
    by_tricks_by_cards = []
    if len(tricks_A) == len(tricks_B):
        by_tricks_by_cards.append('Tie')
    elif len(tricks_A) > len(tricks_B):
        by_tricks_by_cards.append('A')
    else:
        by_tricks_by_cards.append('B')

    if cards_A == cards_B:
        by_tricks_by_cards.append('Tie')
    elif cards_A > cards_B:
        by_tricks_by_cards.append('A')
    else:
        by_tricks_by_cards.append('B')
    return by_tricks_by_cards

def assemble_df() -> pd.DataFrame:
    '''
    Creates the dataframe that will contain the simulated results.
    Returns:
        - result (DataFrame): A multi-indexed dataframe based on pairwise sequences for each outcome 
    '''
    match_sequences = []
    for a in A_SEQUENCES:
        for b in B_SEQUENCES:
            if np.array_equal(a,b):
                continue
            match_sequences.append((tuple(a),tuple(b)))
    idx = pd.MultiIndex.from_tuples(match_sequences, names=['A','B'])
    frame = pd.DataFrame(0,index=idx,columns=['A Wins by Tricks',
                                              'B Wins by Tricks',
                                              'A Wins by Cards',
                                              'B Wins by Cards',
                                              'Ties by Tricks',
                                              'Ties by Cards'])
    return frame

def simulate(n_decks: int = 1000000, n_cards: int = 52, seed: int=None):
    '''
    Simulates the game with a chosen seed to generate data
    Arguments:
        - n_decks (int): The number of decks for the Monte Carlo simulation (default 1000000)
        - n_cards (int): The number of cards each deck will have (default 52)
        - seed (int): The random seed for the decks (default None)
    Returns: 
        - result (DataFame): A Pandas dataframe of the results 
    '''
    PATH_RESULTS = Path('../data/processed/')
    PATH_RESULTS.mkdir(parents=True,exist_ok=True)
    results = assemble_df()
    decks, seeds = generate_shuffled_decks(n_decks=n_decks,n_cards=n_cards,base_seed=seed)
    saved_data = save_decks(decks,seeds)
    data = np.load(saved_data)

    for a in A_SEQUENCES:
        for b in B_SEQUENCES:
            if np.array_equal(a,b):
                continue
            A_WINS_TRICKS = 0
            A_WINS_CARDS = 0
            TIES_TRICKS = 0
            TIES_CARDS = 0
            for i in range(len(data['decks'])):
                winner = get_winner(a,b,data['decks'][i])
                if winner[0]=='A':
                    A_WINS_TRICKS+=1
                elif winner[0]=='Tie':
                    TIES_TRICKS+=1
                if winner[1]=='A':
                    A_WINS_CARDS+=1
                elif winner[1]=='Tie':
                    TIES_CARDS+=1
            B_WINS_TRICKS = n_decks-A_WINS_TRICKS-TIES_TRICKS
            B_WINS_CARDS = n_decks-A_WINS_CARDS-TIES_CARDS
            results.loc[(tuple(a),tuple(b)),:] = [A_WINS_TRICKS,
                                              B_WINS_TRICKS,
                                              A_WINS_CARDS,
                                              B_WINS_CARDS,
                                              TIES_TRICKS,
                                              TIES_CARDS]
    filename = PATH_RESULTS/f'results_{n_decks}x{n_cards}_startingseed_{seeds[0]}.csv'
    results.to_csv(filename)
    return results

if __name__=="__main__":
    simulate(1_000,52,1)
    
     
     
     