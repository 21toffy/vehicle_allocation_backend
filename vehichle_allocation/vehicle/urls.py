from django.urls import path
from vehicle import views

urlpatterns = [
    path("suitable/", views.ListSuitableBussesView.as_view(),name="suitable_buses_list"),
    path("allocate-suitable/", views.AllocateBusView.as_view(),name="allocate_suitable_buses"),


    
    path("create/bus/", views.BusView.as_view(),name="bus_create"),
    path("create/location/", views.LocationView.as_view(),name="location_create"),
    path('edit-bus/<int:bus_id>/', views.BusView.as_view(), name='edit_bus'),
    path('edit-location/<int:location_id>/', views.LocationView.as_view(), name='edit_location'),

    path("<str:condition>/",views.ListBus.as_view(),name="bus_list"),
    path("list-location/<str:distance>/",views.ListLocation.as_view(),name="location_list"),




    
    # path("update/<int:pk>/",views.UpdateTodoAPIView.as_view(),name="update_todo"),
    # path("delete/<int:pk>/",views.DeleteTodoAPIView.as_view(),name="delete_todo")
]