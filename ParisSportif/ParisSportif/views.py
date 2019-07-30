from django.shortcuts import render
def home(request):
	return render(request, 'fr/public/home.html')
	
