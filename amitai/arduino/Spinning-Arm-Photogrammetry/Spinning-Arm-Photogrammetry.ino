#include "Basic_Routines.h"

void setup() {

  Serial.begin(BAUDRATE);
  Keyboard.begin();
  delay (1000);

  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(LED_OUT, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  digitalWrite(ENABLE_PIN, HIGH);
  
//  homming();
}

void loop() {
  
  if (millis() > last_click_time + delay_between_clicks) {
    clickable = true;
  }

  if (clickable && digitalRead(BUTTON_PIN) == LOW) {
    clickable = false;
    digitalWrite(ENABLE_PIN, LOW);
    delay(5); // delay for IO's to stable
    //start photogrammetry routine:
    Keyboard.write(starting_key);  // 0
    //move to the side
    hard_move(MAX_ANGLE);
    delay(DELAY_AT_STOP);
    Keyboard.write(starting_key);  // 0
    send_keys = true;
    current_key = first_angle_key;
    next_angle_for_image = MAX_ANGLE;
    hard_move(MIN_ANGLE);
    delay(DELAY_AT_STOP);
    send_keys = false;
    hard_move(0);
    delay(5); // delay for IO's to stable
    digitalWrite(ENABLE_PIN, HIGH);
  }
}
