//////////////////////////////////////////////////////////
// <put header here>
//////////////////////////////////////////////////////////
#include <Arduino.h>

#define SHORT_DELAY 50 // 50 ms delay for button debounce
#define DEBUG false // set false before submitting!
#define BAUD_RATE 9600 // 9600

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
	Serial.begin(BAUD_RATE); // serial comms is done over default Serial port
	Serial.setTimeout(1); // TEST
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
// <pin 1> , <0 for button down, 1 for button up> , <pin 2>,...,<newline>
void transmit()
{
	const int numChars = 15; // 4 pins + 4 states + 7 commas = 15 characters

	for (int i = 0; i < numChars; i++)
	{
		// i in (0, 4, 8, 12): add pin ID (0, 1, 2, 3)
		if (i % 4 == 0)
			Serial.print(buttonPins[i/numButtonPins]);

		// i in (2, 6, 10, 14): add pin state (0, 1, 2, 3)
		else if ((i+2) % 2 == 0)
			Serial.print(pinStates[(i-2)/numPinStates]);

		// i is odd: add comma 
		else if (i % 2 != 0)
			Serial.print(',');
	}

	Serial.println();
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