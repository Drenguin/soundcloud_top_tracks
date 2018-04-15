from flask import Flask
from flask import render_template
from flask import request
import scquery

app = Flask(__name__)

@app.route('/')
def loadHomepage():
    return render_template("search_artist.html")

@app.route('/search/results')
def loadSearchResults():
    searchName = request.args.get('artistName')
    artistsResponse = scquery.getUsersForName(searchName)
    for artist in artistsResponse:
        # The ',' option signals the use of a comma for a thousands separator.
        artist.followers_count = "{:,}".format(artist.followers_count)
    return render_template("search_artist_results.html", searchName=searchName, artists=artistsResponse)

@app.route('/artist/<artistname>')
def loadArtist(artistname):
    artistResponse, tracksResponse = scquery.getTopTracks(artistname)
    for track in tracksResponse:
        # The ',' option signals the use of a comma for a thousands separator.
        track.playback_count = "{:,}".format(track.playback_count)
    return render_template("artist.html", artist=artistResponse, tracks=tracksResponse)

if __name__ == "__main__":
    app.run()