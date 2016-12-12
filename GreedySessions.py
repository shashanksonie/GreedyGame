import json,mysql.connector,sys
from datetime import datetime


MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'test'
MYSQL_USER = 'root'
MYSQL_PASS = 'shashanksoni'

cnx = mysql.connector.connect(host=MYSQL_HOST,database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASS)
cursor = cnx.cursor()

log = open ("ggevent.log","r")

active_seesion = {}

def insert(game_id,ai5,start_time,stop_time,session_time,validity):
	query = ("""
		INSERT INTO greedy (game_id,ai5,start_time,stop_time,session_time,validity) VALUES (%s,%s,%s,%s,%s,%s)
		""")
	cursor.execute(query,(game_id,ai5,start_time,stop_time,session_time,validity))
	cnx.commit()


for line in log:
	x =  json.loads(line)
	# if x['headers']['ai5'] == 'e8288d45e9efa574b3ae922ba218bc3d':
	key = x['bottle']['game_id']+x['headers']['ai5']
	if key not in active_seesion:
		if x['post']['event'] == 'ggstart':
			active_seesion[key] = {}
			# print 'Entered First time in Active with ggstart ' , x['bottle']['timestamp']
			active_seesion[key]['ggstart'] = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
		else:
			# print 'STOP W Start ', x['bottle']['game_id'], ' -> ' , x['post']['event'] ,' -> ' , x['bottle']['timestamp'] , x['headers']['ai5']
			pass
	else :
		if 'ggstop' not in active_seesion[key].keys():
			if x['post']['event'] == 'ggstop':
				t2 = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
				t1 = active_seesion[key]['ggstart']
				active_seesion[key]['ggstop'] = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
				active_seesion[key]['time'] = (t2-t1).total_seconds()
				# print 'Entered First Time in Active with ggstop' , x['bottle']['timestamp']
			else:
				# print 'START W Stop ', x['bottle']['game_id'], ' -> ' , x['post']['event'] ,' -> ' , x['bottle']['timestamp'] , x['headers']['ai5']	
				pass
		else:
			if 'ggstartA' not in active_seesion[key].keys():
				if x['post']['event'] == 'ggstart':
					startA = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
					diff = (startA-active_seesion[key]['ggstop']).total_seconds()
					if diff > 30:
						print 'Session Time for device ', x['headers']['ai5'], ' playing game ', x['bottle']['game_id'] , 'is between ' , active_seesion[key]['ggstart'] ,' and ', active_seesion[key]['ggstop'] , 'i.e.', active_seesion[key]['time']
						valid = 1 if active_seesion[key]['time'] > 60 else 0
						insert(x['bottle']['game_id'],x['headers']['ai5'],active_seesion[key]['ggstart'],active_seesion[key]['ggstop'],active_seesion[key]['time'],valid)
						active_seesion.pop(key,'None')
						# print 'Entered First time in Active with ggstart ' , x['bottle']['timestamp']
						active_seesion[key] = {}
						active_seesion[key]['ggstart'] = startA
					else:
						# print 'Entered in Active with ggstartA' , x['bottle']['timestamp']
						active_seesion[key]['ggstartA'] = startA
				else:
					# print 'STOP W Start ', x['bottle']['game_id'], ' -> ' , x['post']['event'] ,' -> ' , x['bottle']['timestamp'] , x['headers']['ai5']
					pass
			else:
				if x['post']['event'] == 'ggstop':
					tx = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
					ty = active_seesion[key]['ggstartA']
					active_seesion[key]['time'] = active_seesion[key]['time'] + (tx-ty).total_seconds()
					# print 'Updating ggstop in Active from' , active_seesion[key]['ggstop'], 'to this ' , x['bottle']['timestamp']
					active_seesion[key]['ggstop'] = tx
					active_seesion[key].pop('ggstartA','None')
				else:
					startA = datetime.strptime(x['bottle']['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
					diff = (startA-active_seesion[key]['ggstop']).total_seconds()
					if diff > 30:
						print 'Session Time for device ', x['headers']['ai5'], ' playing game ', x['bottle']['game_id'] , 'is between ' , active_seesion[key]['ggstart'] ,' and ', active_seesion[key]['ggstop'] , 'i.e.', active_seesion[key]['time']
						valid = 1 if active_seesion[key]['time'] > 60 else 0
						insert(x['bottle']['game_id'],x['headers']['ai5'],active_seesion[key]['ggstart'],active_seesion[key]['ggstop'],active_seesion[key]['time'],valid)
						active_seesion.pop(key,'None')
						# print 'Entered First time in Active with ggstart ' , x['bottle']['timestamp']
						active_seesion[key] = {}
						active_seesion[key]['ggstart'] = startA
					else:
						# print 'Updating ggstartA in Active from' , active_seesion[key]['ggstartA'], 'to this ' , x['bottle']['timestamp']
						active_seesion[key]['ggstartA'] = startA

for key in active_seesion:
	if 'ggstop' in active_seesion[key].keys():
		print 'Session Time for device ', x['headers']['ai5'], ' playing game ', x['bottle']['game_id'] , 'is between ' , active_seesion[key]['ggstart'] ,' and ', active_seesion[key]['ggstop'] , 'i.e.', active_seesion[key]['time']
		valid = 1 if active_seesion[key]['time'] > 60 else 0
		insert(x['bottle']['game_id'],x['headers']['ai5'],active_seesion[key]['ggstart'],active_seesion[key]['ggstop'],active_seesion[key]['time'],valid)			

