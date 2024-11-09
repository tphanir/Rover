import smbus
import time

# MPU9250 I2C address
MPU_ADDRESS = 0x68

# Register addresses
WHO_AM_I = 0x75
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
MAG_XOUT_H = 0x03

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
    gyro_z = read_word_2c(GYRO_XOUT_H + 4)
    return gyro_x, gyro_y, gyro_z

# Function to convert raw gyroscope data to °/s
def convert_gyroscope(raw_values):
    # 131 LSB per degree/second in +/- 250 degrees/second mode
    gyro_dps = [val / 131.0 for val in raw_values]
    return gyro_dps

# Function to calibrate gyroscope
def calibrate_gyroscope(calibration_samples=100):
    print("Calibrating gyroscope... Please keep the IMU steady.")
    gyro_offset = [0, 0, 0]
    
    # Collect `calibration_samples` samples to compute the offset
    for i in range(calibration_samples):
        gyro_raw = read_gyroscope()
        gyro_offset[0] += gyro_raw[0]
        gyro_offset[1] += gyro_raw[1]
        gyro_offset[2] += gyro_raw[2]
        time.sleep(0.01)  # Small delay between samples
    
    # Calculate the average offset for each axis
    gyro_offset = [x / calibration_samples for x in gyro_offset]
    
    # Convert the offsets to °/s
    gyro_offset = convert_gyroscope(gyro_offset)
    print(f"Gyroscope offset: {gyro_offset}")
    
    return gyro_offset

# Main loop to read and print calibrated gyroscope values
def main():
    wake_up_mpu()
    print("WHO_AM_I register:", hex(read_who_am_i()))
    
    # Calibrate the gyroscope
    gyro_offset = calibrate_gyroscope(calibration_samples=100)
    
    rot = False

    prev = time.time()

    n = 330
    count = 0
    theta = 0
    omega = 0

    with open('data.txt', 'w') as file:
        while True:
            gyro_raw = read_gyroscope() 
            gyro_dps = convert_gyroscope(gyro_raw)

        # Apply calibration offsets
            gyro_calibrated = [gyro_dps[i] - gyro_offset[i] for i in range(3)]
        
        # Round the values for easier readability
            gyro_calibrated = [round(val, 2) for val in gyro_calibrated]

            delta = 0.5 * (gyro_calibrated[2] - omega) / n
            theta_dash = theta + delta + (gyro_calibrated[2] * 1.0 / n)
            theta = theta_dash
            omega = gyro_calibrated[2]
            file.write(str(gyro_calibrated[2]) + ' ' + str(theta_dash) + '\n')
        
        
        '''
        while gyro_calibrated[2] > 1.0:
            rot = True
            curr = time.time()
            angle += gyro_calibrated[2] * (curr - prev)
            prev = curr
        
        if rot:
            print(angle)
            rot = False
        
        '''
        

if __name__ == "__main__":
    main()

