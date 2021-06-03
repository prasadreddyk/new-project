from django.urls import path

from . import views

urlpatterns = [
    path('movie', views.Movies_list.as_view()),
    path('update/<int:pk>/', views.Movies_detail.as_view()),
    path('search', views.Movies_search.as_view()),
    path('ordering', views.Movies_search_odering.as_view()),
    path('pdf', views.write_pdf_view)
]
