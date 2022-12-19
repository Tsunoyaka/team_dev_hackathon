import os
from django.core.exceptions import ValidationError
from mutagen.mp3 import MP3
from mutagen.mp3 import MP3
from datetime import datetime
from django import template
# import math

# register=template.Library()

# @register.filter
# def time_formater(time):
#     time=int(time)
#     min=math.floor((time%3600)/60)
#     sec=math.floor(time%60)
    
#     if (sec<10):
#       sec=f"0{sec}"
      
#     return f"{min}:{sec}"
    

def get_time():
    format = '%Y%m%d%M%s'
    return datetime.now().strftime(format)

def get_audio_length(file):
    audio = MP3(file)
    return audio.info.length
   

def validate_is_audio(file):
    try:
        audio = MP3(file)

        if not audio :
            raise TypeError()

        first_file_check=True
    
    except Exception as e:
        first_file_check=False
    
    if not first_file_check:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp3']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')
