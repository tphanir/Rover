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

# Function to read accelerometer values
def read_accelerometer():
    accel_x = read_word_2c(ACCEL_XOUT_H)
    accel_y = read_word_2c(ACCEL_XOUT_H + 2)
    accel_z = read_word_2c(ACCEL_XOUT_H + 4)
    return accel_x, accel_y, accel_z

# Function to read gyroscope values
def read_gyroscope():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    gyro_y = read_word_2c(GYRO_XOUT_H + 2)
    gyro_z = read_word_2c(GYRO_XOUT_H + 4)
    return gyro_x, gyro_y, gyro_z

# Function to read magnetometer values (assumes raw read here)
def read_magnetometer():
    # Normally this requires configuring the AK8963 magnetometer, but assuming direct read here
    mag_x = read_word_2c(MAG_XOUT_H)
    mag_y = read_word_2c(MAG_XOUT_H + 2)
    mag_z = read_word_2c(MAG_XOUT_H + 4)
    return mag_x, mag_y, mag_z

# Conversion functions
def convert_accelerometer(raw_values):
    # 16384 LSB per g in +/- 2g mode
    accel_g = [val / 16384.0 for val in raw_values]
    return accel_g

def convert_gyroscope(raw_values):
    # 131 LSB per degree/second in +/- 250 degrees/second mode
    gyro_dps = [val / 131.0 for val in raw_values]
    return gyro_dps

def convert_magnetometer(raw_values):
    # 0.6 uT per LSB (assuming direct access mode)
    mag_uT = [val * 0.6 for val in raw_values]
    return mag_uT

# Main loop to read values continuously
def main():
    wake_up_mpu()
    print("WHO_AM_I register:", hex(read_who_am_i()))
    
    while True:
        accel_raw = read_accelerometer()
        gyro_raw = read_gyroscope()
        mag_raw = read_magnetometer()
        
        accel_g = convert_accelerometer(accel_raw)
        gyro_dps = convert_gyroscope(gyro_raw)
        mag_uT = convert_magnetometer(mag_raw)
        
        gyro_dps = [round(num, 2) for num in gyro_dps]

        #print(f"Accelerometer (g): {accel_g}")
        print(f"Gyroscope (°/s): {gyro_dps}")
        #print(f"Magnetometer (µT): {mag_uT}")
        print("") 
        time.sleep(2)

if __name__ == "__main__":
    main()

