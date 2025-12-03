from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# File paths
SONGS_FILE = "songs.json"
ARTISTS_FILE = "artists.json"

# Helper functions to load/save data
def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Initialize data
songs = load_data(SONGS_FILE)
artists = load_data(ARTISTS_FILE)

@app.route("/")
def home():
    return "Home"

# Get Requests

@app.route("/songs")
def get_songs():
    return jsonify(songs), 200

@app.route("/songs/<int:song_id>")
def get_song(song_id):
    for song in songs:
        if song["id"] == song_id:
            return jsonify(song), 200
    return jsonify({"error": "Song not found"}), 404

@app.route("/artists")
def get_artists():
    return jsonify(artists), 200

@app.route("/artists/<int:artist_id>")
def get_artist(artist_id):
    for artist in artists:
        if artist["id"] == artist_id:
            return jsonify(artist), 200
    return jsonify({"error": "Artist not found"}), 404

# Post Requests

@app.route("/songs", methods=["POST"])
def create_song():
    data = request.get_json()
    new_id = len(songs) + 1
    data["id"] = new_id
    songs.append(data)
    return jsonify(data), 201

@app.route("/artists", methods=["POST"])
def create_artist():
    data = request.get_json()
    new_id = len(artists) + 1
    data["id"] = new_id
    artists.append(data)
    return jsonify(data), 201

# Put Requests

@app.route("/songs/<int:song_id>", methods =["PUT"])
def replace_song(song_id):
    data = request.get_json()
    for i, song in enumerate(songs):
        if song["id"] == song_id:
            songs[i] = data
            data["id"] = song_id
            return jsonify({"message": "Song replaced"}), 200
    return jsonify({"error": "Song not found"}), 404

@app.route("/artists/<int:artist_id>", methods =["PUT"])
def replace_artist(artist_id):
    data = request.get_json()
    for i, artist in enumerate(artists):
        if artist["id"] == artist_id:
            artists[i] = data
            data["id"] = artist_id
            return jsonify({"message": "Artist replaced"}), 200
    return jsonify({"error": "Artist not found"}), 404

# Patch Requests

@app.route("/songs/<int:song_id>", methods=["PATCH"])
def update_song(song_id):
    data = request.get_json()
    for song in songs:
        if song["id"] == song_id:
            song.update(data)
            return jsonify({"message": "Song updated", "song": song}), 200
    return jsonify({"error": "Song not found"}), 404

@app.route("/artists/<int:artist_id>", methods=["PATCH"])
def update_artist(artist_id):
    data = request.get_json()
    for artist in artists:
        if artist["id"] == artist_id:
            artist.update(data)
            return jsonify({"message": "Artist updated", "artist": artist}), 200
    return jsonify({"error": "Artist not found"}), 404

# Delete Requests

@app.route("/songs/<int:song_id>", methods=["DELETE"])
def delete_song(song_id):
    for song in songs:
        if song["id"] == song_id:
            songs.remove(song)
            return jsonify({"message": f"Song with id {song_id} deleted"}), 200
    return jsonify({"error": "Song not found"}), 404

@app.route("/artists/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    for artist in artists:
        if artist["id"] == artist_id:
            artists.remove(artist)
            return jsonify({"message": f"Artist with id {artist_id} deleted"}), 200
    return jsonify({"error": "Artist not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)