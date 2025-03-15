from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .serializers import DirectorDetailSerializer, MovieDetailSerializer, ReviewDetailSerializer
from django.db import transaction


@api_view(http_method_names = ['GET', 'POST'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        director = Director.objects.all()
        data = DirectorSerializer(instance=director, many=True).data
        for director in data:
            director['movies_count'] = director.get('id', 0)
            director['movies_count'] = Director.objects.get(id=director['id']).movie_set.count()
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')
        with transaction.atomic():
            director = Director.objects.create(
                name=name,
            )
            return Response(data=DirectorDetailSerializer(director).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data = {'error': 'Director not found'},
                        status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorDetailSerializer(director, many = False).data
        return Response(data = data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(data = {'error': 'Director deleted'}, status = status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.save()
        return Response(data = DirectorDetailSerializer(director, many = False).data, status = status.HTTP_201_CREATED)

#<<<-------->>>

@api_view(http_method_names = ['GET',"POST"])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        data = MovieSerializer(instance=movie, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        with transaction.atomic():
            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id
            )
            return Response(data=MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)

@api_view(['GET' , 'PUT' , 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data = {'error': 'Movie not found'},
                        status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieDetailSerializer(movie, many = False).data
        return Response(data = data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data = {'error': 'Movie deleted'}, status = status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(data = MovieDetailSerializer(movie).data, status = status.HTTP_201_CREATED)

#<<<-------->>>

@api_view(http_method_names = ['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(instance=review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        points = request.data.get('points')

        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                movie_id=movie_id,
                points=points
            )
            return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data = {'error': 'Movie not found'},
                        status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many = False).data
        return Response(data = data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(data = {'error': 'Review deleted'}, status = status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie_id')
        review.points = request.data.get('points')
        review.save()
        return Response(data = ReviewDetailSerializer(review).data, status = status.HTTP_201_CREATED)

@api_view(['GET'])
def movie_with_reviews_api_view(request):
    movies = Movie.objects.all()
    movie_data = []

    for movie in movies:
        reviews = movie.reviews.all()
        reviews_data = []
        if reviews.exists():
            reviews_data = ReviewSerializer(reviews, many=True).data
            total_points = sum([review['points'] for review in reviews_data])
            average_rating = total_points / len(reviews_data)
        else:
            reviews_data = []
            average_rating = None

        movie_info = MovieSerializer(movie).data
        movie_info['reviews'] = reviews_data
        movie_info['average_rating'] = average_rating

        movie_data.append(movie_info)

    return Response(movie_data)
