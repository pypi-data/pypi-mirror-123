import django

__version__ = '2021.10.18'

if django.VERSION < (3, 2):
    default_app_config = 'drf_spectacular.apps.SpectacularSidecarConfig'
