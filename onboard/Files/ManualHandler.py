def manual(radio, mega):
 
    while True:
        # Get input from the user
        if radio.serial_connection.in_waiting > 0:
            command = radio.serial_connection.readline().decode('utf-8').strip()
            
        # Map commands to robot actions
            if command == 'W':
                mega.write(f"f\n".encode())
            elif command == 'A':
                mega.write(f"l\n".encode())
            elif command == 'S':
                mega.write(f"b\n".encode())
            elif command == 'D':
                mega.write(f"r\n".encode())
            elif command == 'X':
                mega.write(f"s\n".encode())
            elif command == 'return':
                mega.write(f'return\n'.encode())
                break

