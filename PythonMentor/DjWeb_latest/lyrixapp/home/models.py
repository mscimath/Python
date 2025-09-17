from django.db import models

# Data models
class Lyric(models.Model):
    title = models.CharField(max_length=100)
    lyric = models.TextField()
    mood = models.DecimalField(max_digits=10, decimal_places=2) #a value for mood to be entered by a user (1- depressing, 5-realistic, 10- positive), the scale to be later calculated and output as a color of a song and categorised
