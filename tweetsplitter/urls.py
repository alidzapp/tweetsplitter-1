from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.home', name='index'),
                       url(r'^login$', 'main.views.login', name='login-twitter'),
                       url(r'^logout$', 'main.views.logout', name='logout-twitter'),
                       url(r'^post$', 'main.views.post', name='post-twitter'),
                       url(r'^post_ajax$', 'main.views.post_ajax', name="post-ajax"),
                       url(r'^get_oauth', 'main.views.get_oauth', name='get-oauth'),
                       #url(r'^admin/', include(admin.site.urls)),
)
