from core.models import BibleVerseModel


def dataset_documents_upload(dataset):
    """Upload documents to database"""
    # for row in BibleVerseModel.objects.all().reverse():
    #     if BibleVerseModel.objects.filter(book = row.book,chapter = row.chapter,verse=row.verse).count() > 1:
    #         row.delete()


    count_new = 0
    for document in dataset.itertuples():

            if BibleVerseModel.objects.filter(book = document.book,chapter = document.chapter,verse=document.verse).exists():
                pass
            else:
                document = BibleVerseModel.objects.create(
                    book = document.book,
                    chapter = document.chapter,
                    verse=document.verse,
                    text=document.text,

                )
                count_new += 1

    print(count_new)
    report = {"count_new": count_new }

    return report
