import serial
import time

from robotic_arm.config import SERVO_SERIAL_PATH, SERVO_SERIAL_BAUD, SERVO_BOARD_PORTS

servo_commands = {
    "write": 1,
    "read": 28,
    "lock": 31
}


def acquire_serial_handle(device_path=None, serial_baud=None):
    device_path = device_path or SERVO_SERIAL_PATH
    serial_baud = serial_baud or SERVO_SERIAL_BAUD
    return serial.Serial(device_path, serial_baud)


def servo_exec(handle, id, cmd, par1=None, par2=None):
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


def init_servo_board(ports=None):
    ports = ports or SERVO_BOARD_PORTS
    from robotic_arm.gpio import pi
    import pigpio
    pi.set_mode(ports[0], pigpio.OUTPUT)  # 配置RX_CON 即 GPIO17 为输出
    pi.write(ports[0], 0)
    pi.set_mode(ports[1], pigpio.OUTPUT)  # 配置TX_CON 即 GPIO27 为输出
    pi.write(ports[1], 1)


def set_servo_board_mode(ports, mode):
    ports = ports or SERVO_BOARD_PORTS
    from robotic_arm.gpio import pi
    if mode == "read":
        pi.write(ports[1], 0)  # 拉低TX_CON 即 GPIO27
        pi.write(ports[0], 1)  # 拉高RX_CON 即 GPIO17
    elif mode == "write":
        pi.write(ports[1], 1)  # 拉高TX_CON 即 GPIO27
        pi.write(ports[0], 0)  # 拉低RX_CON 即 GPIO17
    else:
        raise ValueError("Mode can only be 'read' or 'write'!")


def servo_read(handle, id, board_ports=None):
    set_servo_board_mode(board_ports, "write")  # 将单线串口配置为输出
    handle.flushInput()  # 清空接收缓存
    servo_exec(handle, id, servo_commands["read"])  # 发送读取位置命令
    time.sleep(0.00034)  # 小延时，等命令发送完毕。不知道是否能进行这么精确的延时的，但是修改这个值的确实会产生影响。
    # 实验测试调到这个值的时候效果最好
    set_servo_board_mode(board_ports, "read")  # 将单线串口配置为输入
    time.sleep(0.005)  # 稍作延时，等待接收完毕
    count = handle.inWaiting()  # 获取接收缓存中的字节数
    pos = None
    if count != 0:  # 如果接收到的数据不空
        recv_data = handle.read(count)  # 读取接收到的数据
        if count == 8:  # 如果接收到的数据是8个字节（符合位置读取命令的返回数据的长度）
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == 0x1C:
                # 第一第二个字节等于0x55, 第5个字节是0x1C 就是 28 就是 位置读取命令的命令号
                pos = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))  # 将接收到的字节数据拼接成完整的位置数据
                # 上面这小段代码我们简化了操作没有进行和校验，只要帧头和命令对了就认为数据无误
    return pos  # 返回读取到的位置
