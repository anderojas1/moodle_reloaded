from django.conf.urls import include, url, patterns
from .views import Index, SignupLeaderTeacher, Perfil

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'inicio/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}
        ),
    url(r'^signup/$', SignupLeaderTeacher.as_view(), name='signup'),
    url(r'^profile/$', Perfil.as_view(), name='signup'),
)