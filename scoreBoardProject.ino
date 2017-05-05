#include <Bridge.h>
#include <HttpClient.h>
#include <Process.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {  
  Serial.begin(9600); //sets baud rate

  // Set the cursor and begin
  lcd.setCursor(0, 1);
  lcd.begin(16, 2);
  lcd.print("MLB Scoreboard");
}

void loop() {
  if (Serial.available()) {
    delay(100);  //wait some time for the data to fully be read
    lcd.clear();
    // Read input and write it to the lcd
    while (Serial.available() > 0) {
      char c = Serial.read();
      lcd.write(c);
    }

  }
}



