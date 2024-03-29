import datetime
import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uWarnCount = models.IntegerField(default=0)
    uActive = models.IntegerField(default=0)
    penaltyDate = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'User'


class Room(models.Model):
    address = models.TextField()
    postcode = models.IntegerField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    buildingFloorNum = models.IntegerField(null=True, blank=True)
    builtYear = models.IntegerField(null=True, blank=True)
    commonInfo = models.JSONField(null=True, blank=True)
    ownerPhone = models.TextField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True) # 100미터 단위, 학교 도서관까지 거리
    convNum = models.IntegerField(null=True, blank=True) # 반경 100미터 이내 편의점 수

    class Meta:
        db_table = 'Room'


class Review(models.Model):
    uId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='writer')
    roomId = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='whichRoom')
    reviewTitle = models.CharField(max_length=50)
    reviewDate = models.DateField(default=datetime.date.today)
    reviewSentence = models.JSONField()
    rent = models.IntegerField(null=True)                #전세: 0 / 월세: 1 (구분)
    deposit = models.IntegerField(null=True)             #보증금(전세/월세)
    monthlyRent = models.IntegerField(null=True)         #월세
    roomSize = models.FloatField(null=True)              #제곱미터
    humidity = models.IntegerField(             #습도
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    soundproof = models.IntegerField(            #방음
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    lighting = models.IntegerField(             #채광
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    cleanliness = models.IntegerField(          #청결도
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)])

    class Meta:
        db_table = 'Review'


class Icon(models.Model):
    reviewId = models.ForeignKey(Review, null=True, on_delete=models.CASCADE, related_name='includedIcon')
    iconKind = models.TextField()
    changedIconKind = models.TextField()

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


class ReviewImage(models.Model):
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='additionalImage')
    image = models.TextField(null=True)

    class Meta:
        db_table = 'ReviewImage'

    def __str__(self):
        return self.image

    def delete(self):
        print(self.image)
        delete_review_image(self.image)
        return models.Model.delete(self)


class RoomImage(models.Model):
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomImage')
    image = models.TextField(null=True)

    class Meta:
        db_table = 'RoomImage'

    def __str__(self):
        return self.image


    def delete(self):
        print(self.image)
        delete_review_image(self.image)
        return models.Model.delete(self)


def delete_review_image(image):
    if os.path.exists(os.path.join('static/images/reviewImage',image)):
        os.remove('static/images/reviewImage/'+image)


def delete_room_image(image):
    if os.path.exists(os.path.join('static/images/roomImage' + image)):
        os.remove('static/images/roomImage/' + image)
