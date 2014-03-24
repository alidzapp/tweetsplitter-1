from django.db import models

class Members(models.Model):
    twitter_screen_name = models.CharField(max_length=100)
    twitter_fullname = models.CharField(max_length=100)
    twitter_id = models.IntegerField()
    access_token_key = models.CharField(max_length=50)
    access_token_secret = models.CharField(max_length=50)
    profile_picture = models.URLField()

    def __unicode__(self):
        return "{0} - {1}".format(self.twitter_fullname, self.twitter_screen_name)

class Members_Data(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    last_login = models.DateTimeField(auto_now=True)
    members = models.ForeignKey(Members)