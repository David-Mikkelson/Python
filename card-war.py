
import random
# Converting a number into a card for players
cards = {
		'2'   : 'Two',
		'3'   : 'Three',
		'4'   :	'Four',
		'5'   : 'Five',
		'6'   :	'six',		
		'7'   : 'Seven',
		'8'   :	'Eight',
		'9'   : 'Nine',
		'10'  : 'Ten',
		'11'  :	'Jack',
		'12'  : 'Queen',
		'13'  :	'King',
		'14'  : 'Ace'				
		}


def drawAcard(): return random.randint(2, 15)

def action(playerName):
	# This is where the dealer and player draw cards
	# the compare is done and returns who won
	# player, dealer or push
	player = drawAcard()
	house = drawAcard()
	print('{} draws a {} and Dealer draws a {}'.format(playerName, cards[str(player)], cards[str(house)]))
	if player < house:
		print("Sorry! Dealer wins")
		return ('dealer')
	elif player > house:
		print('Congradulation, you win!')
		return ('player')
	else:
		print('push')
		return('pushing')

def keep_going(playerName, player_money):
	# for asking if the player wants to continue
	try:
		s = input('Would {} like to place a bet on Card Wars? y/n '.format(playerName))
		#print(lower(s))
		if s.lower() != 'n':
			return('yes')
		else:
			print('Thank you for playing {}, your ending total is ${}.'.format(playerName, player_money))
			print('\n See you later.... ')
			return('quit')
	except:
		print('Please just a (y) or (n)')
		keep_going(playerName, player_money)


def main():
	# Start out with Players name and with $100
	playerName = input('Whats the players Name? ')
	player_money = 100
	print('Welcome {}, you are starting out with ${}'.format(playerName, player_money))
	
	while True:
		# Main loop to request bet and call all functions
		try:
			bet = int(input('How much would you like to bet? '))
		
		except:
			continue
		# See if player has the money or not
		if (player_money >= bet):
			# If player has the money
			winner = action(playerName)
			if winner == 'player':
				player_money += bet
				print('{} now has ${}'.format(playerName, player_money))	
			elif winner == 'dealer':
				player_money -= bet
				print('Dealer won.')
		else:
			# If player does not have the money
			print('{}, you only have {}.'.format(playerName, player_money))		
		# Are we done?
		DONE = keep_going(playerName, player_money)
		if DONE == 'quit':
			break


			
if __name__ == "__main__": main()









