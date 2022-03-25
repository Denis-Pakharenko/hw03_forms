from django.views.generic.base import TemplateView
# Create your views here.


class AboutAuthorView(TemplateView):
    template_name = 'about/about.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
