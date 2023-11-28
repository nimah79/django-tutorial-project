"""spotify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from spotify.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r"posts", PostViewSet)
router.register(r"countries", CountryViewSet)
router.register(r"cities", CityViewSet)
router.register(r"artists", ArtistViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"covers", CoverViewSet)
router.register(r"tracks", TrackViewSet)
router.register(r"playlists", PlaylistViewSet)
router.register(r"playlist_tracks", PlaylistTrackViewSet)
router.register(r"subscriptions", SubscriptionViewSet)
router.register(r"user_subscriptions", UserSubscriptionViewSet)
router.register(r"coupons", CouponViewSet)
router.register(r"vouchers", VoucherViewSet)
router.register(r"voucher_redeems", VoucherRedeemViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", hello),
    path("ping", PingAPIView.as_view()),
    path("posts/<int:id>/", post_details),
    # path('posts', posts),
    path("signup", SignUpView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("change_password", change_password, name="change_password"),
    path("logout", logout, name="logout"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user-delete"),
    path("users/new", UserCreateView.as_view()),
    path("create_post", csrf_exempt(CreatePostView.as_view())),
    path("contact", ContactFormView.as_view()),
    path("about", AboutUsView.as_view()),
    path("authors/<int:id>/posts", author_posts),
    path("<str:name>/<int:number>/", index),
    path("api/posts", PostAPIView.as_view()),
    path("api/posts/<int:post_id>", SinglePostAPIView.as_view()),
    path("api/login", view=obtain_auth_token),
    path("api/logout", view=LogoutAPIView.as_view()),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("cache", cache_example),
    path("__debug__/", include("debug_toolbar.urls")),
]

# POST /api/posts
# GET /api/posts
# GET /api/posts/<int:id>
# PUT /api/posts/<int:id>
# DELETE /api/posts/<int:id>
# GET /api/posts/<int:id>/comments
# GET /api/post_comments/<int:id>
# GET /api/comments/<int:id>
