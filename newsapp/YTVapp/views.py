from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from pytube import YouTube

def index(request):

    try:


        if request.method == 'POST':
            try:
                link = request.POST['link']
                video = YouTube(link)


                stream = video.streams.get_lowest_resolution()

                stream.download()


                return render(request, 'index.html', {'msg':'Video downloaded'})
            except:
                return render(request, 'index.html', {'msg':'Video not downloaded'})
        return render(request, 'index.html', {'msg':''})
    except:
        return render(request, "index.html", {"msg":"Sorry something went wrong!"})