from flask import Flask, jsonify, request

app = Flask(__name__)

songs = {
    1: {"name": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock"},
    2: {"name": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop"}
}
playlists = {
    1: {"name": "My Favorites", "songs": [1, 2]}
}

# ----------------------------- Song Endpoints -----------------------------

# 1. Create Song
@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    song_id = len(songs) + 1 
    songs[song_id] = data
    return jsonify({'id': song_id, 'message': 'Song created successfully'}), 201

# 2. Update Song
@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id in songs:
        data = request.get_json()
        songs[song_id] = data
        return jsonify({'message': 'Song updated successfully'}), 200
    else:
        return jsonify({'message': 'Song not found'}), 404

# 3. Delete Song
@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id in songs:
        del songs[song_id]
        return jsonify({'message': 'Song deleted successfully'}), 200
    else:
        return jsonify({'message': 'Song not found'}), 404

# 4. Search/Get a Song (by ID)
@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    if song_id in songs:
        return jsonify(songs[song_id]), 200
    else:
        return jsonify({'message': 'Song not found'}), 404

# ----------------------------- Playlist Endpoints -----------------------------

# 1. Create Playlist
@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    playlist_id = len(playlists) + 1 
    playlists[playlist_id] = {'name': data['name'], 'songs': []} 
    return jsonify({'id': playlist_id, 'message': 'Playlist created successfully'}), 201

# 2. Get Playlist
@app.route('/playlists/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    if playlist_id in playlists:
        return jsonify(playlists[playlist_id]), 200
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# 3. Update Playlist (e.g., change name)
@app.route('/playlists/<int:playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    if playlist_id in playlists:
        data = request.get_json()
        playlists[playlist_id]['name'] = data['name'] 
        return jsonify({'message': 'Playlist updated successfully'}), 200
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# 4. Delete Playlist
@app.route('/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id in playlists:
        del playlists[playlist_id]
        return jsonify({'message': 'Playlist deleted successfully'}), 200
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# ----------------------------- Additional Endpoints -----------------------------

# 1. Add Song to Playlist
@app.route('/playlists/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    if playlist_id in playlists:
        data = request.get_json()
        song_id = data['song_id']
        if song_id in songs: 
            playlists[playlist_id]['songs'].append(song_id)
            return jsonify({'message': 'Song added to playlist successfully'}), 200
        else:
            return jsonify({'message': 'Song not found'}), 404
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# 2. Remove Song from Playlist
@app.route('/playlists/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    if playlist_id in playlists:
        if song_id in playlists[playlist_id]['songs']:
            playlists[playlist_id]['songs'].remove(song_id)
            return jsonify({'message': 'Song removed from playlist successfully'}), 200
        else:
            return jsonify({'message': 'Song not found in playlist'}), 404
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# 3. Sort Songs in Playlist
@app.route('/playlists/<int:playlist_id>/sort', methods=['POST'])
def sort_playlist(playlist_id):
    if playlist_id in playlists:
        data = request.get_json()
        sort_by = data.get('sort_by', 'name')  # Default to sorting by 'name'

        def get_song_attribute(song_id, attr):
            return songs[song_id].get(attr, '')  # Handle missing attributes

        if sort_by in ['name', 'genre', 'artist']:
            playlists[playlist_id]['songs'].sort(key=lambda x: get_song_attribute(x, sort_by))
            return jsonify({'message': 'Playlist sorted successfully'}), 200
        else:
            return jsonify({'message': 'Invalid sort criteria'}), 400
    else:
        return jsonify({'message': 'Playlist not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)