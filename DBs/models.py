import datetime

from django.db import models


class User(models.Model):
    uId = models.CharField(primary_key=True, max_length=20)
    uNickname = models.TextField()
    uEmail = models.EmailField(unique=True)
    uAccessToken = models.TextField(null=True)
    uWarnCount = models.IntegerField(default=0)
    uActive = models.IntegerField(default=0)
    penaltyDate = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return '%s/%s' % (self.uNickname, self.uEmail)


class Manager(models.Model):
    uId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mTel = models.TextField()

    class Meta:
        db_table = 'manager'


class Room(models.Model):
    address = models.TextField()
    builtYear = models.CharField(max_length=5)
    commonInfo = models.JSONField()

    class Meta:
        db_table = 'Room'


class Review(models.Model):
    uId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='writer')
    roomId = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='whichRoom')
    reviewDate = models.DateField(default=datetime.date.today)
    reviewKind = models.IntegerField()
    reviewSentence = models.TextField()

    class Meta:
        db_table = 'Review'


class Icon(models.Model):
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='includedIcon')
    iconKind = models.TextField()
    iconInformation = models.TextField()

    class Meta:
        db_table = 'Icon'


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


class Image(models.Model):
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='additionalImage')
    image = models.ImageField()

    class Meta:
        db_table = 'Image'
