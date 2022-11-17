from django.contrib import admin
from DBs import models as md

# Register your models here.
admin.site.register(md.User)
admin.site.register(md.Room)
admin.site.register(md.Review)
admin.site.register(md.Icon)
admin.site.register(md.Recommend)
admin.site.register(md.Report)
admin.site.register(md.ReviewImage)
admin.site.register(md.RoomImage)
