from django.shortcuts import render

# Import Class Based View
from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name = 'core/index.html'


