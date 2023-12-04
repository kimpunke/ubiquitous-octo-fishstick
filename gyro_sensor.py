import smbus
import time

# MPU-9250의 I2C 주소
MPU9250_ADDRESS = 0x68

# 레지스터 주소
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_ACCEL_YOUT_H = 0x3D
MPU9250_ACCEL_ZOUT_H = 0x3F

MPU9250_GYRO_XOUT_H = 0x43
MPU9250_GYRO_YOUT_H = 0x45
MPU9250_GYRO_ZOUT_H = 0x47

# I2C 버스 초기화
bus = smbus.SMBus(1)

# MPU-9250 초기화
bus.write_byte_data(MPU9250_ADDRESS, 0x6B, 0)

# 이전 데이터를 저장할 변수 초기화
before_x = before_y = before_z = 0

def read_word(reg):
    high = bus.read_byte_data(MPU9250_ADDRESS, reg)
    low = bus.read_byte_data(MPU9250_ADDRESS, reg + 1)
    value = (high << 8) + low
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def read_gyroscope():
    x = read_word_2c(MPU9250_GYRO_XOUT_H)
    y = read_word_2c(MPU9250_GYRO_YOUT_H)
    z = read_word_2c(MPU9250_GYRO_ZOUT_H)
    return x, y, z

while True:
    # 이전 데이터 저장
    before_x, before_y, before_z = read_gyroscope()

    # 0.5초 대기
    time.sleep(0.5)

    # 현재 데이터 읽어오기
    x, y, z = read_gyroscope()

    # 차이 출력
    print(f"Delta Gyroscope (x, y, z): {x - before_x}, {y - before_y}, {z - before_z}")

    # 이전 데이터 업데이트
    before_x, before_y, before_z = x, y, z
