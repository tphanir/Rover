def voice(radio, mega):
    prev = ''
    def do(string, threshold):
        try:
            command, probability = string.strip().split(',')
            
            # Convert probability to float
            probability = float(probability)

            # Check if the probability is greater than the threshold
            if probability > threshold:
                if command == prev:
                    return
                if command == "go":
                    mega.write(f"f\n".encode())
                elif command == "left":
                    mega.write(f"l\n".encode())
                elif command == "right":
                    mega.write(f"r\n".encode())
                elif command == "stop":
                    mega.write(f"s\n".encode())
                else:
                    return
                print(f'[VOICE] {command}')
        except ValueError:
            print("Input Error")

    
    result = subprocess.run(['docker', 'stop', 'voice-nav'])
    result = subprocess.run(['docker', 'rm', 'voice-nav'])
    result = subprocess.run(['./script.sh'])
    
    mega.write('Manual\n'.encode())
    while True:
        with open('VoiceNav/data.txt', 'r') as file:
            content = file.read() 
            do(content, 0.9)

        if radio.serial_connection and radio.serial_connection.in_waiting > 0:
            data = radio.serial_connection.readline()
            if data == 'return':
                result = subprocess.run(['docker', 'stop' 'voice-nav'])
                mega.write('return\n'.encode())
                break

