from unicodedata import category

from rest_framework import serializers
from . import models
from rest_framework. exceptions import ValidationError

from .models import Director, Movie


#<<<------------------------------List View-------------------------->>>
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
    class Meta:
        model = models.Review
        fields = 'text points'.split(' ')


#<<<------------------------------Detail View-------------------------->>>
class DirectorDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(source='movie_set', many=True)

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

#<<<------------------------------Validation-------------------------->>>
class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=3)

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=3)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(min_value=3)
    director_id = serializers.IntegerField(min_value=1)
    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist')
        return director_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    movie_id = serializers.IntegerField(min_value=1)
    points = serializers.IntegerField(max_value=5, min_value=1)
    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie does not exist')
        return movie_id