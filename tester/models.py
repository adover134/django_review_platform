import datetime

from django.db import models


class User(models.Model):
    u_id = models.CharField(primary_key=True, max_length=20)
    u_nickname = models.TextField()
    u_email = models.EmailField(unique=True)
    u_access_token = models.TextField(null=True)
    u_warn_count = models.IntegerField(default=0)
    u_active = models.IntegerField(default=0)
    penalty_date = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return '%s/%s' % (self.u_nickname, self.u_email)


class Manager(models.Model):
    u_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    m_tel = models.TextField()


class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    address = models.TextField()
    real_estate_agency = models.TextField()


class Review(models.Model):
    rev_id = models.IntegerField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='writer', null=True)
    r_id = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='room', null=True)
    review = models.TextField()


class Icon(models.Model):
    rev_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='icons')
    icon_x = models.IntegerField()
    icon_y = models.IntegerField()


class Option(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='options')
    option_name = models.TextField()
