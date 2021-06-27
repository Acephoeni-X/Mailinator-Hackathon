import json, os
import datetime
from datetime import datetime
import re

def sendCron():
    time_now = datetime.time(datetime.now())
    time_now = re.findall("\d\d:\d\d:\d\d", str(time_now))[0]
    # print(type(time_now))
    todaY = ['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday','Sunday']
    todaY = todaY[datetime.today().weekday()]
    # print(todaY)
    with open ('data.json', 'r') as f:
        data = json.loads(f.read())
        data = data['datas']
        
        for data in data:
            try:
                if (data['time'] == time_now and data['day'] == todaY):
                    os.rename(f'{data["sender"]}.pickle', 'token_gmail_v1.pickle')
                    from appone import sendmail
                    sendmail.sendMail(data['to'], data['subject'], data['message'])
                    os.rename('token_gmail_v1.pickle',f'{data["sender"]}.pickle')
            except:
                continue

if __name__ == '__main__':
    print('Started')
    while True:
        sendCron()
        # break
