from django.views.generic.base import TemplateView
from django.conf import settings



class IndexTemplateView(TemplateView):
    """For serving Vue.js frontend"""
    def get_template_names(self):
        if settings.DEBUG:
            template_name = "index-dev.html"
        else:
            template_name = "index.html"
        return template_name