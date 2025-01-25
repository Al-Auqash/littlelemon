from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),


    path('throttle', views.ThrottleCheckView.as_view()),


    path('category', views.CategoryView.as_view()),
    path('category/<int:id>', views.CategoryDetailView.as_view()),


    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:id>', views.MenuItemDetailView.as_view()),


    path('groups/manager/users', views.ManagerSetView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerDeleteView.as_view()),
    path('groups/delivery-crew/users', views.DeliverySetView.as_view()),


    # Test for admin access
    path('admin/users', views.ManagerAdminView.as_view()),

    path('admin/group', views.GroupView.as_view()),
]
