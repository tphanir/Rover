import smbus
import time

# MPU9250 I2C address
MPU_ADDRESS = 0x68

# Register addresses
WHO_AM_I = 0x75
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43

# Initialize I2C (bus 1)
bus = smbus.SMBus(1)

# Function to read the WHO_AM_I register
def read_who_am_i():
    who_am_i = bus.read_byte_data(MPU_ADDRESS, WHO_AM_I)
    return who_am_i

# Function to wake up the MPU9250
def wake_up_mpu():
    bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0)  # Clear sleep bit (6)
    time.sleep(0.1)  # Wait for device to be ready

# Function to read a word (16 bits) and handle endian-ness
def read_word_2c(addr):
    high = bus.read_byte_data(MPU_ADDRESS, addr)
    low = bus.read_byte_data(MPU_ADDRESS, addr+1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

# Function to read gyroscope values
def read_gyroscope():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    gyro_y = read_word_2c(GYRO_XOUT_H + 2)
    return gyro_x, gyro_y

# Conversion function
def convert_gyroscope(raw_values):
    # 131 LSB per degree/second in +/- 250 degrees/second mode
    gyro_dps = [val / 131.0 for val in raw_values]
    return gyro_dps

# Function to calibrate gyroscope
def calibrate_gyroscope(samples=100):
    offset_x = 0
    offset_y = 0
    for _ in range(samples):
        gyro_raw = read_gyroscope()
        gyro_dps = convert_gyroscope(gyro_raw)
        offset_x += gyro_dps[0]
        offset_y += gyro_dps[1]
        time.sleep(0.01)
    offset_x /= samples
    offset_y /= samples
    return offset_x, offset_y

# Main loop to read values continuously and calculate rotation
def main():
    wake_up_mpu()
    print("WHO_AM_I register:", hex(read_who_am_i()))
    
    offset_x, offset_y = calibrate_gyroscope()
    print(f"Calibration offsets: X={offset_x:.2f} °/s, Y={offset_y:.2f} °/s")

    previous_time = time.time()
    angle_x = 0.0
    angle_y = 0.0

    while True:

        gyro_raw = read_gyroscope()
        gyro_dps = convert_gyroscope(gyro_raw)

        # Adjust for drift
        gyro_dps[0] -= offset_x
        gyro_dps[1] -= offset_y


        # Print the readings every 2 seconds
        if dt >= 2:
            print(f"Gyroscope (°/s): {gyro_dps}")
            print(f"Rotation (°): X={round(angle_x, 2)}, Y={round(angle_y, 2)}")
            print("")
            previous_time = current_time

        time.sleep(0.1)

if __name__ == "__main__":
    main()

