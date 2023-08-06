import os
import uuid
import time
import logging
import requests
import secrets
import icecream
import pause
import json
from colorama import Fore as F
from icecream import ic as ICE
from prettytable import PrettyTable
from waveradio.conf import wave_token

H  = {
	'Host':'api.wave.com.tw',
	'version':'5.6.2(575)',
	'devicetype':'Android',
	'language':'en',
	'deviceid':secrets.token_hex(7),
	'appsflyeruid':'1628801704343-6452787816854394803',
	'advertisingid':secrets.token_hex(16),
	'region':'ID',
	'authorization':wave_token,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/4.5.0'
}
def SearchUser(nickname: str):
	Datas= []
	try:
		baseUrl = "https://api.wave.com.tw/v1/users/?cursor=&q=" + nickname
		req = requests.get(baseUrl, headers=H)
		X = PrettyTable(padding_width=1, border=True)
		X.field_names = ["No", "DJ", "FAN", "FOL", "UID"]
		c = 0
		return req.text
		for i in req.json()['data']:
			c += 1
			nickname = i['name']
			uid = i['id']
			description = i['description']
			followers = i['follower_count']
			followings = i['following_count']
			profile_pic = i['avatar_url']
			X.add_row([c, nickname, followers, followings, uid[:5]])
		return X.get_string()
	except KeyError:
		return X
	except Exception as er:
		return er

def EndLive(IDRoom: str):
	try:
		r= requests.delete('https://api.wave.com.tw/api/v1/lives/'+ IDRoom + '?reason=1', headers=H)
		assert r.status_code== 200, ''
		return True, r.text
	except AssertionError:
		return False, r.text
		
def writeConfig(data: dict):
	PATH = os.getenv("PATH").split(":")[0]
	with open(f'{PATH}/.config.json', 'w') as f:
		json.dump(data,f)
		
	return True
	
class Ranking:
	def __init__(self):
		self.datas = []
	def Rank(self, cursor: str=""):
		try:
			BASE_URL = f"https://api.wave.com.tw/api/v1/lives?category_id=&cursor={cursor}&sort_by=female_first"
			r = requests.request('GET', BASE_URL, headers=H)
			cursor = r.json()['cursor']
			for i in range(len(r.json()['data'])):
				IDRoom = r.json()['data'][i]['id']
				streamer = r.json()['data'][i]['streamer']['name']
				like_count = r.json()['data'][i]['like_count']
				title = r.json()['data'][i]['title']
				viewer = r.json()['data'][i]['now_viewer_count']
				is_upcall = r.json()['data'][i]['groupcall']
				profile_pic = r.json()['data'][i]["streamer"]["avatar_url"]
				if is_upcall != None:
					is_upcall = True
				data = {
					"idroom":IDRoom,
					"dj":streamer,
					"title":title,
					"like_count":like_count,
					"viewer_count":viewer,
					"profile_pic":profile_pic,
					"on_mic":is_upcall
				}
				self.datas.append(data)
			return cursor
		except KeyError:
			pass
		except Exception as e:
			pass
			
	def RankData(self):
		req = self.Rank(cursor="")
		while req !="":
			req = self.Rank(req)
		return self.datas
		
	def Display(self):
		data = self.RankData()
		X = PrettyTable(padding_width=1, border=True)
		X.field_names = ["No", "DJ", "TTL", "LST", "LKE"]
		
		i=0
		for d in data:
			i+=1
			nickname = d['dj']
			title = d['title']
			listener = d['viewer_count']
			like = d['like_count']
			X.add_row([i, nickname, title, listener, like])
		return X.get_string()
		
class WaveRadio:
	HOST = "https://wavemanager.herokuapp.com/v5/"
	def __init__(self, veryLongUrl: str, token: str, total: str):
		self.token = token
		self.total = total
		self.veryLongUrl = veryLongUrl
		self.cut_ = self.veryLongUrl.split("=")[3]
		self.IDRoom = self.cut_.split('&')[0]
	def WaveLike(self):
		data = {
			"token":self.token,
			"total":self.total
		}
		r = requests.post(self.HOST + "like/" + self.IDRoom, json=data)
		assert r.status_code == 200,''
		refresh_token = r.json()['refresh_token']
		return refresh_token

	def WaveJoin(self):
		data = {
			"token":self.token,
			"total":self.total
		}
		r = requests.post(self.HOST + "join/" + self.IDRoom, json=data)
		assert r.status_code == 200,''
		refresh_token = r.json()['refresh_token']
		return refresh_token
		
	def WaveSpam(self, text: str):
		data = {
			"token":self.token,
			"total":self.total, 
			"text":text
		}
		r = requests.post(self.HOST + "spam/" + self.IDRoom, json=data)
		assert r.status_code == 200,''
		refresh_token = r.json()['refresh_token']
		return refresh_token

class UpCall:
	def __init__(self, IDRoom: str):
		self.datas = []
		self.data_dict = {}
		self.IDRoom = IDRoom
		self.Header = H
	def UpCallParticipants(self):
		r = requests.get('https://api.wave.com.tw/api/v1/lives/' + self.IDRoom, headers=self.Header).json()
		for data in r["groupcall"]["seats"]:
			try:
				if data["status"] != 0:
					data_dict = {} 
					nickname = data["user"]["name"]
					user_id = data["user"]["id"]
					data_dict["nickname"] = nickname
					data_dict["user_id"] = user_id
					self.datas.append(data_dict)
			except TypeError:
				pass
			except Exception as e:
				ICE()
				ICE(e)
		return self.datas
	
	def Mute(self, user_id: str):
		r = requests.post('https://api.wave.com.tw/api/v1/lives/'+ self.IDRoom +'/groupcall/users/' + user_id + '/mute', headers=self.Header)
		return r.status_code
	
	def UnMute(self, user_id: str):
		r = requests.delete('https://api.wave.com.tw/api/v1/lives/' + self.IDRoom + '/groupcall/users/' + user_id + '/unmute', headers=self.Header)
		return r.status_code
		
	def LeaveCall(self, user_id: str):
		r = requests.post('https://api.wave.com.tw/api/v1/lives/'+self.IDRoom+'/groupcall/leave', headers=self.Header,json={"user_id":user_id})
		return r.status_code
		
	def AcceptAllRequest(self):
		r = requests.get('https://api.wave.com.tw/api/v1/lives/'+self.IDRoom+'/groupcall/queue?cursor=',headers=self.Header)
		if int(r.json()["total"]) >= 1:
			for i in range(int(r.json()["total"])):
				user_id = r.json()['data'][i]['id']
				req = requests.post('https://api.wave.com.tw/api/v1/lives/'+self.IDRoom+'/groupcall/accept',headers=self.Header,json={"user_id":user_id})
		return r.status_code
		
	def OffCall(self):
		r = requests.patch('https://api.wave.com.tw/api/v1/lives/'+self.IDRoom,headers=self.Header,json={'mode':0})
		return r.status_code
		
	def OnCall(self):
		r = requests.patch('https://api.wave.com.tw/api/v1/lives/'+self.IDRoom, headers=self.Header, json={'mode':1})
		return r.status_code