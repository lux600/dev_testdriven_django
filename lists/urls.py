from django.conf.urls import url

from .views import home_page, view_list, new_list

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^the-only-list-in-the-world/$', view_list, name='view_list' ),
    url(r'^new$',new_list, name='new_list' )
]