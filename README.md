# Spotify on TV

Client de l'API Spotify pour afficher la musique en cours dans Eirlab

## Installation

```bash
git clone https://github.com/eirlab/spotify-on-tv
cd spotify-on-tv
python3 -m venv venv # optionnel
source venv/bin/activate # optionnel
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