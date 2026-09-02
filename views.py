from django.http import request, HttpResponse
from django.shortcuts import render

def main(req: request):
    return render(req, 'main.html')