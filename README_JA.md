
[![日本語(original)](https://img.shields.io/badge/日本語-original%20document-brightgreen)](README_JA.md)
[![English](https://img.shields.io/badge/English-document-brightgreen)](README.md)

<img src="https://github.com/takumi4424.png" alt="takumi4424 logo" height="50" align="right">

picoco: C/C++ build helper system for Raspberry Pi Pico
=======================================================
ついに Raspberry Pi Pico が発売されましたね :exclamation: :exclamation:
早速購入したあなたも[スタートガイド](https://datasheets.raspberrypi.org/pico/getting-started-with-pico.pdf)を見ながらLEDをチカチカさせていることでしょう :smile:

でも……`cmake`とか`make`とかよくわかりにくくないですか？
（私は初心者なのでよくわかりませんでした :sob:）

そこで，この`picoco`ツールを利用してより簡単に Raspberry Pi Pico の開発を行いましょう :exclamation: :exclamation:

もしあなたが`docker`コマンドを使用できるのなら，すぐに開発環境を立ち上げることができます :+1:
([Develop with Docker](#develop-with-docker)まで読み飛ばしてください．)

## 目次
- [Installation](#installation)
- [Usage](#usage)
  - [Develop with Docker](#develop-with-docker)
  - [Develop in local environment](#develop-in-local-environment)

## Installation
最低限以下のソフトウェアが必要です：
- [`picoco`](https://github.com/takumi4424/picoco)
  - `python3`
- [`pico-sdk`](https://github.com/raspberrypi/pico-sdk)
  - `cmake`
  - `gcc-arm-none-eabi`
  - `libnewlib-arm-none-eabi`
  - `build-essential`

**TODO: インストールスクリプトの作成**

### Ubuntu
```sh
$ sudo apt update
$ sudo apt install -y python3 cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential
$ INSTALL_DIR=$HOME/.pico # 適当なパス: $HOME/.pico や /opt/pico など……
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
ここで挙げる例では，以下を行います．
- `test_pico`というパッケージを作成
  - LED点滅させるコード(`test_pico/src/test_pico_main.c`)
  - `CMakeLists.txt`
- `test_pico`パッケージをビルド
  - `test_pico/build/test_pico.uf2`の生成

成果物である`test_pico/build/test_pico.uf2`をあなたの Raspberry Pi Pico にコピーすれば，LEDが点滅するはずです :exclamation: :exclamation:

### Develop with Docker
[picocoイメージ](https://hub.docker.com/repository/docker/takumi4424/picoco)を利用すると，すぐに開発環境の立ち上げができます :+1:
```sh
host$ docker run -it takumi4424/picoco:latest
container$ picoco create_pkg /root/test_pico
container$ cd /root/test_pico
container$ picoco build
```

### Develop in local environment
```sh
$ picoco create_pkg test_pico
$ cd test_pico
$ picoco build
```
