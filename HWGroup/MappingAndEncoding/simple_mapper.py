from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import encoder
import Node

# if modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# This is for Brian's spreadsheet
# Sheet1 is set like [id, id_to_left, id_to_right, id_to_front, id_to_behind]
# Sheet2 is set like [id, x, y]
SPREADSHEET_ID = '1M31oyvu16W-2ndPq3pRrzKlIovIwu7DrmkOp9jvZA74' # This is for Brian's spreadsheet, make your own
GET_RANGE = 'Sheet1!A2:E150'
SET_RANGE = 'Sheet2!A2:C201'
    
def main():
    #################################################################################################
    # NOTE ! You need a credentials.json https://developers.google.com/sheets/api/quickstart/python #
    #################################################################################################

    # connect to the google sheet
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token, encoding="latin1")
            # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=GET_RANGE).execute()
    values = result.get('values', [])

    map = [None] * len(values)
    grid = ""
    
#    print(len(map))
    
    if not values:
        print('No data found.')
    else:
        for row in values:
            # rows on gSheets are [id, id_to_left, id_to_right, id_to_front, id_to_behind]
            for i in range(len(row)):
                # user didn't have a neighbor, reformat entry
                if row[i] is u'':
                    row[i] = None
                else:
                    row[i] = int(row[i])
                if len(row) is 4:
                    row.append(None)
            n = row[0]
            # create Node in map initialized to the student's id
            map[n] = Node(n)
            map[n].l = row[1]
            map[n].r = row[2]
            map[n].u = row[3]
            map[n].d = row[4]

    edge_map = [None] * len(values)
     
    # find the top left corner
    n = int(len(map)/2)
    while map[n].u is not None or map[n].l is not None:
        if map[n].u is not None:
            n = map[n].u
        if map[n].l is not None:
            n = map[n].l

    # construct a grid moving from the top left corner
    cur_x = 0
    cur_y = 0
    while True:
        while map[n].r is not None:
            map[n].x = cur_x
            map[n].y = cur_y
            cur_x = cur_x + 1
            grid = grid + str(n) + ' '
            n = map[n].r

        map[n].x = cur_x
        map[n].y = cur_y
        cur_x = 0
        cur_y = cur_y + 1
        
        grid = grid + str(n) + '\n'
        
        if map[n].d is not None:
            n = map[n].d
            while map[n].l is not None:
                n = map[n].l
        else:
            break    

    # construct coords for updating the google sheet
    coords = [None] * len(map)
    for i in range(len(map)):
        coords[i] = [i, map[i].x, map[i].y]

#    print(coords)

#    messages = encodeMessages(map)

#   update the google sheet to have the current positions of people
    body = {'range':SET_RANGE, 'values':coords}
    ret = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                range=SET_RANGE, body=body,
                                valueInputOption='RAW').execute()
#    print(ret.toString())

#    decodeMessages(messages)
    
if __name__ == '__main__':
    main()