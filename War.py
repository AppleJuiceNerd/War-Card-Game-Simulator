from random import *
from sys import *  #arguments will be added soon(tm)



class Card:
	def __init__(self, value, suit):
		self.value_ = value
		self.suit_ = suit  #suit determ by num betwn 0-3

		# massive card initialization (else/if hell)

		if self.value_ <= 8: self.value = self.value_ + 2  #2-10
		elif self.value_ == 9: self.value = "Jack"
		elif self.value_ == 10: self.value = "Queen"
		elif self.value_ == 11: self.value = "King"
		elif self.value_ == 12: self.value = "Ace"
		else: print("This is not a valid value")

		if self.suit_ == 0: self.suit = "Spades"
		elif self.suit_ == 1: self.suit = "Hearts"
		elif self.suit_ == 2: self.suit = "Clubs"
		elif self.suit_ == 3: self.suit = "Diamonds"
		else: print("This is not a valid suit")

	def getCard(self):
		return f"{self.value} of {self.suit}"


class Deck:
	def __init__(self):
		self.Deck = []

		#initialize deck
		for s in range(4):  #suit
			for v in range(13):  #value
				self.Deck.append(Card(v, s))

	def Deal(self, plr1, plr2):
		shuffle(self.Deck)
		i = randint(1, 2)  #temporary variable
		for c in self.Deck:
			if i % 2 == 0: plr2.hand.append(c)  #if i is even
			else: plr1.hand.append(c)
			i += 1


class Player:
	def __init__(self):
		self.hand = []
		self.shand = []  #side hand - collected cards from battles


class Game:
	def __init__(self):
		self.p1 = Player()  # user of the program
		self.p2 = Player()
		self.Deck = Deck()
		self.Table = []  # used for wars

		self.Deck.Deal(self.p1, self.p2)

		#statistical variables
		self.Battles = 0
		self.BattlesWon = 0
		self.Wars = 0
		self.WarsWon = 0
		self.Restocks = 0

	def Battle(self):
		if len(self.p1.hand) == 0: self.Restock(self.p1)
		if len(self.p2.hand) == 0: self.Restock(self.p2)
		if self.CheckForLoss() == True: return 0

		self.Battles += 1

		if self.p1.hand[0].value_ > self.p2.hand[0].value_:
			print(f"You used {self.p1.hand[0].getCard()}")
			print(f"Opp used {self.p2.hand[0].getCard()}")
			print("You won the battle!\n")

			self.MoveCard(self.p1.hand, 0, self.p1.shand)
			self.MoveCard(self.p2.hand, 0, self.p1.shand)

			self.BattlesWon += 1

		elif self.p1.hand[0].value_ < self.p2.hand[0].value_:
			print(f"You used {self.p1.hand[0].getCard()}")
			print(f"Opp used {self.p2.hand[0].getCard()}")
			print("You lost the battle!\n")

			self.MoveCard(self.p1.hand, 0, self.p2.shand)
			self.MoveCard(self.p2.hand, 0, self.p2.shand)

		elif self.p1.hand[0].value_ == self.p2.hand[0].value_:
			print(f"You used {self.p1.hand[0].getCard()}")
			print(f"Opp used {self.p2.hand[0].getCard()}\n")
			self.War()

	def War(self):
		print("war initiated!!")
		if self.CheckForLoss() == True: return 0

		self.Wars += 1

		for i in range(4):
			if len(self.p1.hand) == 0: self.Restock(self.p1)
			if len(self.p2.hand) == 0: self.Restock(self.p2)
			if self.CheckForLoss() == True: return
			self.MoveCard(self.p1.hand, 0, self.Table)
			self.MoveCard(self.p2.hand, 0, self.Table)
		if len(self.p1.hand) == 0: self.Restock(self.p1)
		if len(self.p2.hand) == 0: self.Restock(self.p2)
		if self.CheckForLoss() == True: return

		if self.p1.hand[0].value_ > self.p2.hand[0].value_:
			print(f"You used {self.p1.hand[0].getCard()}")
			print(f"Opp used {self.p2.hand[0].getCard()}")
			print("You won the war!\n")

			self.MoveCard(self.p1.hand, 0, self.p1.shand)
			self.MoveCard(self.p2.hand, 0, self.p1.shand)

			for c in self.Table:
				shuffle(self.Table)
				self.p1.shand.append(c)
				self.Table.remove(c)

			self.WarsWon += 1

		elif self.p1.hand[0].value_ < self.p2.hand[0].value_:
			print(f"You used {self.p1.hand[0].getCard()}")
			print(f"Opp used {self.p2.hand[0].getCard()}")
			print("You lost the war!\n")

			self.MoveCard(self.p1.hand, 0, self.p2.shand)
			self.MoveCard(self.p2.hand, 0, self.p2.shand)

			for c in self.Table:
				shuffle(self.Table)
				self.p2.shand.append(c)
				self.Table.remove(c)

		elif self.p1.hand[0].value_ == self.p2.hand[0].value_:
			self.War()

	def Restock(self, plr):
		plr.shand.reverse()
		for c in plr.shand:
			plr.hand.append(c)
		plr.shand.clear()

	def CheckForLoss(self):
		if len(self.p1.hand) == 0 and len(self.p1.shand) == 0: return True
		elif len(self.p2.hand) == 0 and len(self.p2.shand) == 0: return True
		else: return False

	def MoveCard(self, cardsrc, cardidx,
														target):  #cardsrc = Card Source;  cardidx = Card Index
		if self.CheckForLoss(): return
		target.append(cardsrc[cardidx])
		cardsrc.remove(cardsrc[cardidx])

	def Play(self):
		while self.CheckForLoss() == False:
			self.Battle()
			#input()
		print('war over.\n')
		self.End()

	def End(self):
		if len(self.p2.hand)==0 and len(self.p2.hand)==0:
			print("You won!")
		else: print('You lost!')
		print("game done\n")
		print(f'''
Battles: {self.Battles}
Battles Won: {self.BattlesWon}
Wars: {self.Wars}
Wars Won: {self.WarsWon}
		''')


if __name__ == '__main__':
	War=Game()
	War.Play()
