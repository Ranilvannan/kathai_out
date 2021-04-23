#!/bin/sh

echo "Mongdb URI"
export MONGO_URI="mongodb://localhost:27017/story"

echo "Import Path"
export IMPORT_PATH="/var/story_reader/English"
export DATABASE="story"
export STORY="english_story"
export CATEGORY="english_category"
export LANGUAGE="English"

echo "Flask"
export FLASK_APP="application.py"
