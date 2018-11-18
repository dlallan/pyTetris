import serial

def main():
	ser = serial.Serial('/dev/ttyACM0', 9600)

	while True:
		# print("".join(map(chr, ser.readline())), end='')
		line = "".join(map(chr, ser.readline())).rstrip()
		# line = line.split(',')
		# if len(line) == 1:
			# continue
		if len(line) == 15: # ignore fragments
			print(line)

if __name__ == "__main__":
	main()