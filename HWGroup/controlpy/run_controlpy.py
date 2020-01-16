#Note for this to be able to run on school wifi, this needs to be on a vpn

#All this is is a simple webserver that will:
#Take the input google forms
#Display what everyone's assigned role and seat number is
#For debugging purposes, have the clients ack back.
#This will likely not be used in production


#pip install gspread
#pip install oauth2client
#pip install flask-bootstrap

from __future__ import print_function
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pandas as pd
import json
import numpy as np
from flask import Flask, request, jsonify
from flask import render_template
from flask_bootstrap import Bootstrap

from BLE.BLE import broadcast_setup, broadcast

#Will use bootstrap for frontend

#Structure of a BLE packet to send when broadcasting:
#

broadcast_setup()

def process_loc(sync_loc):
	temp_str = sync_loc
	temp_str = temp_str.replace('Sync_', '')
	at_index = temp_str.find('at')
	role_id = temp_str[0:at_index]
	row_col = temp_str[at_index + 2:len(temp_str)]

	#print(row_col)
	comma_index = row_col.find(',')
	row = row_col[0:comma_index]
	col = row_col[comma_index:len(row_col)]

	return role_id, row, col

app = Flask(__name__)
Bootstrap(app)

def format_ble_message(row, col, id, mode):
	#Row, Columns are 8 bit unsigned numbers
	row = np.uint8(row)
	col = np.uint8(col[1:])
	id = np.uint8(id) # Check to see how many people are going to this thing...
	mode = np.uint8(mode)
	#_array = np.array(([row, col, id, mode]), dtype=np.uint8)
	_bytes = bytearray([row, col, id, mode])
	print(_bytes)
	return str(_bytes)
	#Mode is the type of image being displayed.

def pack_ble_messages_syncall(pandas_dataframe):
	ble_list = []
	for index, row_iter in pandas_dataframe.iterrows():
		#print(row_iter['row'])
		#print(row_iter)
		row = np.uint8(row_iter['row'])
		col = np.uint8(row_iter['col'])
		role_id = np.uint8(row_iter['role_id'])
		mode = np.uint8(0)
		ble_list.extend([row, col, role_id, mode])
	print(ble_list)
	_bytes = bytearray(ble_list)
	print(_bytes)
	return str(_bytes)

def _init():

	SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
	SECRETS_FILE = "API_key.json"
	SPREADSHEET = "EE180DA Google Sheet"

	json_key = json.load(open(SECRETS_FILE))
	# Authenticate using the signed key
	credentials = SignedJwtAssertionCredentials(json_key['client_email'],
												json_key['private_key'], SCOPE)
	gc = gspread.authorize(credentials)
	#Get google sheets information, which is passed from the google form
	
	#print("The following sheets are available")
	for sheet in gc.openall():
		print("{} - {}".format(sheet.title, sheet.id))


	workbook = gc.open(SPREADSHEET)
	sheet = workbook.sheet1

	#We now have our row, column, and role_index of each person!
	data = pd.DataFrame(sheet.get_all_records())
	column_names = {'What role number (printed label) on your Raspberry Pi do you have?': 'role_id',
				'What row number are you in, from front to back, starting from 0? (MAKE SURE TO COUNT CLOSELY)': 'row',
				'What column number are you in, from left to right, starting from 0? (MAKE SURE TO COUNT CLOSELY)': 'col',
				}

	data.rename(columns=column_names, inplace=True)
	#data.timestamp = pd.to_datetime(data.timestamp)
	#print(data)
	data.drop_duplicates(subset='role_id', keep='first', inplace=False)
	return data

@app.route("/", methods = ['POST', 'GET'])
def hello():
	data = _init()
	container = """<div class="container">\n\t{}
	</div>
	"""
	rows = ""
	row_num = 0
	max_row = data["row"].max()
	max_col = data["col"].max()
	#print("max_row: " + str(max_row) + "max_col: " + str(max_col))
	#TODO: Bugfix this to have a container that isnt completely empty!
	for row in range(0, max_row + 1):
		#print(row)
		rows += """ <div class="row"> \n\t {} \n\t </div> """
		col_num = 0
		_row = ""
		for col in range(0, max_col + 1):
			sub_data = data.loc[(data["col"] == col_num) & (data["row"] == row_num)]
			#print(sub_data)
			#timestamp = sub_data["timestamp"]
			if sub_data.empty:
				#_row.format("(Row, Col) = (" + str(row) + " , " + str(col) + " )")
				_row += """<div class="col"> Empty </div>\n"""
				#print("Entered!")
			else:
				_row += """<div class="col"> {} </div>\n"""
				str_subdata = str(sub_data)
				#print(_row)
				#print(str(sub_data['role_id'])[2:26])
				role_id = str(sub_data['role_id'])[4:8].strip()
				#_row = _row.format("\n\t<div>(Row, Col) = (" + str(row_num) + " , " + str(col_num) + " )" + "<br>role_id: " + str(sub_data['role_id'])[4:8].strip() + "</div>{}")

				#Add a new line for a button
				button = ("""\n\t<form action="" method = "post">
					<input type = "submit" class="btn btn-primary btn-lg" name = "SyncBtn" value="Sync_{}" role="button"><br/>\n
					</form>""")

				button = button.format(str(role_id) + "at" + str(row_num) + "," + str(col_num))

				_row = _row.format(button)
				#print("_row: " + str(_row))
				#print("_button: " + str(button))
				#row.format(str_subdata)
				#rows.format(row_num)

				if request.method == 'POST':
					sync_loc = request.form.get('SyncBtn')
					#print(sync_loc)
					if sync_loc == "SyncAll":
						print('SyncAll')
						#TODO: Send RESYNC All, retry twice!
						ble_msg = pack_ble_messages_syncall(data)
						broadcast(ble_msg)
					else:
						this_role, this_row, this_col = process_loc(sync_loc)
						print(str(this_row))
						ble_msg = format_ble_message(this_row, this_col, this_role, 0) #Assuming only one image displaying
						broadcast(ble_msg)
						#TODO: Send BLE command that sends the row and column to the role id

			col_num += 1
		#print(rows)
		#print(_row)
		rows = rows.format(_row)
		row_num += 1
	container = container.format(rows)
	#print(str(container))
	return render_template("template.html", data_content=container)

if __name__ == "__main__":
	#data = _init()
	#a = hello()
	#app = Flask(__name__)
	#Bootstrap(app)
	app.run(debug=True)