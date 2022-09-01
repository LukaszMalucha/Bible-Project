from core.models import BibleVerseModel


def dataset_documents_upload(dataset):
    """Upload documents to database"""
    count_new = 0
    for document in dataset.itertuples():

            document = BibleVerseModel.objects.create(
                book = document.book,
                chapter = document.chapter,
                verse=document.verse,
                text=document.text,

            )
            count_new += 1


    report = {"count_new": count_new }

    return report
