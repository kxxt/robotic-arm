# Setup Mediapipe on Raspberry PI 4 model B
# DO NOT FOLLOW THIS GUIDE!
## Install Bazel from source

Follow this [guide](SetupBazel.md)

## Clone Mediapipe 

```bash
git clone https://github.com/google/mediapipe.git
cd mediapipe
```

## Install OpenCV from source

```bash
chmod +x setup_opencv.sh
./setup_opencv.sh
```

## Install EGL Driver

```bash
sudo apt-get install mesa-common-dev libegl1-mesa-dev libgles2-mesa-dev -y
```

## Then follow this guide [jiuqiant/mediapipe_python_aarch64 (github.com)

Note: add this to the bazel command in setup.py before building wheel.

```
'--copt=-march=armv7-a',
'--copt=-mfpu=neon-vfpv4',
```

## References

- [【MediaPipe】Raspberry Pi 4で環境構築し、CPU/GPUで動かしてみた（v0.7.5） | DevelopersIO (classmethod.jp)](https://dev.classmethod.jp/articles/mediapipe-install-on-raspberry-pi-4-with-cpu-gpu/#toc-16)
- [jiuqiant/mediapipe_python_aarch64 (github.com)
- [[Raspberry Pi4 単体で TensorFlow Lite はどれくらいの速度で動く？ - Qiita](https://qiita.com/terryky/items/243000fcfcb89af11510)](https://github.com/jiuqiant/mediapipe_python_aarch64)

- [Neon error when importing mediapipe python on raspberry pi 3 · Issue #1629 · google/mediapipe (github.com)](https://github.com/google/mediapipe/issues/1629)