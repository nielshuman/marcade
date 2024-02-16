cd ~/marcade
sudo apt update
sudo apt install git git-lfs -y
git pull
git lfs pull

pip install flask_socketio PyOpenAL --break-system-packages
sudo apt install python3-flask python3-eventlet python3-selenium python3-yaml python3-waitress chromium-browser chromium-chromedriver libportaudio2 -y

mkdir -p ~/.config/autostart
cp -f shit/marcade.desktop ~/.config/autostart/
cp -f shit/marcade.desktop ~/.local/share/applications/
cp -f shit/update.desktop ~/.local/share/applications/
cp -f shit/home.desktop ~/.local/share/applications/

sudo dpkg -i -EG shit/antimicrox-3.3.4-aarch64.deb
sudo apt install -f -y
chmod +x home.sh
# only do this is files are not identical
if ! cmp -s shit/wait.png /usr/share/plymouth/themes/pix/splash.png; then
    echo "Applying splash screen"
    sudo cp -f shit/wait.png /usr/share/plymouth/themes/pix/splash.png
    sudo plymouth-set-default-theme --rebuild-initrd pix
fi