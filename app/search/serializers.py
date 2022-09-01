from rest_framework import serializers

from core.models import BibleVerseModel


class BibleVerseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BibleVerseModel
        fields = "__all__"
        read_only_fields = ("id",)