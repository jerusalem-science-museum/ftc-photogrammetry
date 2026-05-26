#include "Basic_Routines.h"

//-------set current steps  ---------------------
void set_steps(int16_t s) {
  steps = s;
}

//---------print steps-----------
void print_steps() {
  char buffer[100];
  sprintf(buffer, "Steps: %d", steps);
  Serial.println(buffer); 
}

//---------set angle---------------
void set_angle(float ang) {
  angle = ang;
}

//-------------print the current angle-------------------
void print_angle() {
  Serial.print("Angle: ");
  Serial.println(angle);
}

//------------set destination for angle---------------
void set_destination(float dest_angle) {
  destination = dest_angle;
}

//---------------print the destination-----------------
void print_destination() {
  char buffer[100];
  sprintf(buffer, "Destination: %f", destination);
  Serial.println(buffer); 
}


//----------check if arm has reached the destination------
bool in_destination() {
  return (abs(angle-destination) < TOLERANCE);
}


//---------move the motor to the angle with blocking functions as delay - also sends key codes
void hard_move(float dest_angle) {
  destination = dest_angle;
  if (in_destination())
    return;
  int delta_steps = int(abs(angle-dest_angle)/angle_per_pulse);
  for (int i = 0; i < delta_steps; i++) {
    one_step((angle < dest_angle) ? false : true);
    delay(rate);

    if (send_keys) {
      if (int(angle) < next_angle_for_image) {
        Keyboard.write(KEY_CAPS_LOCK);
        // Keyboard.write(KEY_CAPS_LOCK);
        // delay(100); // You can adjust the delay as needed
        // Keyboard.release(KEY_CAPS_LOCK);
        // Keyboard.write(current_key);
        current_key++;
        if (current_key == first_angle_key + NUMBER_OF_IMAGES)
          Keyboard.write(end_key);
        next_angle_for_image -= angle_per_image;
      }
    }

  }
  print_steps();
  print_angle();
}

//----------move a motor one step-----------------
void one_step(bool move_direction) {
  if (move_direction != motor_direction){
      motor_direction = move_direction;
      digitalWrite(DIR_PIN, move_direction);
      delay(DIRECTION_CHANGE_WAIT_TIME);// wait to IO stable   
  }
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(2);// for fasr processors may not need with ATMEGA
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(2);
  if (move_direction == false) {
    steps++;
    angle += angle_per_pulse; }
  else {
    steps--;
    angle -= angle_per_pulse; 
  }
}

//------ go to the side and calibrate to 0---------
void homming(){
  digitalWrite(ENABLE_PIN, LOW);  //enable motors 
  for(int16_t i=0; i< HOMMING_STEPS; i++){
    one_step(true);
    delay(HOMMING_RATE);
  }
  // move to the center
  for(int16_t i=0; i < STEPS_TO_CENTER; ++i){
    one_step(false);
    delay(HOMMING_RATE);
  }

  set_angle(0);
  set_steps(0);
  delay(300);
  digitalWrite(ENABLE_PIN, HIGH);
}

//-------blink led XX times, Ton , Toff) --------------------
void blink_Led(uint8_t blinks_number, uint16_t on_time, uint16_t off_time){
  for(uint8_t i=0; i< blinks_number; ++i){
    digitalWrite(LED_OUT, HIGH);  //led on 
    delay(on_time);
    digitalWrite(LED_OUT, LOW);  //led off 
    delay(off_time);
  }
}
