from django.shortcuts import render

def forms(request):
    return render(request, 'forms.html')