from django.shortcuts import render

# Import Class Based View
from django.views.generic import TemplateView, ListView

#Models
from .models import Search

#Third Party
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

## URL PAth
BASE_URL = 'https://www.pdfdrive.com/search?q={}&pagecount=&pubyear=&searchin=&em='



class HomeView(TemplateView):
	template_name = 'core/index.html'

class SearchView(ListView):
	model = Search
	context_object_name = 'searches'
	template_name = 'core/recent.html'

	def get_queryset(self):
		return Search.objects.order_by("-time")

def search(request):
	search = request.GET['search']
	Search.objects.create(search=search)
	
	url = BASE_URL.format(quote_plus(search))
	source = requests.get(url).text

	soup = BeautifulSoup(source, 'lxml')

	div = soup.find('div', class_="files-new")

	books = []
	for pdf in div.find_all('li'):
		image = pdf.find('img')['src']
		title = pdf.find('img')['title']
		link = pdf.find('a')['href']
		try:
			page = pdf.find('span', class_="fi-pagecount").text
		except:
			page = 'N/A'
		year = pdf.find('span', class_="fi-year").text
		downloads = pdf.find('span', class_="fi-hit").text

		books.append((title, image, link, page, year, downloads))

	frontend = {
		'search' : search,
		'books' : books,
	}
	return render(request, 'core/search.html', frontend)