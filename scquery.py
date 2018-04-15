import sys
import soundcloud

client = soundcloud.Client(client_id="4jkoEFmZEDaqjwJ9Eih4ATNhcH3vMVfp")

def getTopTracks(artistURLName):
    # Resolve the english text user to a numeric id
    artistObject = client.get('/resolve', url="https://soundcloud.com/"+artistURLName)
    artistId = artistObject.id

    allTracks = []

    tracks = client.get('/users/'+str(artistId)+'/tracks', order='created_at', limit=50, linked_partitioning=1)
    allTracks.extend(tracks.collection)
    while tracks.next_href is not None:
        tracks = client.get(tracks.next_href, order='created_at', limit=50, linked_partitioning=1)
        allTracks.extend(tracks.collection)

    allTracks.sort(key=lambda track: track.playback_count, reverse=True)
    return artistObject, allTracks

def getUsersForName(name):
    users = client.get('/search/users', q=name)
    return users.collection

if __name__ == "__main__":
    # Parse command line inputs
    artistUrlName = sys.argv[1]
    tracks = getTopTracks(artistUrlName)
    for track in tracks:
        print(track.user["username"]+": "+track.title+" - "+str(track.playback_count) + " - " + str(track.permalink_url))
