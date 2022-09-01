import pandas as pd
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from core.models import BibleVerseModel
from db_manager.data_upload import dataset_documents_upload
from db_manager.data_validation import documents_dataset_check


@user_passes_test(lambda u: u.is_staff)
def db_manager(request):
    return render(request, "db-manager.html")


@user_passes_test(lambda u: u.is_superuser)
def documents_upload(request):
    """Document dataset upload to database"""
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            critical_error = "Incorrect file format. Please upload CSV file"
            return render(request, "documents.html",
                          {"critical_error": critical_error, })
        data = pd.read_csv(csv_file, encoding="utf-8-sig")
        dataset_errors = documents_dataset_check(data)

        if len(dataset_errors) == 0:
            # try:
            report = dataset_documents_upload(data)
            # except:
            #     critical_error = "Dataset upload wasn't successful due to error"
            #     return render(request, "documents.html",
            #                   {"critical_error": critical_error, })

            upload_report = report
            return render(request, "documents.html",
                          {"upload_report": upload_report})
        else:
            return render(request, "documents.html",
                          {"dataset_errors": dataset_errors})

    return render(request, "documents.html")



@user_passes_test(lambda u: u.is_superuser)
def delete_data(request):
    """Delete weekly uploads"""
    years = [ '2020', ]
    weeks = list(range(1, 53))

    if request.method == "POST":
        year = request.POST['year']
        week = request.POST['week']
        queryset = BibleVerseModel.objects.filter(year=year, week=week)
        count = queryset.count()
        if count > 0:
            queryset.delete()
            message = f" Year {year}, week {week} - documents were deleted successfully ({count})."
        else:
            message = f" No document for year {year}, week {week} has been found."

        return render(request, "delete.html",
                      {"message": message, "years": years, "weeks": weeks})

    return render(request, "delete.html", {"years": years, "weeks": weeks})
