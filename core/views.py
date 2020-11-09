from django.shortcuts import render

# Import Class Based View
from django.views.generic import TemplateView, ListView

# Models
from .models import Search

# Third Party
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

# URL Path to Link
BASE_URL = 'https://www.pdfdrive.com/search?q={}&pagecount=&pubyear=&searchin=&em='

# Home Page


class HomeView(TemplateView):
    template_name = 'core/index.html'

# Recent Searches


class SearchView(ListView):
    model = Search
    context_object_name = 'searches'
    template_name = 'core/recent.html'

    def get_queryset(self):
        return Search.objects.order_by("-time")

# Search Page


def search(request):
    # Collect Data From Form
    search = request.GET['search']

    # Create Database Item
    Search.objects.create(search=search)

    # If Form Data has space,replace space with '+'
    url = BASE_URL.format(quote_plus(search))

    # Turn url into HTML Text
    source = requests.get(url).text

    # Create Soup Object
    soup = BeautifulSoup(source, 'lxml')

    # Find Div TAg with Class
    div = soup.find('div', class_="files-new")

    # Create An Empty List
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
        'search': search,
        'books': books,
    }
    return render(request, 'core/search.html', frontend)
