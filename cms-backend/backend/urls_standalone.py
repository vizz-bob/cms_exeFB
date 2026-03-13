"""
urls_standalone.py
==================
URL configuration for the standalone (.exe) deployment.

Imports all API routes from the original urls.py and appends a catch-all
that serves the React SPA's index.html for every non-API path, enabling
client-side routing to work correctly when served from Django.
"""

import os
from django.urls import re_path
from django.http import HttpResponse, FileResponse
from django.conf import settings

# Import all existing URL patterns unchanged
from backend.urls import urlpatterns as _base_urlpatterns


# ---------------------------------------------------------------------------
# React SPA catch-all view
# ---------------------------------------------------------------------------

def serve_react_index(request, path=''):
    """
    Serve the React SPA for any URL that doesn't match an API route.
    Enables React Router client-side navigation (e.g. /about, /blog/:slug).
    """
    react_index = os.path.join(
        str(getattr(settings, 'BASE_DIR', '')),
        'frontend_build',
        'index.html'
    )

    if os.path.exists(react_index):
        return FileResponse(open(react_index, 'rb'), content_type='text/html')

    # Fallback message when frontend hasn't been built yet
    return HttpResponse(
        "<h1>Frontend not found</h1>"
        "<p>Please run <code>npm run build</code> in the cms-frontend directory "
        "and copy the output to <code>cms-backend/frontend_build/</code>.</p>",
        status=404,
        content_type='text/html',
    )


# ---------------------------------------------------------------------------
# URL patterns
# ---------------------------------------------------------------------------

# Start from the base patterns and add the React catch-all LAST
# (it must come after all API / admin patterns so it doesn't shadow them)
urlpatterns = list(_base_urlpatterns) + [
    # Matches anything that isn't already handled:
    #   - NOT /api/...
    #   - NOT /admin/...
    #   - NOT /static/...
    #   - NOT /media/...
    re_path(
        r'^(?!api/|admin/|static/|media/).*$',
        serve_react_index,
        name='react_index',
    ),
]
