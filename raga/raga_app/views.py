from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Audio
from .processing.process import ProcessAudio

# Create your views here.
class IndexView(View):
    def get(self, request):
        audio = Audio.objects.order_by("-uploaded_date")[0]
        audio1 = Audio.objects.order_by("-uploaded_date1")[0]
        
        audiofile = "C:/Users/anees/Documents/BlueLight/proj/final 2/raga_identifier-main - Copy/raga/Audio/" + str(audio.audio.name)
        audiofile1 = "C:/Users/anees/Documents/BlueLight/proj/final 2/raga_identifier-main - Copy/raga/Audio/" + str(audio1.audio1.name)
        print(audio.audio.name)
        print(audio.selected_option)
        if (audio.selected_option=="song"):
            Output=ProcessAudio(audiofile,audiofile1,1).get_dict()
        elif(audio.selected_option=="swara"):
             Output=ProcessAudio(audiofile,audiofile1,0).get_dict1()
        print(Output)
        return render(request,"raga_app/index.html",
            {
                "audio":audio,
                "audio1":audio1,
                "Output":Output
            }
        )