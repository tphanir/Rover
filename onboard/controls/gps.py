def gps(radio, mega):
    while True:
        
        if radio.serial_connection.in_waiting > 0:
            command = radio.serial_connection.readline().decode('utf-8').strip()
            match = re.search(r"gps\s(-?\d+\.\d+),(-?\d+\.\d+)", command)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                mega.write(f'{latitude},{longitude}\n'.encode())
                break
            elif command == 'return':
                mega.write("return\n".encode())
            
                break
            else:
                print("Coordinates not found")

