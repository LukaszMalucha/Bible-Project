from rest_framework import filters
from rest_framework import views, viewsets, status, mixins
from core.models import BibleVerseModel
from core.permissions import IsAdminOrReadOnly
from search import serializers
from rest_framework.response import Response
import pandas as pd


class BibleVerseViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = serializers.BibleVerseModelSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("book", "chapter", "verse", "text")
    ordering_fields = "__all__"
    queryset = BibleVerseModel.objects.order_by("id")

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class KeywordSearch(views.APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self,request, keyword):
        queryset = BibleVerseModel.objects.filter(text__icontains=f" {keyword} ").values("book", "chapter", "verse", "text").order_by("id")
        verse_count = queryset.count()

        return Response({"verse_count": verse_count, "results": queryset}, status=status.HTTP_200_OK)


class BookSearch(views.APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, book):
        queryset = BibleVerseModel.objects.filter(book = book).values("book", "chapter", "verse",
                                                                                         "text").order_by("id")

        dataset = pd.DataFrame(list(queryset), columns=["book", "chapter", "verse", "text"])

        chapters = sorted(dataset['chapter'].value_counts(dropna=False).keys().tolist())
        chapter_dict = {}
        for ch in chapters:
            chapter = dataset[dataset["chapter"] == ch]
            chapter_text = chapter['text'].tolist()
            chapter_text = (" ").join(chapter_text)
            chapter_dict[ch] = chapter_text



        return Response({"chapter_dict": chapter_dict, }, status=status.HTTP_200_OK)










