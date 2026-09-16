import numpy as np


def create_shuffled_deck(seed: int = None) -> np.ndarray:
    '''
    Creates a representation of a standard 52 deck of cards (color only).
    Returns:
        - The shuffled deck as a NumPy array
    '''
    if seed is not None:
        generator = np.random.default_rng(seed=seed)
    else:
        generator = np.random.default_rng()

    deck = np.array(['B'] * 26 + ['R'] * 26)


    generator.shuffle(deck)
    return deck

def get_tricks(sequence_A: np.ndarray, sequence_B: np.ndarray, deck: np.ndarray) -> dict:
    '''
    Finds the position(s) of a sequence in the shuffled deck. Used for the original H-N Game.
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
    Counts the number of cards preceeding a sequence in the shuffled deck. Used for a variation of the game.
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


def score(sequence_A:np.ndarray, sequence_B: np.ndarray, deck:np.ndarray, by: str = "tricks") -> str:
    if by=="tricks":
        result = get_tricks(sequence_A,sequence_B,deck)

        A = result['A']
        B = result['B']

        if len(A) == 0 and len(B) == 0:
            return 'Tie'
        elif len(A) == len(B):
            return 'Tie'
        elif len(A) > len(B):
            return 'A wins'
        else:
            return 'B wins'
        
    elif by=="cards":
        result = get_card_counts(sequence_A,sequence_B,deck)

        A = result['A']
        B = result['B']

        if A == 0 and B == 0:
            return 'Tie'
        elif A == B:
            return 'Tie'
        elif A > B:
            return 'A'
        else:
            return 'B'
    else:
        raise ValueError("'by' must be 'tricks' or 'cards'")
         



def play_game(sequence_A: np.ndarray, sequence_B: np.ndarray, seed:int = None, by: str = "tricks") -> int:
    '''
    Plays the game of a specified variation.
    '''
    deck = create_shuffled_deck(seed=seed)
    winner = score(sequence_A,sequence_B, deck, by=by)
    print(winner)
    return winner

    
if __name__=="__main__":
    ### Initial test sequences before simulating
    a_sequence = np.array(['B','R','B'])
    b_sequence = np.array(['B','B','R'])
    play_game(a_sequence, b_sequence, by="tricks")
