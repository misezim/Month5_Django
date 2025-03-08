from rest_framework import serializers
from . import models

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField(source='director.name')
    class Meta:
        model = models.Movie
        fields = 'title duration director'.split(' ')

class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title')

    class Meta:
        model = models.Review
        fields = '__all__'





class DirectorDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(source='movie_set', many=True, read_only=True)
    class Meta:
        model = models.Director
        fields = ['id', 'name', 'movies']

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title')
    class Meta:
        model = models.Review
        fields = '__all__'