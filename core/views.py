from django.shortcuts import render

# Import Class Based View
from django.views.generic import TemplateView

#Third Party
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus





class HomeView(TemplateView):
	template_name = 'core/index.html'

def search(request):
	return render(request, 'core/search.html')