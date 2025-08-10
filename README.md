# Quantum_Blackjack

10/Aug/25

A user vs house bot game with implementations of true randomness originating from quantum principles via Qiskit code.

Classic blackjack casino game for one player vs the house with a 'Quantum Ace' power-up. Dealing of cards to both player and the house is done via true randomness using (in the case of the code) the simulator in the Qiskit package. This code could be adapted so that the quantum circuits involved in dealing and the control of the 'Quantum Ace' game mechanic are run on an IBM quantum computer. 

The 'Quantum Ace' is activated once the user hits a 2-game win streak, and can be saved until desired. Upon activation, the user can select a card in their hand (after ending their turn, but before final scoring) to change to an Ace by entering n-1 according to the card's position in their hand (to be changed), and then choose whether they want this Ace to be valued 1 or 11. This mechanic is to offer a reward to the player and help them build win streaks.


Scope for further developments include:

  * improved output visuals - use tkinter?
  * make the house twist on Ace+6 initial hand
  * have a running win streak counter - special rewards at 5,10 wins etc.?
  * further implementations of Qiskit as new game mechanics/power-ups
  * clean up code, add function explanations and comments to track the logic
