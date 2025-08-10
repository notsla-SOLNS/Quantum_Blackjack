from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator  # New recommended simulator
import numpy as np



bitstrings = ['00', '01', '10', '11']

#==============================================================================
# Create dictionary to contain each of the suits and their bitstring assignment
#

bit_string_to_suit = {'♦': '00', '♠': '01', '♥': '10', '♣': '11' }
bit_string_to_pic = {'J': '00', 'Q': '01', 'K': '10', 'A': '11' }
bit_string_to_number = {
    2: '0000',
    3: '0001',
    4: '0010',
    5: '0011',
    6: '0100',
    7: '0101',
    8: '0110',
    9: '0111',
    10: '1000'
}


#
# Create circuit
#

def two_qubit_circuit():
    

    suit_circuit = QuantumCircuit(2, 2)
    
    suit_circuit.h([0, 1])  # Hadamard gates
    
    suit_circuit.measure([0, 1], [0, 1])
    
    #
    # Run using AerSimulator (modern approach)
    #
    
    simulator2_qubit = AerSimulator()
    result = simulator2_qubit.run(suit_circuit, shots=1000).result()
    counts = result.get_counts()
    
    return counts



def find_mode_result(counts):
    """
    Calculates result of the measurement, either 00,01,10,11, by finding the 
    bitstring that is found the most by measurement.
    """
    modal_bitstring = max(counts, key=counts.get )
    
    return modal_bitstring


def selection_from_bitstring(modal_bitstring, bit_string_to_suit):
    
    """
    Determines the card's suit by checking the modal bitstring from measurement
    against the associated suit from the user defined dictionary'
    """
    
    #determine suit of first card
    
    card_suit = None
    
    for m in range(len(bit_string_to_suit)):
        
        if modal_bitstring == list(bit_string_to_suit.values())[m]:
            
            card_suit = list(bit_string_to_suit.keys())[m]
            
    
    return card_suit


#==============================================================================
# TO fairly determine pic or num card, need a fresh quantum circuit
#

#
# Create circuit for card type, only need 1 qubit this time
#
def one_qubit_circuit():
    
    type_circuit = QuantumCircuit(1, 1)
    
    type_circuit.h(0)  # Hadamard gates
    
    type_circuit.measure([0],[0])
    
    #
    # Run using AerSimulator
    #
    simulator1_qubit = AerSimulator()
    type_result = simulator1_qubit.run(type_circuit, shots=1000).result()
    type_counts = type_result.get_counts()
    
    return type_counts







def pic_or_num(type_counts):
    """
    this function will determine picture or number card based on measurement
    of single qubit ( 0 for Pic or 1 for Num)
    """
    
    modal_bit = int(find_mode_result(type_counts))
    
    # print(modal_bit)
    
    if modal_bit == 1:
        
        card_type = 'N'
        
        # print('1: card type ' + card_type)
    
    else:
        
        card_type = 'P'
        
    return card_type
        


#==============================================================================
#
# Now to determine the final card, need to run another 2 qubit circuit for pics
# and also create a 4 qubit circuit for number selection
#

def four_qubit_circuit():
    
    suit_circuit = QuantumCircuit(4, 4)
    
    suit_circuit.h([0, 1, 2, 3])  # Hadamard gates
    
    suit_circuit.measure([0, 1, 2, 3], [0, 1, 2, 3])
    
    #
    # Run using AerSimulator (modern approach)
    #
    
    simulator4_qubit = AerSimulator()
    result = simulator4_qubit.run(suit_circuit, shots=1000).result()
    counts3 = result.get_counts()
    
    return counts3

#
# Now build the scoring mechanic to determine winner
#

numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10']


def player_score(players_cards):
    
    """ Cycles through each 2 letter card name in the list of player's cards
    and extracts the second character of the string. Then if this is a number (as in the list above) 
    the current score gets updated to be just that, and if it is a picture the current hand score gets +10.
    If it is an ace, the ace value function is called which asks user to input what they want all the aces
    in their hand to be worth. Final hand score is returned.
    """
    
    # player's score first
    current_score = 0
    
    for m in range(len(players_cards)):
        
        current_card = str(players_cards[m])[1]
        
        # print(current_card)
        
        if current_card in numbers:
            
            current_score += int(current_card)
            
            
        elif current_card != 'A':
            
            current_score += 10
    
    players_score = current_score + ace_value_control(players_cards)
    
    
    return players_score
            
            
            
            

def ace_value_control(players_cards):
    
    """ Determines the value of each ace in the user's hand and returns for use in
    score calculation.
    """
    
    #
    # ace control for player
    #
    ace_scores = []
    num_aces = 0
    
    for card in players_cards:
        
        # count how many aces in the hand
        
        if 'A' in card:
            
            num_aces += 1
            
            ace_scores.append(int(input('Enter value of Ace no.{}, "1" or "11": '.format(num_aces))))
            
        total_ace_score = sum(ace_scores)   
        
    return total_ace_score        



def deal_cards(cards_needed):
    
    cards = []   
    
    for  i in range(0,cards_needed):
       
                    
        card = ''
        
        counts = two_qubit_circuit()
        
        modal_bitstring = str(find_mode_result(counts))
        
        suit = selection_from_bitstring(modal_bitstring, bit_string_to_suit)
        # print(suit)
        card = card + suit
        
        type_counts = one_qubit_circuit()
        
        
        card_type = pic_or_num(type_counts)
        # print(card_type)
        
        
        if card_type == 'P':
            
            counts2 = two_qubit_circuit() # find the bitstring pops
            
            modal_result2 = find_mode_result(counts2) # find modal result
            
            # pass new tings into previous function for determining suit
            
            picture = selection_from_bitstring(modal_result2, bit_string_to_pic) 
            
            # print(picture)
            card = card + picture
        
            cards.append(card)
            
        else:
            
            valid_string = False
            
            while valid_string == False:
                
                counts_for_num = four_qubit_circuit()
                
                modal_result3 = find_mode_result(counts_for_num)
                
                # print('Hello 1')
            
                if modal_result3 in list(bit_string_to_number.values()):
                    
                    valid_string = True
                    
                    # print('Hello2')
            
            number = selection_from_bitstring(modal_result3, bit_string_to_number)
            
            card = card + str(number)
            # print(number)
            
        
            cards.append(card)
            
        
            
        # print(card) # print('Card {}: {}'.format(i,player_card))
        
    return cards
        


    
    
def house_score():
    
    num_aces = 0
    aces_score = 0
    h_current_score = 0
    
    #
        
    for m in range(len(houses_cards)):
        
        current_card = str(houses_cards[m])[1]
        
        # print(current_card)
        
        if current_card in numbers:
            
            h_current_score += int(current_card)
            
            
        elif current_card != 'A':
            
            h_current_score += 10
        
        # if we have an ace:
            
        elif current_card == 'A':
            
            num_aces += 1
            
            # by default add 11 for each
            
            aces_score += 11
            # print("Aces_score: {}".format(aces_score))

        
    return h_current_score+aces_score, num_aces, 



def last_card_in_hand_score(num_aces):
    
    # final_card = houses_cards[int(len(houses_cards))-1,int(len(houses_cards))]
    final_card = houses_cards[-1][-1]  # Gets the last element of the last row
    final_card_val = 0
    
    print(final_card)
    
    if final_card in numbers:
        
        final_card_val += int(final_card)
        
        
    elif final_card != 'A':
        
        final_card_val += 10
    
    # if we have an ace:
        
    elif final_card == 'A':
        
        num_aces += 1
        
        # by default add 11 for each
        
        final_card_val += 11
        # print("Aces_score: {}".format(aces_score))
        
    return final_card_val, num_aces
   
    
#==============================================================================
#
# Build circuit to determine success of quantum ace and change user's selected card with QA
#
def quantum_ace():
    
    qc_ace = QuantumCircuit(1,1)
    
    
    theta = 2 * np.arcsin(np.sqrt(0.65))  # 70% bias toward |1⟩ (Ace)
    
    qc_ace.ry(theta, 0)  # Rotate qubit to √0.3|0⟩ + √0.7|1⟩

    qc_ace.measure([0],[0])
    
    simulator_ace = AerSimulator()
    
    result = simulator_ace.run(qc_ace, shots=1, memory=True).result()
    memory = result.get_memory()  # Returns list like ['0'] or ['1']
    collapsed_state = memory[0]
    
    # print(collapsed_state)

    # print(f"Qubit collapsed to |{collapsed_state}⟩")
    
    if collapsed_state == '1':
        
        to_be_replaced = int(input("Success! Select card to be replaced: "))
        print(" ")
        
        players_cards[to_be_replaced] = 'QA'
        
        quantum_table = True
        
        print_table(quantum_table, houses_turn)
        
    else:
        
        print("Failure! You are cursed with classical cards.")
        print(" ")
        
        quantum_table = False
        
    return quantum_table



def print_table(quantum_table, houses_turn):
    
    if quantum_table == True:
        
        
        print(" ")
        print("=== QUANTUM TABLE ===")  
        print(" ")
        print("House: {}".format(" ".join(map(str, houses_cards))))   
        print(" ")
        # reveal player's hand
        
        print("  You: {}".format(" ".join(map(str, players_cards))))
        print(" ")
        print("=====================")  
        
        print(" ")
        
    elif quantum_table == False and houses_turn == True:
        
        print(" ")
        print("======= TABLE =======")  
        print(" ")
        print("House: {}".format(" ".join(map(str, houses_cards))))   
        print(" ")
        # reveal player's hand
        
        print("  You: {}".format(" ".join(map(str, players_cards))))
        print(" ")
        print("=====================")  
        
        print(" ")
        
    elif houses_turn == False:
        
        print(" ")
        print("======= TABLE =======")  
        print(" ")
        print("House: {}".format(houses_cards[0])) 
        print(" ")
        # reveal player's hand
        
        print("  You: {}".format(" ".join(map(str, players_cards))))
        print(" ")
        print("=====================")  
        
        print(" ")
        
        

def win_streak_tracking(win_streak, save_QA):
    
    if save_QA == True:
        
        allow_QA = True
        
    else:
        
        
        if win_streak == 2:
            
            allow_QA = True
            
        else:
            
            allow_QA = False

    return allow_QA
     
    
# deal 2 cards to player and two to the house

player_wins = 0
house_wins = 0
draws = 0


win_streak = 0
allow_QA = False
save_QA = False


hands = int(input("How many hands would you like to play?: "))
print(" ")
for l in range(hands):
    
    print(" ")
    print("---------------")
    print("Round {}".format(l+1))
    print("---------------")
    
    players_cards = []
    houses_cards = []
    
    cards_needed = 2 # ( 2 each )
    
    players_cards.extend(deal_cards(cards_needed))
    houses_cards.extend(deal_cards(cards_needed))
    
    quantum_table = False
    houses_turn = False
    
    print_table(quantum_table, houses_turn)
    
    # ask user to stick or twist
    
    twist = True
    
    # Loop to keep adding cards until user says stop
            
    while twist == True:
        
        # if twist:
                
        repeat = True 
        
        while repeat == True:
            
            S_or_T = str(input("S/T?: "))
            print(" ")
            
            if S_or_T == 'S':
                
                twist = False
                
                repeat = False
                
            elif S_or_T == 'T':
                
                cards_needed = 1
                
                players_cards.extend(deal_cards(cards_needed))
                
                print_table(quantum_table, houses_turn)
                
                repeat = False
            
            else:
                
                print("Invalid entry, try again.")
                print(" ")
                repeat = True
                
    
    # introduce quantum ace
    try_again = True
    
    
    allow_QA = win_streak_tracking(win_streak, save_QA)
        
    # CHECK winstreak and if = 2:
    
    if not save_QA and allow_QA:
        print("****************************************")
        print("Quantum Ace UNLOCKED! - saved until use.")
        print("****************************************")
              
    if allow_QA:
        
        while try_again == True:
            
            print(" ")
            activate_ace = input("Activate Quantum Ace? Y/N: ")
            print(" ")
            
            if activate_ace == 'Y':
                
                quantum_ace()
                
                try_again = False
                
                save_QA = False
                
            elif activate_ace != 'N':
                
                print("Invalid input, try again.")
                
                
            else:
                
                try_again = False
                
                save_QA = True
        
    
        
    # calculate player's score
    
    players_score = player_score(players_cards)
    
    
    #Now house plays, and calculate its score
    
    score_h = house_score()[0]
    
    houses_turn = True
    
    # Introduce Ace + 6 later
    
    while score_h < 17 :
        
        cards_needed = 1
        
        houses_cards.extend(deal_cards(cards_needed))
        
        score_h = house_score()[0] # should update score, redoing with all new cards
        
        
    used_aces = 0
    
    
    num_aces = house_score()[1]
    
    # print("origonal number of aces {}".format(num_aces))
    
    
    while score_h > 21 and used_aces != num_aces:
        
        
        if num_aces != 0: # need to keep track of how many aces have been changed
        
            for m in range(num_aces):
            
                score_h -= 10
                
                used_aces += 1
                
                # print('Score adjusted for ace, score now: {}'.format(score_h))
                # to get further HIT when changing ace value takes score to <17
                if score_h < 17 :
                 
                    cards_needed = 1
                    
                    houses_cards.extend(deal_cards(cards_needed))
                    
                    score_h += last_card_in_hand_score(num_aces)[0] # should update score with value of new card
                    
                    num_aces = last_card_in_hand_score(num_aces)[1] #update number of aces
                    
                    # print("Number of aces in hand after HIT: {}".format(num_aces))
                    
                    # print('Score went <17, is now: {}'.format(score_h))
                    
                    
                if 17 <= score_h <= 21:
                    
                    break
                
                elif score_h > 21:
                    
                    break
                
      
    print_table(quantum_table, houses_turn)

    
        
    #add up scores and reveal winner
    print(" ")  
    print("You {} - {} House".format(players_score, score_h))
    print(" ")
        
    house_bust = False
    player_bust = False
    
    if players_score > 21:
        
        player_bust = True
        
    if score_h > 21:
        
        house_bust = True
        
    # determine winner and count wins
    
    
        
    if player_bust == True and score_h <= 21:
        print(" ")  
        print("You Lose.")
        
        house_wins += 1
        
        win_streak = 0
        
  
        
    elif player_bust == False and house_bust == True:
        print(" ")  
        print("You win!")
        player_wins += 1
        
        win_streak += 1
        

    
    elif player_bust == True and house_bust == True:
        
        print("Both bust - You Lose.")
        
        house_wins += 1
        
        win_streak = 0
        
     
        
    elif player_bust == False and house_bust == False:
        
        if players_score > score_h:
            print(" ")  
            print("You Win!")
            
            player_wins += 1
            
            win_streak += 1
            
           
            
        elif players_score == score_h:
            print(" ")  
            print("Draw.")
            
            win_streak = 0
            
            
            
            draws += 1
        else:
            print(" ")  
            print("You Lose.")
            
            house_wins += 1
            
            win_streak = 0
            

    
    
    
            
            



    
