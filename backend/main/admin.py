from django.contrib import admin
from .models import Resource,Subject, Profile, Question,Reply,ImageQuestion,ImageReply




admin.site.register(Subject)
admin.site.register(Resource)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(ImageQuestion)
admin.site.register(ImageReply)