# flaskAPI
to create new audio
(method=POST) http://127.0.0.1:5000/
example for creating song: 
{
  "fileType":"song",
  "fileMetaData":{
    "song name" :"somename",
    "duration":123,
    }
 }
 
example for creating podcast:
{
  "fileType":"podcast",
  "fileMetaData":{
    "podcast name":"anyname",
    "duration":123,
    "participants":"any participant name"
  }
}
example for creating audio book:
{
  "fileType":"audiobook",
  "fileMetaData":{
  "title":"title_name",
  "author":"author_name",
  "narrator":"narrator_name",
  "duration":123
  }
}

To read all songs
(method=GET) http://127.0.0.1:5000/song
to read single song details
(method=GET) http://127.0.0.1:5000/song/id

to read all podcasts
(method=GET) http://127.0.0.1:5000/podcast
to read single podcast details
(method=GET) http://127.0.0.1:5000/podcast/id

to read all audiobooks
(method=GET) http://127.0.0.1:5000/audiobook
to read single audio book details
(method=GET) http://127.0.0.1:5000/audiobook/id

to update any song
(method=PUT) http://127.0.0.1:5000/song/id

to update any podcast
(method=PUT) http://127.0.0.1:5000/podcast/id

to update any audiobook
(method=PUT) http://127.0.0.1:5000/audiobook/id

to delete any song
(method=DELETE) http://127.0.0.1:5000/song/id

to delete any podcast
(method=DELETE) http://127.0.0.1:5000/podcast/id

to delete any audiobook
(method=DELETE) http://127.0.0.1:5000/audiobook/id
