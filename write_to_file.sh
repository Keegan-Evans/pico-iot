# /usr/bin/bash


if [[ ! -d pico ]]; then
mkdir pico
fi

cd pico

git clone https://github.com/micropython/micropython.git --branch master

cd micropython
make -C ports/rp2 submodules

sudo apt update
sudo apt install -y cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential 

cd ports/rp2
make BOARD=PICO_W