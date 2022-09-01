from django.contrib import admin

from core import models





class BibleVerseAdmin(admin.ModelAdmin):
    ordering = ["book", "chapter", "verse"]
    list_display = ["book", "chapter", "verse"]
    search_fields = ["book", "chapter", "verse"]

    class Meta:
        model = models.BibleVerseModel

admin.site.register(models.BibleVerseModel, BibleVerseAdmin)
