def forward(mega, radio):
    buffer = bytearray()
    while True:
        if mega.serial_connection and mega.serial_connection.in_waiting > 0:
            data = mega.serial_connection.read(1024)
            buffer.extend(data)

            while b'\n' in buffer:
                line, _, buffer = buffer.partition(b'\n')
                print(f"Received: {line}")

