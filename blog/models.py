from django.db import models
from django.utils import timezone
from django.conf import settings
from tinymce.models import HTMLField
from stdimage.models import StdImageField


class Post(models.Model):
    """
    Here we'll define our Post model
    """

    # author is linked to a registered
    # user in the 'auth_user' table.
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = HTMLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)  # Record how often a post is seen
    category = models.CharField(max_length=100, blank=True, null=True)
    image = StdImageField(upload_to="images/user_profiles",
                          variations={
                              'medium': {'width': 400, 'height': 400},
                          },
                          blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title
