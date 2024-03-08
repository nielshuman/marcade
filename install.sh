sudo apt update
pip install flask_socketio PyOpenAL --break-system-packages
sudo apt install git git-lfs python3-flask python3-eventlet python3-selenium python3-yaml python3-waitress chromium-browser chromium-chromedriver libportaudio2 -y

cd ~/marcade
git pull
git lfs pull

# sudo dpkg -i -EG shit/antimicrox-3.3.4-aarch64.deb
sudo dpkg -i -EG shit/input-remapper-2.0.1.deb
sudo apt install -f -y
mkdir -p ~/.config/autostart
cp -f shit/video.desktop ~/.config/autostart/
cp -f shit/marcade.desktop ~/.local/share/applications/
cp -f shit/update.desktop ~/.local/share/applications/
cp -f shit/home.desktop ~/.local/share/applications/
cp -f shit/video.desktop ~/.local/share/applications/
# only if ~/.config/input-remapper-2 does not already exist

if [ ! -L ~/.config/input-remapper-2 ]; then
    ln -s ~/marcade/inputremapper-config/ ~/.config/input-remapper-2
fi

chmod +x home.sh

# only do this is files are not identical
if ! cmp -s shit/wait.png /usr/share/plymouth/themes/pix/splash.png; then
    echo "Applying splash screen"
    sudo cp -f shit/wait.png /usr/share/plymouth/themes/pix/splash.png
    sudo plymouth-set-default-theme --rebuild-initrd pix
fi