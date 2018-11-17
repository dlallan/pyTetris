//////////////////////////////////////////////////////////
// <put header here>
//////////////////////////////////////////////////////////
#include <Arduino.h>

#define SHORT_DELAY 50 // 50 ms delay for button debounce

// pin numbers
// TODO: assign pin numbers for buttons
const int pinButtonLeft;
const int pinButtonRight;
const int pinButtonUp;
const int pinButtonDown;

// button states array
bool pinStates[4] = {false, false, false, false};


void 

void setup()
{
	init();
	Serial.begin(9600); // serial comms is done over default Serial port

	// set control pins

	// set pull-up resistors on pins
}

int main()
{
	setup();

	while(true)
	{
		// check pins
		// 
	}

	return 0;
}