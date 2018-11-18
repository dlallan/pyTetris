import serial

def main():
	ser = serial.Serial('/dev/ttyACM0', 9600)

	while True:
		# print("".join(map(chr, ser.readline())), end='')
		line = "".join(map(chr, ser.readline()))
		line = line.split(',')
		if len(line) == 1:
			continue
		print(line[0], line[1].rstrip('\n\r'))

if __name__ == "__main__":
	main()