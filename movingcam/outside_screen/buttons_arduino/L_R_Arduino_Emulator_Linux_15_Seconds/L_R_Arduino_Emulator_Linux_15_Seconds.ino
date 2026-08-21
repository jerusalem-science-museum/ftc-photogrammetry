#include <Keyboard.h>

const int leftButtonPin = A1;   // Pin for the left button (A1)
const int rightButtonPin = A2;  // Pin for the right button (A2)
const int groundPin = A0;       // Pin for ground (A0)
const unsigned long debounceDelay = 1000;  // Debounce delay in milliseconds
const unsigned long autoPressDelay = 15000;  // Auto press delay in milliseconds (15 seconds)

unsigned long lastPressTime = 0;  // Last button press time
unsigned long lastAutoPressTime = 0;  // Last auto press time

void setup() {
  pinMode(leftButtonPin, INPUT_PULLUP);   // Initialize the left button with internal pull-up resistor
  pinMode(rightButtonPin, INPUT_PULLUP);  // Initialize the right button with internal pull-up resistor
  pinMode(groundPin, OUTPUT);             // Initialize the ground pin as output
  digitalWrite(groundPin, LOW);           // Set ground pin LOW
  Keyboard.begin();                       // Initialize keyboard emulation
}

void loop() {
  unsigned long currentTime = millis();  // Current time in milliseconds
  
  // Check button presses
  checkButtonPress(leftButtonPin, 'l', currentTime);
  checkButtonPress(rightButtonPin, 'r', currentTime);

  // Check for automatic 'R' press
  if (currentTime - lastAutoPressTime > autoPressDelay) {
    pressKey('r');
    lastAutoPressTime = currentTime;
  }
}

void checkButtonPress(int buttonPin, char key, unsigned long currentTime) {
  static bool lastButtonState = HIGH;    // Previous button state
  bool currentState = digitalRead(buttonPin);  // Current button state

  // If button state has changed and enough time has passed since last press
  if (currentState != lastButtonState && currentTime - lastPressTime > debounceDelay) {
    // If button is pressed
    if (currentState == LOW) {
      pressKey(key);  // Emulate key press
      lastPressTime = currentTime;  // Update last press time
      lastAutoPressTime = currentTime;  // Reset auto press timer
    }
  }

  lastButtonState = currentState;  // Update previous button state
}

void pressKey(char key) {
  Keyboard.press(key);
  delay(100);  // Delay after key press for debounce (adjust as needed)
  Keyboard.release(key);
}


