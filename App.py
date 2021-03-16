from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, inputs, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

ma=Marshmallow(app)

#creating models

#Song model
class Song(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   songName = db.Column(db.String(100), nullable=False)
   songDuration = db.Column(db.Integer, nullable=False)
   uploadTime = db.Column(db.DateTime, nullable=False)

   def __init__(self, songName,songDuration,uploadTime):
      self.songName=songName
      self.songDuration=songDuration
      self.uploadTime=uploadTime

#Podcast Model
class Podcast(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   podcastName = db.Column(db.String(100), nullable=False)
   podcastDuration = db.Column(db.Integer, nullable=False)
   uploadTime = db.Column(db.DateTime, nullable=False)
   participants = db.Column(db.String(100),nullable=True)

   def __init__(self,podcastName,podcastDuration,uploadTime,participants):
      self.podcastName = podcastName
      self.podcastDuration = podcastDuration
      self.uploadTime = uploadTime
      self.participants = participants
      

# class Participants(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    participant = db.Column(db.String(100),nullable=False)
#    podcastid = db.Column(db.Integer,db.ForeignKey('podcast.id'))
   


#AudioBook Model
class AudioBook(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100))
      author = db.Column(db.String(100))
      narrator = db.Column(db.String(100))
      duration = db.Column(db.Integer, nullable=False)
      uploadTime = db.Column(db.DateTime, nullable=False)

      def __init__(self, title, author, narrator, duration, uploadTime):
         self.title = title
         self.author = author
         self.narrator = narrator
         self.duration = duration
         self.uploadTime = uploadTime

db.create_all()

# CREATING SCHEMAS

# Song Model Schema
class SongSchema(ma.Schema):
   class Meta:
      fields = ('id', 'songName', 'songDuration', 'uploadTime')

# PODCAST MODEL SCHEMA
class PodcastSchema(ma.Schema):
   class Meta:
      fields = ('id', 'podcastName', 'podcastDuration',
                'uploadTime', 'participants')
class PartSchema(ma.Schema):
   class Meta:
      fields = ('id', 'participant')

# audio  Book Model Schema

class AudioBookSchema(ma.Schema):
   class Meta:
      fields = ('id', 'title', 'author', 'narrator', 'duration', 'uploadTime')


# INIT SCHEMAS
song_schema = SongSchema()
songs_schema = SongSchema(many=True)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)
partschema = PartSchema()
parts = PartSchema(many=True)
book_schema = AudioBookSchema()
books_schema = AudioBookSchema(many=True)

#creating audio files
@app.route('/', methods=['POST'])
def createAudio():
   fileType = request.json['fileType']
   if(fileType == 'song'):

       fileMetaData = request.json['fileMetaData']
       
       songName = fileMetaData['song name']
       songDuration = fileMetaData['duration']
       uploadTime = datetime.now()
       new_song = Song(songName, songDuration, uploadTime)
       db.session.add(new_song)
       db.session.commit()
       return partschema.jsonify(part)

   elif(fileType=='podcast'):
      fileMetaData = request.json['fileMetaData']
      podcastName = fileMetaData['podcast name']
      podcastDuration = fileMetaData['duration']
      participant = fileMetaData['participants']
      uploadTime = datetime.now()
      new_podcast = Podcast(podcastName, podcastDuration,uploadTime,participant)
      
      
      db.session.add(new_podcast)
      db.session.commit()
      return podcast_schema.jsonify(new_podcast)

   elif(fileType=='audiobook'):
      fileMetaData=request.json['fileMetaData']
      title = fileMetaData['title']
      author = fileMetaData['author']
      narrator = fileMetaData['narrator']
      duration = fileMetaData['duration']
      uploadTime = datetime.now()
      new_book = AudioBook(title,author,narrator,duration,uploadTime)
      db.session.add(new_book)
      db.session.commit()
      return book_schema.jsonify(new_book) , 200

   else:
      return 400


@app.route('/', methods=['GET'])
def index():
   
   return 404

#get all audio
@app.route('/<string:audioType>',methods=['GET'])
def getAudios(audioType):
   if(audioType=='song'):
      all_songs=Song.query.all()
      return songs_schema.jsonify(all_songs), 200

   elif(audioType=='podcast'):
      all_podcast = Podcast.query.all()
      return podcasts_schema.jsonify(all_podcast), 200

   elif(audioType=='audiobook'):
      all_books=AudioBook.query.all()
      result=books_schema.dump(all_books)
      return books_schema.jsonify(all_books), 200

   else:
      return 404


 #get single audio


@app.route('/<string:audioType>/<id>', methods=['GET'])
def getAudioById(audioType,id):
   if(audioType == 'song'):
      single_song = Song.query.get(id)
      return song_schema.jsonify(single_song), 200

   elif(audioType == 'podcast'):
      single_podcast = Podcast.query.get(id)
      return podcast_schema.jsonify(single_podcast), 200

   elif(audioType == 'audiobook'):
      single_book = AudioBook.query.get(id)
      return book_schema.jsonify(single_book), 200

   else:
      return 404


#update audio by audio type and id


@app.route('/<string:audioType>/<id>', methods=['PUT'])
def updateAudioById(audioType, id):
   if(audioType == 'song'):
      single_song = Song.query.get(id)
      songName = request.json['songName']
      duration = request.json['songDuration']
      uploadTime = datetime.now()

      single_song.songName = songName
      single_song.songDuration = duration
      single_song.uploadTime = uploadTime

      db.session.commit()
   
      return song_schema.jsonify(single_song), 200

   elif(audioType == 'podcast'):
      single_podcast = Podcast.query.get(id)
      podcastName = request.json['podcastName']
      duration = request.json['podcastDuration']
      uploadTime = datetime.now()
      participant = request.json['participants']

      single_podcast.podcastName = podcastName
      single_podcast.podcastDuration = duration
      single_podcast.uploadTime = uploadTime
      single_podcast.participants = participant

      db.session.commit()
      return podcast_schema.jsonify(single_podcast), 200

   elif(audioType == 'audiobook'):
      single_book = AudioBook.query.get(id)
      title = request.json['title']
      author = request.json['author']
      narrator = request.json['narrator']
      duration = request.json['duration']
      uploadTime = datetime.now()

      single_book.title = title
      single_book.author = author
      single_book.narrator = narrator
      single_book.duration = duration
      single_book.uploadTime = uploadTime

      db.session.commit()
      
      return book_schema.jsonify(single_book), 200

   else:
      return '404 bad request'

#delete audio by audio type and id


@app.route('/<string:audioType>/<id>', methods=['DELETE'])
def deleteAudioById(audioType, id):
   if(audioType == 'song'):
      single_song = Song.query.get(id)
      db.session.delete(single_song)
      db.session.commit()
      return 'deleted successfully'

   elif(audioType == 'podcast'):
      single_podcast = Podcast.query.get(id)
      db.session.delete(single_podcast)
      db.session.commit()
      return 'deleted successfully'

   elif(audioType == 'audiobook'):
      single_book = AudioBook.query.get(id)
      db.session.delete(single_book)
      db.session.commit()
      return 'deleted successfully'

   else:
      return 404


if __name__ == "__main__":
    app.run(debug=True)
