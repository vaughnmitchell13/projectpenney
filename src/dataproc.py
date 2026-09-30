import numpy as np
from pathlib import Path
import pandas as pd
from .datagen import generate_shuffled_decks, save_decks
from datetime import datetime as dt

A_SEQUENCES = B_SEQUENCES =  np.array(['BBB',
                                       'BBR',
                                       'BRB',
                                       'BRR',
                                       'RBB',
                                       'RBR',
                                       'RRB',
                                       'RRR'])



def get_score(sequence_A:np.ndarray, sequence_B: np.ndarray, deck:np.ndarray) -> tuple:
    '''
    Determines Player A's and Player B's score (both variations of the game).
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - score (tuple): Contains the tricks and card totals for each player
    
    '''
    tricks_A = 0
    tricks_B = 0 
    cards_A = 0
    cards_B = 0
    seq_length = len(sequence_A)
    start = 0

    while True:
        index_A = deck.find(sequence_A, start)
        index_B = deck.find(sequence_B,start)
        if index_A == -1 and index_B == -1:
            break

        if index_A != -1 and (index_B == -1 or index_A <= index_B):
            end = index_A + seq_length
            tricks_A +=1
            cards_A += end-start
        else:
            end = index_B + seq_length
            tricks_B += 1
            cards_B += end-start
        start=end

    return tricks_A,cards_A,tricks_B,cards_B


def get_winner(sequence_A:np.ndarray, sequence_B: np.ndarray, deck) -> list:
    '''
    Compares the scores (by tricks and cards) to find the winner of the game.
    Arguments:
        - sequence_A (NumPy array): Player A's chosen sequence of cards
        - sequence_B (NumPy array): Player B's chosen sequence of cards
        - deck (NumPy array): The shuffled deck
    Returns:
        - winner_by_tricks_by_cards (list): The winner by tricks (indexed at [0]) and by cards (indexed at [1])
    '''
    tricks_A, cards_A, tricks_B, cards_B = get_score(sequence_A,sequence_B, deck)
    winner_by_tricks_by_cards = []

    if tricks_A == tricks_B:
        winner_by_tricks_by_cards.append('Tie')
    elif tricks_A > tricks_B:
        winner_by_tricks_by_cards.append('A')
    else:
        winner_by_tricks_by_cards.append('B')

    if cards_A == cards_B:
        winner_by_tricks_by_cards.append('Tie')
    elif cards_A > cards_B:
        winner_by_tricks_by_cards.append('A')
    else:
        winner_by_tricks_by_cards.append('B')

    return winner_by_tricks_by_cards

def assemble_df() -> pd.DataFrame:
    '''
    Creates the dataframe that will contain the simulated results.
    Returns:
        - result (DataFrame): A multi-indexed dataframe based on pairwise sequences for each outcome 
    '''
    match_sequences = []
    for a in A_SEQUENCES:
        for b in B_SEQUENCES:
            if a==b:
                continue
            match_sequences.append((a,b))
    idx = pd.MultiIndex.from_tuples(match_sequences, names=['A','B'])
    frame = pd.DataFrame(0,index=idx,columns=['A Wins by Tricks',
                                              'B Wins by Tricks',
                                              'Ties by Tricks',
                                              'A Wins by Cards',
                                              'B Wins by Cards',
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
    PATH_PROCESSED = Path('../data/processed/')
    PATH_PROCESSED.mkdir(parents=True,exist_ok=True)
    results = assemble_df()
    decks, seed = generate_shuffled_decks(n_decks=n_decks,n_cards=n_cards,seed=seed)
    save_decks(decks,seed)
    decks = ["".join(deck) for deck in decks]

    t0 = dt.now()
    for a in A_SEQUENCES:
        for b in B_SEQUENCES:
            if a==b:
                continue
            A_WINS_TRICKS = 0
            A_WINS_CARDS = 0
            TIES_TRICKS = 0
            TIES_CARDS = 0
            for deck in decks:
                winner = get_winner(a,b,deck)
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
            results.loc[(a,b),:] = [A_WINS_TRICKS,
                                    B_WINS_TRICKS,
                                    TIES_TRICKS,
                                    A_WINS_CARDS,
                                    B_WINS_CARDS,
                                    TIES_CARDS]
            print(f"Simulated {a} vs {b} with {n_decks} decks")
    duration = dt.now()-t0
    print(f"Simulation done. Elapsed: {duration}")
    filename = PATH_PROCESSED/f'results_{n_decks}x{n_cards}_seed{seed}.csv'
    results.to_csv(filename)
    return results

    
     
     
     