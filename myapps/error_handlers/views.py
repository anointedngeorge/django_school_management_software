from django.shortcuts import render

from django.http import HttpResponseNotFound
import logging

# Set up logging
logger = logging.getLogger(__name__)


def handler_404(request, exception):
    try:
        return render(request, 'errors/404.html', status=404)
    except Exception as e:
        logger.error(f"Error rendering 404 page: {e}")
        # Fallback: return a simple 404 response if the template rendering fails
        return HttpResponseNotFound('<h1>Page not found</h1>')