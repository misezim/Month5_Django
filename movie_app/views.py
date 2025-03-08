from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .serializers import DirectorDetailSerializer, MovieDetailSerializer, ReviewDetailSerializer


@api_view(http_method_names = ['GET'])
def director_list_api_view(request):
    director = Director.objects.all()
    data = DirectorSerializer(instance=director, many=True).data
    return Response(data=data)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data = {'error': 'Director not found'},
                        status = status.HTTP_404_NOT_FOUND)
    data = DirectorDetailSerializer(director, many = False).data
    return Response(data = data)

#<<<-------->>>

@api_view(http_method_names = ['GET'])
def movie_list_api_view(request):
    movie = Movie.objects.all()
    data = MovieSerializer(instance=movie, many=True).data
    return Response(data=data)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data = {'error': 'Movie not found'},
                        status = status.HTTP_404_NOT_FOUND)
    data = MovieDetailSerializer(movie, many = False).data
    return Response(data = data)


#<<<-------->>>

@api_view(http_method_names = ['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    data = ReviewSerializer(instance=review, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data = {'error': 'Movie not found'},
                        status = status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many = False).data
    return Response(data = data)