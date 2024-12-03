from django.shortcuts import render

# Create your views here.
# text_similarity/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlagiarismReport, PlagiarismReportDetail
from file_manager.models import Folder, File
from .forms import FolderSelectionForm
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
from django.http import HttpResponse

@login_required
def select_folders(request):
    if request.method == 'POST':
        form = FolderSelectionForm(request.user, request.POST)
        if form.is_valid():
            folders = form.cleaned_data['folders']
            report = generate_plagiarism_report(request.user, folders)
            return redirect('view_report', report_id=report.id)
    else:
        form = FolderSelectionForm(request.user)

    user_reports = PlagiarismReport.objects.filter(user=request.user)
    
    return render(request, 'text_similarity/select_folders.html', {
        'form': form,
        'user_reports': user_reports
    })

def generate_plagiarism_report(user, folders):
    report = PlagiarismReport.objects.create(user=user, report_name="Plagiarism Report")
    files = File.objects.filter(folder__in=folders)
    
    texts = [open(f.text_file_path).read() for f in files if f.text_file_path]
    file_pairs = [(files[i], files[j]) for i in range(len(files)) for j in range(i + 1, len(files))]

    vectorizer = TfidfVectorizer().fit_transform(texts)
    vectors = vectorizer.toarray()
    
    for file1, file2 in file_pairs:
        text1 = open(file1.text_file_path).read()
        text2 = open(file2.text_file_path).read()
        similarity_score = cosine_similarity([vectors[list(files).index(file1)]], [vectors[list(files).index(file2)]])[0][0]
        PlagiarismReportDetail.objects.create(report=report, file1=file1, file2=file2, similarity_score=similarity_score)
    
    return report

@login_required
def view_report(request, report_id):
    report = PlagiarismReport.objects.get(id=report_id, user=request.user)
    details = report.details.all().order_by('-similarity_score')[:10]  # Top 10
    return render(request, 'text_similarity/view_report.html', {'report': report, 'details': details})

@login_required
def delete_report(request, report_id):
    report = PlagiarismReport.objects.get(id=report_id, user=request.user)
    report.delete()
    form = FolderSelectionForm()
    user_reports = PlagiarismReport.objects.filter(user=request.user)
    # messages.success(request, 'Report deleted successfully.')
    return render(request, 'text_similarity/select_folders.html', {
        'form': form,
        'user_reports': user_reports
    })

@login_required
def download_report_csv(request, report_id):
    report = PlagiarismReport.objects.get(id=report_id, user=request.user)
    details = report.details.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report.report_name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['File1', 'File2', 'Similarity Score'])

    for detail in details:
        writer.writerow([detail.file1.name, detail.file2.name, detail.similarity_score])

    return response
