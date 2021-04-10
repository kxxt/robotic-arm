# Bazel Installation on raspberrypi 4b

First， install dependencies
```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip
```

Download Bazel dist source code from github releases.

- IMPORTANT ： please download the `dist` zip, not the github generated source tarball.

unzip it and cd to the directory

Make a few changes to it following guides in https://github.com/samjabrahams/tensorflow-on-raspberry-pi/blob/master/GUIDE.md#3-build-bazel

Apply the patch in [bazel-on-arm/bazel-3.7.2-arm.patch at master · koenvervloesem/bazel-on-arm (github.com)](https://github.com/koenvervloesem/bazel-on-arm/blob/master/patches/bazel-3.7.2-arm.patch)

Build it
```
sudo LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 env EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" ./compile.sh
```

### Reference
- https://github.com/opencv/opencv/issues/15278
- [tensorflow-on-raspberry-pi/GUIDE.md at master · samjabrahams/tensorflow-on-raspberry-pi (github.com)](https://github.com/samjabrahams/tensorflow-on-raspberry-pi/blob/master/GUIDE.md#3-build-bazel)

- [koenvervloesem/bazel-on-arm: Build the open source build tool Bazel for ARM on the Raspberry Pi (github.com)](https://github.com/koenvervloesem/bazel-on-arm)