#include <Keyboard.h>

const int leftButtonPin = A1;   // Pin for the left button (A1)
const int rightButtonPin = A2;  // Pin for the right button (A2)
const int groundPin = A0;       // Pin for ground (A0)

void setup() {
  pinMode(leftButtonPin, INPUT_PULLUP);   // Initialize the left button with internal pull-up resistor
  pinMode(rightButtonPin, INPUT_PULLUP);  // Initialize the right button with internal pull-up resistor
  pinMode(groundPin, OUTPUT);             // Initialize the ground pin as output
  digitalWrite(groundPin, LOW);           // Set ground pin to low
  Keyboard.begin();                      // Initialize keyboard emulation
}

void loop() {
  // Check button presses
  checkButtonPresses(leftButtonPin, 'l');
  checkButtonPresses(rightButtonPin, 'r');
}

void checkButtonPresses(int buttonPin, char key) {
  static bool buttonState = HIGH;    // Button state (HIGH - not pressed, LOW - pressed)
  static bool lastButtonState = HIGH;    // Previous button state

  bool currentState = digitalRead(buttonPin);  // Current button state

  // If button state has changed
  if (currentState != lastButtonState) {
    // If button is pressed
    if (currentState == LOW) {
      pressKey(key);  // Emulate key press
    }
  }

  lastButtonState = currentState;  // Update previous button state
}

void pressKey(char key) {
  Keyboard.press(key);  // Press the key
  delay(1000);  // Delay after key press for 1 second
  Keyboard.release(key);  // Release the key
}
