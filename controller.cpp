//////////////////////////////////////////////////////////
// <put header here>
//////////////////////////////////////////////////////////
#include <Arduino.h>

#define SHORT_DELAY 50 // 50 ms delay for button debounce
#define DEBUG true // set false before submitting!

// pin numbers
const int pinButtonRight = 6;
const int pinButtonDown = 7;
const int pinButtonUp = 8;
const int pinButtonLeft = 9;
const int buttonPins[4] = { pinButtonRight, pinButtonDown, pinButtonUp, pinButtonLeft };
const int numButtonPins = sizeof(buttonPins) / sizeof(buttonPins[0]);

// track button states in an array
int pinStates[4] = { HIGH, HIGH, HIGH, HIGH };
const int numPinStates = sizeof(pinStates) / sizeof(pinStates[0]);

void setup()
{
	init();
	Serial.begin(9600); // serial comms is done over default Serial port
	#if DEBUG
		Serial.println("[DEBUG] Serial setup complete.");
	#endif
 
	// set control pins and their pull-up resistors
	for (int i = 0; i < numButtonPins; i++) 
	{	
		pinMode(buttonPins[i], INPUT);
		digitalWrite(buttonPins[i], HIGH);
	}
}

void getPinStates()
{
	// update state of each pin
	for (int i = 0; i < numPinStates; i++)
	{
		pinStates[i] = digitalRead(buttonPins[i]);
		delay(SHORT_DELAY); // delay for button debounce
	}
}


// comms format:
// <pin number>,<0 for button down, 1 for button up><newline>
void transmit()
{
	for (int i = 0; i < numPinStates; i++)
	{
		Serial.print(buttonPins[i]);
		Serial.print(',');
		Serial.println(pinStates[i]);
	}
}

int main()
{
	setup();

	while(true)
	{
		// check and update pin states
		getPinStates();
		
		// write pin states to serial
		transmit();
	}

	return 0;
}