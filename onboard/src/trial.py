import serial
import subprocess

prev = ''

def do(string, threshold, mega):
    global prev
    try:
        command, probability = string.strip().split(',')
        # Convert probability to float
        probability = float(probability)

        # Check if the probability is greater than the threshold
        if probability > threshold:
            if command == prev:
                return
            if command == "go":
                mega.write("f\n".encode())
            elif command == "left":
                mega.write("l\n".encode())
            elif command == "right":
                mega.write("r\n".encode())
            elif command == "stop":
                mega.write("s\n".encode())
            else:
                return

            print(command)
            prev = command
    except ValueError:
        print("Invalid input format. Ensure the input is 'command,probability'.")


def voice(mega):
        
    result = subprocess.run(['docker', 'stop', 'voice-nav'])
    result = subprocess.run(['docker', 'rm', 'voice-nav'])
    process = subprocess.Popen(['./script.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        with open('/home/jetson/rover/jetson-voice/VoiceNav/data.txt', 'r') as file:
            content = file.read() 
            do(content, 0.8, mega)

mega = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
mega.write(f"Manual\n".encode())
voice(mega)
