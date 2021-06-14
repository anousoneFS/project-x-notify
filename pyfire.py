import pyrebase
from app import NotifyToLineChatbot


class MyStuffTracker(object):
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

    # my_stuff: list[dict] = None  # In my example my data is a list of some dictionaries
    my_stuff = []

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
                self.my_stuff.append(message["data"])
                print(self.my_stuff)

                if message["data"] > 38:
                    print('ອຸນຫະພູມສູງເກີນ 38 ອົງສາ')
                    NotifyToLineChatbot('ອຸນຫະພູມໃນໂຮງເຮືອນສູງເກີນ 38 ອົງສາ')

            else:
                print(
                    "Something updated somewhere, I dont't care I just want the latest snapshot of my stuff"
                )
                # Just get whole-data of my stuff and list (second) item of the pyres (that I expect to be a dict)
                # self.my_stuff: List[dict] = list(
                # it.item[1] for it in self._db.child("my_stuff").get().pyres
                # )

    def __init__(self) -> None:
        """Start tracking my stuff changes in Firebase"""
        super().__init__()
        self._db.child("data_sensor_from_arduino/data_from_arduino").stream(self.stream_handler)


tracker = MyStuffTracker()

while not tracker.is_ready:
    pass  # Just wait until the first snapshot of my stuff will be ready


print(f"My stuff is = {tracker.my_stuff}")
