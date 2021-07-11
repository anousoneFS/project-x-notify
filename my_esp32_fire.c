#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>

#define PUMP_PIN 18   // ກຳນົດຂາ 18 ເປັນຂາຄວບຄຸມປໍ້ານໍ້າ(ປ່ອຍໄຟອອກ)

#define FIREBASE_HOST "<Something>.firebaseio.com"
#define FIREBASE_AUTH "<Token or Secret>"
#define WIFI_SSID "<YOU WIFI NAME>"
#define WIFI_PASSWORD "<YOU WIFI PASSWORD>"

// void setup() ເປັນສ່ວນທີ່ code ຈະລັນພຽງແຕ່ຄັ້ງດຽວເທົ່ານັ້ນ ເວລາເປີດໃຊ້ລະບົບ
void setup() {
  pinMode(PUMP_PIN, OUTPUT);
  
  Serial.begin(115200);

  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  // initialize firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  // ທຳການ stream ເອົາຂໍ້ມູນຈາກ firebase ທຸກຄັ້ງທີຂໍ້ມູນຈາກ firebase
  // ໃນ path arduino_streaming ມີການປ່ຽນແປງຈາກເລກ 0 ເປັນເລກ 1 ປໍ້ານໍ້າຈະເປີດທັນທີ
  Firebase.stream("arduino_streaming/", [](FirebaseStream stream) {
    Serial.println("Evant: " + stream.getEvent());
    Serial.println("Path: " + stream.getPath());
    Serial.println("Data: " + stream.getDataString());
    // ທຳການເຊັກວ່າຂໍ້ມູນຈາກ firebase ມີການອັບເດດ ຫຼື ບໍ່
    if (stream.getEvent() == "put") {
      if (stream.getPath() == "/") {
        // ຄຳສັ່ງສຳຫຼັບເປີດ - ປິດ ປໍ້ານໍ້າ ( 0 ຄືປິດ ແລະ 1 ຄືເປີດ)
        digitalWrite(PUMP_PIN, stream.getDataInt());
      }
    }
  });
  
}

// void loop() ເປັນສ່ວນທີ່ code ຈະວົນລູບເຮັດວຽກຢູ່ນີ້ເລື່ອຍໆ
void loop() {
  // put your main code here, to run repeatedly:

}