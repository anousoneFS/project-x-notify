from threading import Thread
import time
import pyrebase
from app import NotifyToLineChatbot

_db = pyrebase.initialize_app(
    {
        "apiKey": "AIzaSyDr0UwYjDiVbU_6T7VdrEtlcGdV4PIVRdI",
        "authDomain": "project-x-23d73.firebaseapp.com",
        "databaseURL": "https://project-x-23d73-default-rtdb.firebaseio.com",
        "projectId": "project-x-23d73",
        "storageBucket": "project-x-23d73.appspot.com",
        "messagingSenderId": "240804399954",
        "appId": "1:240804399954:web:4984d9076e156654a1888b",
        "measurementId": "G-HK4GEQL712"

    }
).database()

allData = []
global num
num = 0
def stream_handler(message):
    print("Got some update from the Firebase")
    # We only care if something changed
    if message["event"] in ("put", "patch"):
        print("Something changed")
        if message["path"] == "/":
            print(
                "Seems like a fresh data or everything have changed, just grab it!"
            )
            # self.my_stuff: List[dict] = message["data"]
            dataSplit = str(message['data']).split(',')
            print(f'data split = {dataSplit}')
            allData.append(message["data"])
            print(allData)

            date = dataSplit[0]
            temp = dataSplit[1]
            humid = dataSplit[2]
            ph = dataSplit[3]
            ec = dataSplit[4]
            temp_water = dataSplit[5]
            light = dataSplit[6]

            data = "{\"time\":" + "\"" + date + "\"" + ", \"temp\": " + "\"" + str(
                temp) + "\"" + ", \"humid\": " + "\"" + str(humid) + "\"" + ",\"ph\":" + "\"" + str(ph) + "\"" + ",\"light\":" + "\"" + str(light) + "\"" + ",\"ec\":" + "\"" + str(ec) + "\"" + ",\"temp_water\":" + "\"" + str(temp_water) + "\""+"}"

            mypath = 'sensor-values2/' + date.split(' ')[0]
            _db.child(mypath).push(data)

            if int(dataSplit[1]) > maxTempAir:
                print(f'ຕອນນີ້ອຸນຫະພູມອາກາດໄດ້ສູງກວ່າ {maxTempAir} ອົງສາ ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ອຸນຫະພູມອາກາດໄດ້ສູງກວ່າ {maxTempAir} ອົງສາ ແລ້ວ!!!')
            
            if int(dataSplit[2]) > maxHumid:
                print(f'ຕອນນີ້ຄວາມຊຸມສູງກວ່າ {maxHumid} % ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄວາມຊຸມສູງກວ່າ {maxHumid} % ແລ້ວ!!!')

            if int(dataSplit[3]) > maxPh:
                print(f'ຕອນນີ້ຄ່າ PH ໄດ້ສູງກວ່າ {maxPh} ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າ PH ໄດ້ສູງກວ່າ {maxPh} ແລ້ວ!!!')

            if int(dataSplit[4]) > maxEc:
                print(f'ຕອນນີ້ຄ່າ EC ໄດ້ສູງກວ່າ {maxEc} ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າ EC ໄດ້ສູງກວ່າ {maxEc} ແລ້ວ!!!')

            if int(dataSplit[5]) > maxTempWater:
                print(f'ຕອນນີ້ອຸນຫະພູມນໍ້າໄດ້ສູງກວ່າ {maxTempWater} ອົງສາ ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ອຸນຫະພູມນໍ້າໄດ້ສູງກວ່າ {maxTempWater} ອົງສາ ແລ້ວ!!!')

            if int(dataSplit[6]) > maxLight:
                print(f'ຕອນນີ້ຄ່າແສງແດດໄດ້ສູງກວ່າ {maxLight} Lux ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າແສງແດດໄດ້ສູງກວ່າ {maxLight} Lux ແລ້ວ!!!')
        # =====================================================================
            if int(dataSplit[1]) < minTempAir:
                print(f'ຕອນນີ້ອຸນຫະພູມອາກາດໄດ້ຕໍ່າກວ່າ {minTempAir} ອົງສາ ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ອຸນຫະພູມອາກາດໄດ້ຕໍ່າກວ່າ {minTempAir} ອົງສາ ແລ້ວ!!!')
            
            if int(dataSplit[2]) < minHumid:
                print(f'ຕອນນີ້ຄວາມຊຸມຕໍ່າກວ່າ {minHumid} % ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄວາມຊຸມຕໍ່າກວ່າ {minHumid} % ແລ້ວ!!!')

            if int(dataSplit[3]) < minPh:
                print(f'ຕອນນີ້ຄ່າ PH ໄດ້ຕໍ່າກວ່າ {minPh} ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າ PH ໄດ້ຕໍ່າກວ່າ {minPh} ແລ້ວ!!!')

            if int(dataSplit[4]) < minEc:
                print(f'ຕອນນີ້ຄ່າ EC ໄດ້ຕໍ່າກວ່າ {minEc} ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າ EC ໄດ້ຕໍ່າກວ່າ {minEc} ແລ້ວ!!!')

            if int(dataSplit[5]) < minTempWater:
                print(f'ຕອນນີ້ອຸນຫະພູມນໍ້າໄດ້ຕໍ່າກວ່າ {minTempWater} ອົງສາ ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ອຸນຫະພູມນໍ້າໄດ້ຕໍ່າກວ່າ {minTempWater} ອົງສາ ແລ້ວ!!!')

            if int(dataSplit[6]) < minLight:
                print(f'ຕອນນີ້ຄ່າແສງແດດໄດ້ຕໍ່າກວ່າ {minLight} Lux ແລ້ວ!!!')
                NotifyToLineChatbot(f'ຕອນນີ້ຄ່າແສງແດດໄດ້ຕໍ່າກວ່າ {minLight} Lux ແລ້ວ!!!')


        else:
            print(
                "1 => Something updated somewhere, I dont't care I just want the latest snapshot of my stuff"
            )

def getSettingData(message):
    settingData = []
    global maxTempAir
    global maxEc
    global maxPh
    global maxTempWater
    global maxHumid
    global maxLight
    global minTempAir
    global minEc
    global minPh
    global minTempWater
    global minHumid
    global minLight
    print("Got some update from the Firebase")
    # We only care if something changed
    if message["event"] in ("put", "patch"):
        print("Something changed")
        if message["path"] == "/":
            print(
                "Seems like a fresh data or everything have changed, just grab it!"
            )
            # self.my_stuff: List[dict] = message["data"]
            data = message['data']
            print(f'setting data = {data}')
            settingData.append(data)
            print(settingData)

            maxTempAir = int(data['maxTempAir'])
            maxHumid = int(data['maxHumid'])
            maxEc = int(data['maxEc'])
            maxPh = int(data['maxPh'])
            maxTempWater = int(data['maxTempWater'])
            maxLight = int(data['maxLight'])
            minTempAir = int(data['minTempAir'])
            minTempWater = int(data['minTempWater'])
            minEc = int(data['minEc'])
            minPh = int(data['minPh'])
            minLight = int(data['minLight'])
            minHumid = int(data['minHumid'])

        elif message['path'] == '/maxTempWater':
            data = message['data']
            print(data)
            maxTempWater = int(data)
        elif message['path'] == '/maxHumid':
            data = message['data']
            print(data)
            maxHumid = int(data)
        elif message['path'] == '/maxPh':
            data = message['data']
            print(data)
            maxPh = int(data)
        elif message['path'] == '/maxEc':
            data = message['data']
            print(data)
            maxEc = int(data)
        elif message['path'] == '/maxTempAir':
            data = message['data']
            print(data)
            maxTempAir = int(data)
        elif message['path'] == '/maxLight':
            data = message['data']
            print(data)
            maxLight = int(data)
        # ===========================================
        elif message['path'] == '/minTempWater':
            data = message['data']
            print(data)
            minTempWater = int(data)
        elif message['path'] == '/minHumid':
            data = message['data']
            print(data)
            minHumid = int(data)
        elif message['path'] == '/minPh':
            data = message['data']
            print(data)
            minPh = int(data)
        elif message['path'] == '/minEc':
            data = message['data']
            print(data)
            minEc = int(data)
        elif message['path'] == '/minTempAir':
            data = message['data']
            print(data)
            minTempAir = int(data)
        elif message['path'] == '/minLight':
            data = message['data']
            print(data)
            minLight = int(data)


        else:
            print(
                "1 => Something updated somewhere, I dont't care I just want the latest snapshot of my stuff"
            )

_db.child('setting').stream(getSettingData)
time.sleep(3)
_db.child('data_sensor_from_arduino/data_from_arduino').stream(stream_handler)