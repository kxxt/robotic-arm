import serial

from robotic_arm.config import SERVO_SERIAL_PATH, SERVO_SERIAL_BAUD


def acquire_serial_handle(device_path=None, serial_baud=None):
    device_path = device_path or SERVO_SERIAL_PATH
    serial_baud = serial_baud or SERVO_SERIAL_BAUD
    return serial.Serial(device_path, serial_baud)


def servo_write(handle, id, cmd, par1=None, par2=None):
    buf = bytearray(b'\x55\x55')
    length = 3  # 若命令是没有参数的话数据长度就是3
    buf1 = bytearray(b'')
    # 对参数进行处理
    if par1 is not None:
        length += 2  # 数据长度加2
        buf1.extend([(0xff & par1), (0xff & (par1 >> 8))])  # 分低8位 高8位 放入缓存
    if par2 is not None:
        length += 2
        buf1.extend([(0xff & par2), (0xff & (par2 >> 8))])  # 分低8位 高8位 放入缓存
    buf.extend([(0xff & id), (0xff & length), (0xff & cmd)])
    buf.extend(buf1)  # 追加参数
    # 计算校验和
    checksum = 0x00
    for b in buf:  # 求和
        checksum += b
    checksum = checksum - 0x55 - 0x55  # 去掉命令开头的两个 0x55
    checksum = ~checksum  # 取反
    buf.append(0xff & checksum)  # 取低8位追加进缓存
    handle.write(buf)  # 发送

