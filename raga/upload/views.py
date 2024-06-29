from django.shortcuts import render, redirect
from .forms import FileUploadForm
from raga_app.models import Audio

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        print("in upload ",request.FILES['audio'].name)
        if form.is_valid():
            uploaded_file_name = request.FILES['audio'].name
            uploaded_swara_name= request.FILES['audio1'].name
            upload_file_option=form.cleaned_data['selected_option']
            uploaded_file = Audio(audio=request.FILES['audio'], 
                                  title=uploaded_file_name,audio1=request.FILES['audio1'],
                                  title1=uploaded_swara_name,selected_option=upload_file_option)
            uploaded_file.save()
            return redirect('/uploaded')  # Redirect to a success page
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def homepage(request):
    if request.method == 'POST':
        return redirect('/upload')
    return render(request, 'home.html')
