__version__="0.5.0"
__author__="Muhammad Al Fajri"
__email__="fajrim228@gmail.com"
__telegram__="ini_peninggi_badan"

import os
import json
import getpass
import jwt
import requests
import pause
import time
import sys
import curses
import logging
import itertools
import webbrowser
import colorama as C
from colorama import Fore as F
from json import JSONDecodeError
from waveradio.app import (
	WaveRadio,
	Ranking,
	UpCall, 
	SearchUser, 
	writeConfig
)
from halo import Halo
from threading import Thread
from prettytable import PrettyTable
from waveradio.conf import wave_token, wavemanager

DEFAULT = F.LIGHTWHITE_EX
Menu = {
	"1":"send like / taplove",
	"2":"send listener / join (rusak)",
	"3":"spam, room live chat",
	"4":"feedback bot (developing)",
	"5":"take down (rusak)",
	"6":"join (bot listeners)",
	"7":"cek rank", 
	"8":"hapus groupcall (rusak)", 
	"9":"create groupcall (rusak)", 
	"10":"mute user", 
	"11":"unmute user (rusak)", 
	"12":"terima request livecall", 
	"13":"turunkan user on mic"
}
        
def UpCallHandler(type_of: str, username: str):
	Loading = Halo(text ="Lagi scanning rank..", placement = "right")
	Loading.start()
	x = Ranking().RankData()
	X = PrettyTable(padding_width=1, border=True)
	X.field_names = ["no","DJ", "Judul"]
	i = 0
	Loading.stop()
	for data in x:
		i+=1
		dj = data['dj']
		title = data['title']
		X.add_row([i,dj, title])
	print(X.get_string())
	index_of = int(input(F.RED + "-> " + DEFAULT + "Masukan nomor room: " + F.GREEN)) - 1
	print(DEFAULT)
	IDRoom = x[index_of]['idroom']
	streamer = x[index_of]["dj"]
	title = x[index_of]["title"]
	rank = index_of
	url_picture = x[index_of]["profile_pic"]
	like_count = x[index_of]["like_count"]
	if type_of == "off":
		UpCall(IDRoom).OffCall()
	elif type_of == "on":
		UpCall(IDRoom).OnCall()
	elif type_of == "accept":
		UpCall(IDRoom).AcceptAllRequest()
	elif type_of == "kick":
		datas = UpCall(IDRoom).UpCallParticipants()
		for i in range(len(datas) - 1):
			i += 1
			print(i, datas[i]["nickname"])
		index_of_ = int(input("`masukan nomor user: "))
		user_id = datas[index_of_]["user_id"]
		UpCall(IDRoom).LeaveCall(user_id=user_id)
	elif type_of == "mute":
		datas = UpCall(IDRoom).UpCallParticipants()
		for i in range(len(datas) - 1):
			i += 1
			print(i, datas[i]["nickname"])
		index_of_ = int(input("`masukan nomor user: "))
		user_id = datas[index_of_]["user_id"]
		UpCall(IDRoom).Mute(user_id=user_id)
	elif type_of == "unmute":
		datas = UpCall(IDRoom).UpCallParticipants()
		for i in range(len(datas) - 1):
			i += 1
			print(i, datas[i]["nickname"])
		index_of_ = int(input("`masukan nomor user: "))
		user_id = datas[index_of_]["user_id"]
		UpCall(IDRoom).UnMute(user_id=user_id)
	
def character(stdscr):
	classes = []
	for i in range(0, 13):
		i += 1
		data = Menu[str(i)].title()
		classes.append(data)
	panah = False
	attributes = {}
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	attributes['normal'] = curses.color_pair(1)
	
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
	attributes['highlighted'] = curses.color_pair(2)
	
	c = 0  # last character read
	option = 0  # the current option that is marked
	while c != 10:  # Enter in ascii
	    stdscr.erase()
	    stdscr.addstr("\tCLI Version of WaveRadioBot v.0.5\n\n", curses.A_UNDERLINE)
	    stdscr.addstr("\n-> Tekan `q` untuk keluar\n\n", curses.A_ITALIC)
	    for i in range(len(classes)):
	        if i == option:
	            attr = attributes['highlighted']
	            panah = True
	        else:
	            attr = attributes['normal']
	            panah = False
	        
	        if panah:
	        	stdscr.addstr('\t-> ' + classes[i] + '\n', attr)
	        else:
	        	stdscr.addstr(classes[i] + '\n', attr)
	    c = stdscr.getch()
	    if c == curses.KEY_UP and option > 0:
	        option -= 1
	    elif c == curses.KEY_DOWN and option < len(classes) - 1:
	        option += 1
	    elif c == 113:
	    	return "q"
	    	
	return str(option + 1)

def Banner(whereAt):
	whereAt= whereAt.title()
	os.system('clear')
	print(C.Back.CYAN + (f"CLI Version of WaveRadioBot v.0.5 {whereAt}"))
	print(C.Style.RESET_ALL)

def main():
	Data= {}
	PATH = os.getenv("PATH").split(":")[0]
	config_file= f'{PATH}/.config.json'
	KEY= 'thisismypassword'
	KEYS= 'thisisnotmypassword'
	KEYKEYI= 'noneofthesearemypassword'
	is_exist= os.path.exists(config_file)
	if is_exist:
		file= open(config_file, 'r')
		try:
			USER_CONFIG= json.load(file)
		except JSONDecodeError:
			os.remove(config_file)
			sys.exit(1)
		username= USER_CONFIG['user']['username']
		user_token= USER_CONFIG['refresh_token']
		Authorized = True
		if Authorized:
			while 1:
				x = None
				X = None
				try:
					action = curses.wrapper(character)
					if action == "1":
						i= 0
						Banner(Menu['1'])
						veryLongUrl = input('masukan disini link: ')
						total = input("masukan total taplove: ")
						os.system("clear")
						api = WaveRadio(veryLongUrl, user_token, total)
						Loading = Halo(text=" \rSedang mengirim.. ", placement = "right")
						Loading.start()
						refresh = api.WaveLike()
						Loading.stop()
						data = USER_CONFIG.copy()
						data.update({'refresh_token':refresh})
						writeConfig(data)
					elif action == "2":
						Banner(Menu['2'])
						break
					elif action == "3":
						Banner(Menu['3'])
						veryLongUrl = input('`` masukan disini link : ')
						text = input('`` masukan disini text : ')
						os.system('clear')
						Loading(text="Spamming.. ", placement="right")
						Loading.start()
						api = WaveRadio(veryLongUrl, user_token, total = 0)
						refresh = api.WaveSpam(text=text)
						Loading.stop()
						data = USER_CONFIG.copy()
						data.update({'refresh_token':refresh})
						writeConfig(data)
					elif action == "4":
						Banner(Menu['4'])
						veryLongUrl  = input('`` masukan disini link : ')
						os.system("clear")
						break
					elif action == "5":
						Banner(Menu['5'])
						Loading = Halo(text="Lagi scanning rank.. ", placement="right")
						Loading.start()
						x = Ranking().RankData()
						X = PrettyTable(padding_width=1, border=True)
						X.field_names = ["no","DJ", "Judul", "Like", "Listener"]
						i = 0
						for data in x:
							i+=1
							dj = data['dj']
							listener = data['viewer_count']
							title = data['title']
							like = data['like_count']
							X.add_row([i,dj, title, like, listener])
						sys.stdout.flush()
						print("\n" + X.get_string())
						Loading.stop()
						index_of = int(input("Masukan nomor room: ")) - 1
						IDRoom = x[index_of]['idroom']
						break
					elif action == "6":
						Banner(Menu["6"])
						veryLongUrl = input('`` masukan disini link : ')
						total = input("`` masukan total bot: ")
						os.system('clear')
						api = WaveRadio(veryLongUrl, user_token, total)
						Loading = Halo(text="Bot joining.. ", placement="right")
						Loading.start()
						refresh = api.WaveJoin()
						Loading.stop()
						data = USER_CONFIG.copy()
						data.update({'refresh_token':refresh})
						writeConfig(data)
					elif action == "7":
						Banner(Menu["7"])
						Loading = Halo(text="Lagi scanning rank.. ", placement="right")
						Loading.start()
						x = Ranking().Display()
						print(x)
						Loading.stop()
						break
					elif action == "8":
						Banner(Menu["8"])
						UpCallHandler(type_of="off", username=username)
						
					elif action == "9":
						Banner(Menu["9"])
						UpCallHandler(type_of="on", username=username)
					
					elif action == "10":
						Banner(Menu["10"])
						UpCallHandler(type_of="mute", username=username)
						
					elif action == "11":
						Banner(Menu["11"])
						UpCallHandler(type_of="unmute", username=username)
						
					elif action == "12":
						Banner(Menu["12"])
						UpCallHandler(type_of="accept", username=username)
						
					elif action == "13":
						Banner(Menu["13"])
						UpCallHandler(type_of="kick", username=username)
						
					elif action == 'q':
						os.system("clear")
						print("thanks!")
						break
					else:
						os.system("clear")
				except KeyboardInterrupt:
					sys.exit(main())
				except Exception as er:
					print(er)
					input()
					if 'list index out of range' in str(er):
						break
					else:
						print(F.RED + "ERROR:" + DEFAULT, er)
		elif user_token == None:
			print(F.RED + 'Hubungi Author.' + DEFAULT)
			os.remove(config_file)
		else:
			pass
	elif not is_exist:
		try:
			x= input('`` masukan username: ')
			p= getpass.getpass('`` masukan pin: ')
			config = {
				'info': {
					'device': {}, 
					'browser': {}, 
					'user_agent': ''
				}, 
				'user': {
					'username':x, 
					'pin':p, 
					'status': 1, 
					'last_confirmed': '',
					'tool_version': '0.5.0'
				}, 
				'refresh_token': '', 
				'exp': 1637046427
			}
			os.system('clear')
			Loading = Halo(text = "Lagi nunggu token.. ", placement = "right")
			webbrowser.open(wavemanager + 'login')
			r = requests.put(wavemanager + 'get_token', json=config)
			assert r.status_code == 201,''
			os.system("clear")
			Loading.start()
			refresh_token = input()
			Loading.stop()
			config['refresh_token'] = refresh_token
			writeConfig(config)
			print(F.GREEN + '`` Silahkan Jalankan Ulang Skrip, setelah terkonfirmasi.' + DEFAULT)
		except AssertionError:
			print(F.RED + '`` Hubungi Author.' + DEFAULT)
		except Exception as e:
			print(e)