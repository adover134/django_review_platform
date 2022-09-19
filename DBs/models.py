import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uWarnCount = models.IntegerField(default=0)
    uActive = models.IntegerField(default=0)
    penaltyDate = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'user_info'


class Manager(models.Model):
    uId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mTel = models.TextField()

    class Meta:
        db_table = 'manager'


class Room(models.Model):
    address = models.TextField()
    name = models.TextField(null=True)
    builtYear = models.IntegerField(max_length=5, null=True)
    commonInfo = models.JSONField(null=True)

    class Meta:
        db_table = 'Room'


class Review(models.Model):
    uId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='writer')
    roomId = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='whichRoom')
    reviewTitle = models.CharField(max_length=50)
    reviewDate = models.DateField(default=datetime.date.today)
    reviewKind = models.IntegerField()
    reviewSentence = models.JSONField()

    class Meta:
        db_table = 'Review'


class Icon(models.Model):
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='includedIcon')
    iconKind = models.TextField()
    changedIconKind = models.TextField()
    iconInformation = models.TextField()

    class Meta:
        db_table = 'Icon'

    def __str__(self):
        return self.iconKind


class Recommend(models.Model):
    uId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='recommender')
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='recommendedOn')

    class Meta:
        db_table = 'Recommend'


class Report(models.Model):
    uId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='reporter')
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reportedOn')

    class Meta:
        db_table = 'Report'


class CommonInfo(models.Model):
    commonInfoName = models.TextField()

    class Meta:
        db_table = 'CommonInfo'


class ReviewImage(models.Model):
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='additionalImage')
    image = models.TextField(null=True)

    class Meta:
        db_table = 'ReviewImage'

    def __str__(self):
        return self.image


class RoomImage(models.Model):
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomImage')
    image = models.TextField(null=True)

    class Meta:
        db_table = 'RoomImage'

    def __str__(self):
        return self.image
