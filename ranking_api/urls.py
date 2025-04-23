"""
URL configuration for ranking_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ranking_api.controllers.item_controller import ItemController
from ranking_api.controllers.ranking_controller import RankingController

urlpatterns = [
    path('admin/', admin.site.urls),

    # ITEM ENDPOINTS
    path('api/rankings/<int:ranking_id>/items/', ItemController.as_view(
        {
            'get': 'get_ranking_items',
            'post': 'create_ranking_item'
        }
    ), name='ranking-items'),
    path('api/items/<int:item_id>/', ItemController.as_view(
        {
            'get': 'get_ranking_item',
            'delete': 'delete_ranking_item',
            'patch': 'patch_ranking_item',
        }
    ), name='ranking-item'),

    # RANKING ENDPOINTS
    path('api/rankings/',RankingController.as_view(
        {
             'get': 'get_all_rankings',
             'post': 'create_ranking'
        }
    ), name='rankings-list'),

    path('api/rankings/<int:ranking_id>/', RankingController.as_view(
        {
             'get': 'get_ranking',
             'delete': 'delete_ranking',
             'put': 'update_ranking',
        }
    ), name='ranking-detail')
]
