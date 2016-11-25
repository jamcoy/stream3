from django.contrib import admin
from .models import Subject, Thread, Post, Poll, PollSubject, PollVote

admin.site.register(Subject)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Poll)
admin.site.register(PollSubject)
admin.site.register(PollVote)
