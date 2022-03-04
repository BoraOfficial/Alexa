echo "Root access required"
cd ~/Desktop
echo "Installing Alexa source code..."
git clone https://github.com/BoraOfficial/Alexa
cd Alexa/
rm README.md
echo "Installing libraries for Alexa to work properly..."
cd /
sudo apt update
sudo apt-get install -y imagemagick
sudo apt install -y ffmpeg
echo "Putting the Alexa in startup..."
cd /etc/profile.d/
echo "python ~/Desktop/Alexa/Alexa.py" > Alexa.sh
echo "Starting Alexa.."
python ~/Desktop/Alexa/Alexa.py