import pyrebase
from app import NotifyToLineChatbot
from threading import Thread

class MyStuffTracker(Thread):
    """Tracks changes of my stuff in Firebase"""

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

    my_stuff = []

    global maxPh
    global maxEc
    global maxHumid
    global maxTempAir
    maxPh = 7
    maxEc = 3
    maxHumid = 80
    maxTempAir = 38

    def __init__(self):
        """Start tracking my stuff changes in Firebase"""
        Thread.__init__(self)
        self._db.child("data_sensor_from_arduino/data_from_arduino").stream(self.stream_handler)
    
    @property
    def is_ready(self) -> bool:
        """
        Returns:
            bool: True if my stuff is ready for use
        """
        return len(self.my_stuff) != 0

    def stream_handler(self, message):
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
                self.my_stuff.append(message["data"])
                print(self.my_stuff)


                print(f'max temp air = {maxTempAir} and humid = {maxHumid}')

                if int(dataSplit[1]) > maxTempAir:
                    print('ອຸນຫະພູມສູງເກີນ 1 ອົງສາ')
                    NotifyToLineChatbot('ອຸນຫະພູມໃນໂຮງເຮືອນສູງເກີນ 1 ອົງສາ')
                
                if int(dataSplit[2]) > maxHumid:
                    print(f'ຄວາມຊຸມສູງເກີນ')
                    NotifyToLineChatbot('ຄວາມຊຸມໃນໂຮງເຮືອນສູງເກີນໄປ')

            else:
                print(
                    "1 => Something updated somewhere, I dont't care I just want the latest snapshot of my stuff"
                )


class GetSettingData(Thread):
    """Tracks changes of my stuff in Firebase"""

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

    settingData = []

    def __init__(self):
        """Start tracking my stuff changes in Firebase"""
        Thread.__init__(self)
        self._db.child("setting").stream(self.stream_handler)
    
    @property
    def is_ready(self) -> bool:
        """
        Returns:
            bool: True if my stuff is ready for use
        """
        return len(self.settingData) != 0

    def stream_handler(self, message):
        print("Got some update from the Firebase")
        # We only care if something changed
        if message["event"] in ("put", "patch"):
            print("Something changed")
            if message["path"] == "/":
                print(
                    "Seems like a fresh data or everything have changed, just grab it!"
                )
                # self.my_stuff: List[dict] = message["data"]
                print(f'===> data setting = {message["data"]}')
                self.settingData.append(message["data"])
                print(self.settingData)

            elif message["path"] == "/maxPh":
                print(message['data'])
            elif message["path"] == "/maxHumid":
                print(message['data'])
                
            elif message["path"] == "/maxTempAir":
                print(message['data'])

            else:
                print(
                    "2 => Something updated somewhere, I dont't care I just want the latest snapshot of my stuff"
                )

    

tracker = MyStuffTracker()

while not tracker.is_ready:
    pass  # Just wait until the first snapshot of my stuff will be ready
print(f"My stuff is = {tracker.my_stuff}")

getSettingData = GetSettingData()

while not getSettingData.is_ready:
    pass
print(f'my setting data = {getSettingData.settingData}')
