from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Description', blank=True)
    duration =models.PositiveIntegerField(verbose_name="Duration")
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

POINTS = (
    (i, str(i)) for i in range(1, 6)
)
class Review(models.Model):
    text = models.TextField(verbose_name='Review')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    points = models.IntegerField(choices=POINTS, default=5)

    def __str__(self):
        return self.movie.title