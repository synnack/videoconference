from django.shortcuts import render


def index(request):
    context = { 'title': "Home" }
    return render(request, 'index.html', context)

def rooms(request):
    context = { 'title': "My rooms" }
    return render(request, 'scheduler/rooms.html', context)

def request(request):
    context = { 'title': "Request conference" }
    return render(request, 'index.html', context)

def room(request):
    context = { }
    return render(request, 'index.html', context)
