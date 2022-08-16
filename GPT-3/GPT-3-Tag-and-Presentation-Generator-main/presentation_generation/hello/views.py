import os

from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import json_slide_parser
from .flaticon import FlatIconParser
from .models import Greeting
from .slideshow import Slideshow

# Create your views here.
from .transcriptform import TranscriptForm


def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def slideshow(request):
    if request.method == "POST":
        form = TranscriptForm(request.POST)
        if form.is_valid():
            transcript = form.cleaned_data["transcript_field"]
            data = json_slide_parser.json_from_transcript(transcript)
            slides = Slideshow.from_json(request.user, data)
            return redirect(slides.get_url())
        else:
            return render(request, "slideshow.html", {"form": form})
    else:
        form = TranscriptForm()
        return render(request, "slideshow.html", {"form": form})


def create_slideshow(request):
    transcript = request.session["transcript"]
    data = json_slide_parser.json_from_transcript(transcript)
    slides = Slideshow.from_json(request.user, data)
    return redirect(slides.get_url())


def slideshow_api(request):
    request.session["transcript"] = request.POST.get("t", "")
    return redirect("/accounts/login/")


def slideshow_api_sender(request):
    transcript = "Hi, my name is Adam and I’m from clear shore. Did you realize that aerospace engineers are retiring " \
                 "at twice the rate that new engineers are entering the field. According to analysts, the lack of " \
                 "clear baton is causing the United States to slip in its competitiveness and is threatening our " \
                 "technological edge. A key federal priority. Clear shore is a near shore r&d outsource based in " \
                 "Puerto Rico that delivers a 40% cost advantage while bringing to the aerospace industry the talents " \
                 "of the 15th and 17th largest engineering schools in the country. Unlike Indians, Puerto Ricans are " \
                 "US citizens on US soil and our clearable. Our team includes Marcos Polanco, who is a policymaker " \
                 "and negotiated the creation of 1700 aerospace jobs in Puerto Rico. And Chris Dodd was one 3 billion " \
                 "in federal contracts as a contract capture consultant. And finally, Tito Mattila has raised over " \
                 "100 million in capital with a five time return to investors. Clear shore generates revenue from " \
                 "fees and additionally from the sale of r&d tax credits, unique to Puerto Rico. In essence, " \
                 "we are positioning good Rico as the India for this 60 billion in federal r&d market, and aim to " \
                 "establish Puerto Rico as a recognized Innovation Hub. We are currently negotiating r&d outsourcing " \
                 "agreements with local universities and you Mr. Investor must be involved because of your expertise " \
                 "in the financing of federal contracts. "
    return render(request, "slideshow_api_sender.html", {"transcript": transcript})


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
