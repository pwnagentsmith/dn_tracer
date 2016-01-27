from django.conf.urls import patterns, url

urlpatterns = patterns("",
                       url(r"^$", "dashboard.views.index"),
                       url(r"^index.html$", "dashboard.views.index"),
                       )
