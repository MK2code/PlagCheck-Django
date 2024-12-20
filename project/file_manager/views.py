from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import the UserProfile model from your user app
from .models import Folder, File
from .forms import FileUploadForm
from django.contrib import messages
import pytesseract
import os
from django.http import JsonResponse

import pytesseract
from pdf2image import convert_from_path


def process_pdf_to_text(pdf_file, folder_name):
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )
    pdf_path = os.path.splitext(pdf_file.name)
    pdf_name = pdf_path[0]
    images = convert_from_path(pdf_file.temporary_file_path(),poppler_path=r"C:\Users\kumaw\Desktop\Website\project\poppler\Library\bin")
    text_content = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        text = text.replace("-\n", "")
        text_content += text

    text_file_path = os.path.join('media', 'text', folder_name, f'{pdf_name}.txt')
    print(text_file_path)
    os.makedirs(os.path.dirname(text_file_path), exist_ok=True)
    with open(text_file_path, 'w') as text_file:
        text_file.write(text_content)
        
    return text_file_path
        

@login_required
def file_explorer(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('verification_required')  # Redirect to a verification required page

    if request.method == 'POST':
        form = FileUploadForm(user, request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            folder = None
            try:
                folder_id = form.cleaned_data['folder'].id
            except:
                pass
            new_folder_name = form.cleaned_data['new_folder_name']

            if new_folder_name:
                if Folder.objects.filter(name=new_folder_name, owner=user).exists():
                    messages.error(request, 'Folder already exists. Please choose a different name.')
                else:
                    folder = Folder.objects.create(name=new_folder_name, owner=user)
            elif folder_id:
                folder = Folder.objects.get(id=folder_id, owner=user)

            if folder:
                uploaded_files = request.FILES.getlist('file')  # Get the list of uploaded files
                for uploaded_file in uploaded_files:
                    file = File(name=uploaded_file.name, folder=folder, owner=user, file=uploaded_file)
                    file.save()
                    if uploaded_file.name.endswith('.pdf'):
                        text_path = process_pdf_to_text(uploaded_file, folder.name)
                        file.text_file_path = text_path
                        file.save()
            return redirect('file_explorer')
    else:
        form = FileUploadForm(user)

    user_folders = Folder.objects.filter(owner=user)
    return render(request, 'file_manager/file_explorer.html', {'folders': user_folders, 'form': form})

@login_required
def file_upload_ajax(request):
    user = request.user
    if request.method == 'POST':
        form = FileUploadForm(user, request.POST, request.FILES)
        if form.is_valid():
            folder = None
            folder_id = form.cleaned_data['folder'].id if form.cleaned_data['folder'] else None
            new_folder_name = form.cleaned_data['new_folder_name']

            if new_folder_name:
                if Folder.objects.filter(name=new_folder_name, owner=user).exists():
                    return JsonResponse({'success': False, 'message': 'Folder already exists.'})
                folder = Folder.objects.create(name=new_folder_name, owner=user)
            elif folder_id:
                folder = Folder.objects.get(id=folder_id, owner=user)

            if folder:
                uploaded_files = request.FILES.getlist('file')
                for uploaded_file in uploaded_files:
                    file = File(name=uploaded_file.name, folder=folder, owner=user, file=uploaded_file)
                    file.save()
                    if uploaded_file.name.endswith('.pdf'):
                        text_path = process_pdf_to_text(uploaded_file, folder.name)
                        file.text_file_path = text_path
                        file.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def delete_file(request, file_id):
    try:
        file_or_folder = File.objects.get(id=file_id)
    except:
        file_or_folder = Folder.objects.get(id=file_id)
        
    if file_or_folder.owner == request.user:  # Check if the user owns the file or folder before deleting
        
        if isinstance(file_or_folder, File) and file_or_folder.name.endswith('.pdf'):
            if file_or_folder.text_file_path:
                os.remove(file_or_folder.text_file_path)
            file_or_folder.file.delete()
            file_or_folder.delete()
            
        elif isinstance(file_or_folder, Folder):
            for file in file_or_folder.file_set.all():
                if file.text_file_path:
                    os.remove(file.text_file_path)
                file.file.delete()
                file.delete()
            
            file_or_folder.delete()
        else:
            # Delete the file
            file_or_folder.file.delete()
            file_or_folder.delete()
    return redirect('file_explorer')

@login_required
def verification_required(request):
    user = request.user
    if user.is_verified:
        return redirect('file_explorer')  # Redirect to the file explorer if user is already verified
    return render(request, 'file_manager/verification_required.html')
