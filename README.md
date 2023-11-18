# Music recommendation app

This app uses spotify API to recommend music based on user inputs such as track, artist, genre or liked songs.

## Setup

### Install software components

In order to use this app, you have to install [Python](https://www.python.org/downloads/), pip and dependencies given in 'requirements.txt'. After installing Python, set up pip:
```bash
# Windows
python -m pip install --user pip
# Linux
sudo apt install python3-pip
``` 
Next, run the command below for installing required Python packages: 
```bash
pip install -r requirements.txt
``` 

### Set environment variables

After installing required packages, you have to set environment variables for client authentication. Contact the owner of this repository for authentication keys! If you have the keys, set the environment variables as follows:
```bash
# Windows
setx SPOTIFY_CLIENT_ID "<client_id>"
setx SPOTIFY_CLIENT_SECRET "<client_secret>"
# Linux
echo 'export SPOTIFY_CLIENT_ID="<client_id>"' >> ~/.bashrc
echo 'export SPOTIFY_CLIENT_SECRET="<client_secret>"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

If everything was configured, navigate to the project directory and start the app by running main.py: 
```bash
# Windows
py main.py
# Linux
python3 main.py
```