import random

print("""
  ____  _            _           _            _
 |  _ \| |          | |         | |          | |
 | |_) | | __ _  ___| | __      | | __ _  ___| | __
 |  _ <| |/ _` |/ __| |/ /  _   | |/ _` |/ __| |/ /
 | |_) | | (_| | (__|   <  | |__| | (_| | (__|   <
 |____/|_|\__,_|\___|_|\_\  \____/ \__,_|\___|_|\_/

""")

# Define card values and suits
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        for rank in ranks:
            for suit in suits:
                card = Card(rank, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if self.value > 21 and 'Ace' in [card.rank for card in self.cards]:
            self.value -= 10

    def __str__(self):
        return ', '.join([str(card) for card in self.cards]) + f"\nTotal value: {self.value}"

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = Hand()

    def place_bet(self):
        while True:
            bet = input(f"{self.name}, you have {self.chips} chips. How much do you want to bet? ")
            if bet.isdigit() and int(bet) <= self.chips:
                self.chips -= int(bet)
                return int(bet)
            else:
                print("Invalid bet amount. Please try again.")

    def hit_or_stand(self):
        while True:
            action = input(f"{self.name}, do you want to hit or stand? ")
            if action.lower() == 'hit':
                return 'hit'
            elif action.lower() == 'stand':
                return 'stand'
            else:
                print("Invalid action. Please try again.")

    def win_bet(self, bet):
        self.chips += 2 * bet

    def push_bet(self, bet):
        self.chips += bet

    def __str__(self):
        return f"{self.name}:\n{str(self.hand)}"

# Initialize game
deck = Deck()
deck.shuffle()
player = Player('Player', 100)
dealer = Player('Dealer', 0)
dealer.hand.add_card(deck.deal_card())
player.hand.add_card(deck.deal_card())
dealer.hand.add_card(deck.deal_card())
player.hand.add_card(deck.deal_card())

# Main game loop
while True:
    print(f"\n{'='*20}\n{'Dealer':>10} | {str(dealer.hand.cards[0])}\n{'Player':>10} | {str(player.hand)}")

    # Player's turn
    while True:
        action = player.hit_or_stand()
        if action == 'hit':
            player.hand.add_card(deck.deal_card())
            print(f"\n{'='*20}\n{'Dealer':>10} | {str(dealer.hand.cards[0])}\n{'Player':>10} | {str(player.hand)}")
            if player.hand.value > 21:
                print(f"{player.name} busts! Dealer wins!")
                break
        else:
            break

    # Dealer's turn
    if player.hand.value <= 21:
        while dealer.hand.value < 17:
            dealer.hand.add_card(deck.deal_card())
        print(f"\n{'='*20}\n{'Dealer':>10} | {str(dealer.hand)}\n{'Player':>10} | {str(player.hand)}")
        if dealer.hand.value > 21:
            print(f"Dealer busts! {player.name} wins!")
            player.win_bet(bet)
        elif dealer.hand.value > player.hand.value:
            print("Dealer wins!")
        elif dealer.hand.value < player.hand.value:
            print(f"{player.name} wins!")
            player.win_bet(bet)
        else:
            print("Push!")
            player.push_bet(bet)

    # Ask player to play again
    if player.chips == 0:
        print(f"{player.name} is out of chips! Game over.")
        break
    while True:
        play_again = input("Do you want to play again? (y/n) ")
        if play_again.lower() == 'y':
            dealer.hand.cards = []
            player.hand.cards = []
            dealer.hand.value = 0
            player.hand.value = 0
            deck = Deck()
            deck.shuffle()
            dealer.hand.add_card(deck.deal_card())
            player.hand.add_card(deck.deal_card())
            dealer.hand.add_card(deck.deal_card())
            player.hand.add_card(deck.deal_card())
            break
        elif play_again.lower() == 'n':
            break
        else:
            print("Invalid input. Please try again.")

    if play_again.lower() == 'n':
        break

