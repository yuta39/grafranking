from django.db import models

class VoteEvent(models.Model):
    '''投票自体に関する情報'''
    name = models.CharField(u'投票イベント名', max_length=255)
    startTimeDate = models.DateTimeField()

    def __str__(self):
        return self.name


class Individual(models.Model):
    '''参加者に関する情報'''
    event = models.ForeignKey(VoteEvent, verbose_name=u'投票イベント', related_name='impressions')
    member_name = models.CharField(u'個人名',max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.member_name
