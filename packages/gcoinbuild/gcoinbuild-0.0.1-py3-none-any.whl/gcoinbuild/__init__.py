import pygsheets
import sys
from os import system
import platform
from random import seed
from random import randint
import time

seed(1)

def get_os():
		plat = platform.system()
		if plat == 'Linux':
			return 'linux'
		elif plat == 'Darwin':
			return 'mac'
		elif plat == 'Windows':
			return  'nt'

def clear():
	pass
	os = get_os()
	if os in ('linux', 'mac'):
		system('clear')
	else:
		system('cls')
clear()

gc = pygsheets.authorize()

sh = gc.open('GCoin DB')
wk1 = sh.sheet1

class account:
	__loggedin__ = False
	__id__ = 0
	__mining__ = False

class mine_info:
	currentguess = 0
	earnings = 0
	successes = 0
	is_correct = False

def login(id, key):
	if key == wk1.cell((int(id) + 1, 2)).value:
		print("Logged in as ID: " + str(id))
		account.__loggedin__ = True
		account.__id__ = int(id)
		return 1
	else:
		return 0

def logout():
	print("Logged out")
	account.__loggedin__ = False
	account.__id__ = 0
	return 1

def create_account(key):
	run = True
	i = 0
	while run == True:
		i += 1
		if wk1.cell((i, 1)).value == "":
			run = False
			wk1.update_value(str(wk1.cell((i, 1)))[6:8], i - 1)
			wk1.update_value(str(wk1.cell((i, 2)))[6:8], key)
			wk1.update_value(str(wk1.cell((i, 3)))[6:8], 0)
			wk1.update_value(str(wk1.cell((i, 4)))[6:8], 0)
			return 1

def balance():
	return float(wk1.cell((account.__id__, 3)).value)

def update_key(newkey):
	wk1.update_value(str(wk1.cell((account.__id__, 2)))[6:8], newkey)
	return 1

def send_gcoin(recipientid, amount):
	if float(amount) > float(wk1.cell((account.__id__, 3)).value):
		return 0
	else:
		wk1.update_value(str(wk1.cell((account.__id__, 3)))[6:8], float(wk1.cell((account.__id__, 3)).value) - float(amount))
		wk1.update_value(str(wk1.cell((int(recipientid) + 1, 3)))[6:8], float(wk1.cell((int(recipientid) + 1, 3)).value) + float(amount))
		return 1

def mine():
	account.__mining__ = True
	guessme = randint(0, 50)
	successes = 0
	earnings = 0
	while account.__mining__ == True:
		guess = randint(0, 50)
		clear()
		if guess == guessme:
			mine_info.is_correct = True
			successes += 1
			earnings += 0.01
			wk1.update_value(str(wk1.cell((account.__id__, 3)))[6:8], float(wk1.cell((account.__id__, 3)).value) + 0.01)
			guessme = randint(0, 50)
			mine_info.currentguess = guess
			mine_info.successes = successes
			mine_info.earnings = earnings
			time.sleep(0.05)
			mine_info.is_correct = False
		else:
			mine_info.currentguess = guess
			mine_info.successes = successes
			mine_info.earnings = earnings
			time.sleep(0.05)

def stop_mine():
	account.__mining__ = False