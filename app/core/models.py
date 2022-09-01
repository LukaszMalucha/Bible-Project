from django.db import models


class BibleVerseModel(models.Model):
    """Model for Document"""
    book = models.CharField(max_length=254, default="Not Specified", blank=True)
    chapter = models.IntegerField(blank=False, default=0)
    verse = models.IntegerField(blank=False, default=0)
    text = models.TextField(max_length=254, default="Not Specified", blank=True)


    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Bible Verses"

    def __str__(self):
        return str(self.book) + " " + str(self.chapter) + " " + str(self.verse)