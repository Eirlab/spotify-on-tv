# Spotify on TV

Client de l'API Spotify pour afficher la musique en cours dans Eirlab

## Installation

```bash
git clone https://github.com/eirlab/spotify-on-tv
cd spotify-on-tv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Une fois l'installation faite, éditer le fichier `app.py` pour remplacer les valeurs suivantes :
- `client_id`
- `client_secret`
- `refresh_token` (optionnel)

## Utilisation
```bash
python3 ./app.py
```

## Création du service

Pour lancer le serveur au démarrage de la raspberry, installer le service `spotify.service` :
```bash
sudo cp spotify.service /etc/systemd/system/
sudo systemctl enable /etc/systemd/system/spotify.service
sudo systemctl start spotify.service
```
