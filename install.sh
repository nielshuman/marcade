cd /home/niels/marcade
git pull
pip install flask_socketio sounddevice --break-system-packages
sudo apt install python3-flask python3-eventlet python3-selenium python3-waitress python3-soundfile chromium-browser chromium-chromedriver libportaudio2 -y
cp -f shit/marcade.desktop ~/.config/autostart/
echo "Copied marcade.desktop to ~/.config/autostart/"
sudo dpkg -i -EG shit/antimicrox-3.3.4-aarch64.deb