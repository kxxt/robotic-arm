# 完全环境配置指南

## 系统安装与基本配置

使用树莓派官方系统烧录工具,烧录`Manjaro-ARM-xfce-rpi4-21.04.img.xz`(镜像去 manjaro 官网下载).

烧录完后修改boot分区的config.txt:

```
# 确保显存>=128MiB
gpu_mem=128
# 启用摄像头
start_x=1
# Enables I2C
dtparam=i2c1=on
dtparam=spi=on
framebuffer_width=1824
framebuffer_height=984
hdmi_group=1
hdmi_mode=1
hdmi_force_hotplug=1
```

弹出SD卡, 插入树莓派上电开机(HDMI外接屏幕)

完成系统的基本设置(键盘布局,用户名pi,密码,主机名raspberry,root密码,时区Asia/Shanghai,语言建议英文en_US)

确认设置后系统会自动调整分区大小并重启

连接到一个稳定快速的网络或者校园网(由于驱动问题,此系统暂时只能识别2.4GHz频段无线网络,影响不大)

## 依赖项安装

### 镜像加速

```bash
sudo pacman-mirrors -c China
# 自动切换国内快速镜像源
```

### 系统更新

```bash
sudo pacman -Syyu
```

### 基础软件安装

pip,yay和基本的开发工具

```bash
sudo pacman -S python-pip yay base-devel net-tools cmake
yay -S pigpio # GPIO 包
yay -S realvnc-vnc-server-aarch64 #　VNC
sudo systemctl enable vncserver-x11-serviced.service
sudo systemctl enable vncserver-virtuald.service
```

### 中文输入法(Optional)

```bash
sudo pacman -S fcitx-googlepinyin fcitx-configtool
```

### 代理软件安装(Optional)

```bash
sudo pacman -S snapd proxychains-ng
reboot
sudo snap install qv2ray
# snap 报错too early 则重试
# v2ray core 下载
wget https://github.com/v2fly/v2ray-core/releases/download/v4.37.3/v2ray-linux-arm64-v8a.zip
mkdir v2ray
unzip v2ray-*.zip -d v2ray/
# v2ray core 解压到一个目录下然后在qv2ray里的Kernel Settings设置对应路径
# 在qv2ray里添加自己机场的订阅
# proxychains 设置 修改 /etc/proxychains.conf
# 修改最后一行 socks5 127.0.0.1 1089
# 然后就可以畅快的上网了
```

### 项目密切相关依赖
```bash
sudo pacman -S gst-python lapack i2c-tools sdl freetype freetype2-demos sdl_gfx sdl_pango sdl_net sdl_sound sdl_image python-pygame python-pygame-sdl2 python-pillow opencv python-opencv
sudo pacman -S blas
yay --aur python-raspberry-gpio 
```
#### Python 包

```bash
# 切换到工程目录下
sudo pip3 install prebuilt/aarch64/vosk/*.whl
sudo pip3 install prebuilt/aarch64/dlib/*.whl
sudo pip3 install prebuilt/aarch64/mediapipe/*.whl
sudo pacman -U prebuilt/aarch64/tflite2.4/*.zst
sudo pip3 install -r requirements.txt
# uncomment mediapipe.python.solutions.drawing_utils
sudo nano /usr/lib/python3.9/site-packages/mediapipe/python/solutions/__init__.py
将下面一行改为
# import mediapipe.python.solutions.drawing_utils
import mediapipe.python.solutions.drawing_utils
```

#### 二进制库(TFLite)

```bash
sudo cp prebuilt/aarch64/tflite2.4/*.so /usr/local/lib/
# 将此路径添加到系统的包含路径
sudo nano /etc/profile
# 追加一行
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
source /etc/profile # 使之生效
# 注意: 重启之后才在全部环境生效
```

