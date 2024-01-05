from django.urls import path

from . import views

urlpatterns = [
    path("", views.products, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_product/", views.add_product, name='add_product'),
    path("details/<int:product_id>/", views.prod_details, name='details'),
    path("add_category/", views.add_category, name='add_category'),
    path('active/', views.active, name='active'),
    path('close/', views.close, name='close' ),
    path('watchlist/add/<int:product_id>/', views.watchlist_toggle, name='watchlist_toggle'),
    path('watchlist/remove/<int:product_id>/', views.remove_watchlist, name='watchlist_remove'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('comments/<int:product_id>/', views.comments, name='comments'),
    path('delete/comment/', views.delete_comments, name='delete_comment'),
    path('close_bid/', views.close_bid, name='close_bid'),
    path('winner/', views.winner, name='winner')
]

