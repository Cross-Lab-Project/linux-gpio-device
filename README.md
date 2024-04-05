First make sure you are running a linux-kernel with gpio-sim enabled.
Otherwise recompile the kernel with it:
```
sudo apt install linux-source linux-headers-$(uname -r) build-essential libncurses-dev pahole
mkdir ~/kernel; cd ~/kernel
tar -xaf /usr/src/linux-source-*.tar.xz
cd linux-source*
yes '' | make localmodconfig
# configure gpio-sim here
make menuconfig
make -j$(nproc)
sudo make modules_install
sudo make install
```

Next install a Python 3.10:
```
sudo apt install wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar xzf Python-3.10.14.tgz
cd Python-3.10.14
./configure --enable-optimizations
sudo make altinstall
```

sudo apt update && sudo apt install libopus-dev libvpx-dev
sudo python3.10 -m pip install -r requirements.txt