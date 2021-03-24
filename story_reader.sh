#!/bin/sh

echo "Mongdb URI"
export MONGO_URI="mongodb://localhost:27017/story"

echo "Import Path"
export IMPORT_PATH="/home/vetrivel/story"

echo "Flask"
export FLASK_APP="application.py"
