from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
from django.conf import settings

from surykatki.tools import object_detection, ErrorHelper

import datetime
import os

from stronka.models import Baza

imagesBeforeDir = os.path.join('media', 'before')
imagesAfterDir = os.path.join('media', 'after')

def index(request):
    datetime_now = datetime.datetime.now()
    context = {
        'datetime_now' : datetime_now,
    }
    return render(request, 'index.html', context)


def upload(request):
    if request.method == 'POST':
        err = ErrorHelper()

        image = request.FILES.get('uploaded_file')
        imageBeforePath = ''
        imageAfterPath = ''

        if not isinstance(image, UploadedFile):
            err.setError('Plik nie został odebrany poprawnie.')
        else:
            # Baza.resetNumerObrazka()
    
            image_nr = Baza.nextNumerObrazka()
    
            fname, fext = os.path.splitext(image.name)
    
            if fext.lower() not in ('.jpg', '.jpeg'):
                err.setError('Obrazek musi być w rozszerzeniu JPG.')
            else:
                filename = 'image{0:05d}{1}'.format(image_nr, fext)

                if not os.path.isdir(imagesBeforeDir):
                    os.makedirs(imagesBeforeDir)
                
                if not os.path.isdir(imagesAfterDir):
                    os.makedirs(imagesAfterDir)
                
                imageBeforePath = os.path.join(imagesBeforeDir, filename)
                imageAfterPath = os.path.join(imagesAfterDir, filename)

                object_detection(image, imageBeforePath, imageAfterPath)
                

        context = {
            'success': err.success,
            'error_msg': err.msg,
            'imageBefore': imageBeforePath,
            'imageAfter': imageAfterPath,
        }

        return render(request, 'upload.html', context)

    return redirect('/')

def list_wyniki(request):
    
    files = []
    
    for filename in os.listdir(imagesAfterDir):
        files.append(filename)
    
    context = {
        'files': files,
    }

    return render(request, 'list.html', context)
    

