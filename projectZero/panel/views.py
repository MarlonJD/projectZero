from django.shortcuts import render


def indexView(request):
    return render(request, 'panel/index.html')
