[![日本語(original)](https://img.shields.io/badge/日本語-original%20document-brightgreen)](README_JA.md)
[![English](https://img.shields.io/badge/English-document-brightgreen)](README.md)

<img src="https://github.com/takumi4424.png" alt="takumi4424 logo" height="50" align="right">

picoco: C/C++ build helper system for RPi Pico
=======================================================
Now, the Raspberry Pi Pico is available :exclamation: :exclamation: <br>
I'm sure you've already bought it, and you're probably blinking your LEDs :smile:

But... We don't really understand `cmake` or `make`, right? <br>
（I'm a beginner, so I don't understand it at all :sob:）

So, let's use this `picoco` tool to develop Raspberry Pi Pico more easily :exclamation: :exclamation:

If you can use the `docker` command, you can quickly set up a development environment :+1: <br>
(See: [Develop with Docker](#develop-with-docker))

## Table of contents
- [Installation](#installation)
- [Usage](#usage)
  - [Develop with Docker](#develop-with-docker)
  - [Develop in local environment](#develop-in-local-environment)

## Installation
At a minimum, followings are required:
- [`picoco`](https://github.com/takumi4424/picoco)
  - `python3`
- [`pico-sdk`](https://github.com/raspberrypi/pico-sdk)
  - `cmake`
  - `gcc-arm-none-eabi`
  - `libnewlib-arm-none-eabi`
  - `build-essential`

**TODO: make installation script**

### Ubuntu
```sh
$ sudo apt update
$ sudo apt install -y python3 cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential
$ INSTALL_DIR=$HOME/.pico # e.g. "$HOME/.pico", "/opt/pico", etc.
$ mkdir -p $(INSTALL_DIR)
$ git -C $INSTALL_DIR clone https://github.com/takumi4424/picoco.git
$ git -C $INSTALL_DIR clone https://github.com/raspberrypi/pico-sdk.git
$ echo "export PICOCO_PATH=$INSTALL_DIR/picoco"     >> $HOME/.bashrc
$ echo "export PICO_SDK_PATH=$INSTALL_DIR/pico-sdk" >> $HOME/.bashrc
$ echo "export PATH=\$PATH:$PICOCO_PATH/bin"        >> $HOME/.bashrc
```

### MacOS
TODO

### Windows
TODO


## Usage
Examples in this section will do the followings:
- Create a new package named `test_pico`
  - It includes LED blinking code (`test_pico/src/test_pico_main.c`)
  - It includes `CMakeLists.txt`
- Build `test_pico` package
  - It makes `test_pico/build/test_pico.uf2`

Copy the product `test_pico/build/test_pico.uf2` to your Raspberry Pi Pico and the LED will blink :examination: :examination:

### Develop with Docker
You can use [picoco image](https://hub.docker.com/repository/docker/takumi4424/picoco) to quickly launch the development environment :+1:
```sh
H$ docker run -it takumi4424/picoco:latest
C$ picoco create_pkg /root/test_pico
C$ cd /root/test_pico
C$ picoco build
C$ ls build/*.uf2
```
`H$`: Host, `C$`: Container

### Develop in local environment
```sh
$ picoco create_pkg test_pico
$ cd test_pico
$ picoco build
```
