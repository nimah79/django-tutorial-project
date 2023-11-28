from django.shortcuts import HttpResponse, render
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Count
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ViewSet, ModelViewSet


from spotify.models import *
from spotify.forms import ContactForm, CreatePostForm, SignUpForm
from spotify.permissions import BlacklistPermission
from spotify.serializers import *


@login_required(login_url="/login")
@permission_required("spotify.view_post", raise_exception=True)
def hello(request):
    if not request.user.is_authenticated:
        return HttpResponse("401")

    users = User.objects.annotate(post_count=Count("post"))
    response = "<html><body>"
    for user in users:
        response += f"{user.username}: {user.post_count}<br>"
    response += "</body></html>"

    return HttpResponse(response)


def index(request, name, number):
    # ~ & |
    people = Person.objects.exclude(id__lt=10)

    response = "<html><body>"
    for person in people:
        response += f"{person.id}<br>"
    response += "</body></html>"

    return JsonResponse([1, 2, 3], safe=False)


def post_details(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return JsonResponse({"error": "not found"}, status=404)
    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
            "gender": post.author.gender,
            "email": post.author.email,
        },
    }

    return JsonResponse(post_dict)


def author_posts(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return JsonResponse({"error": "not found"}, status=404)
    posts = []
    # user.post_set.create(title='Test', content='Lorem ipsum 2')
    for post in user.post_set.all():
        posts.append(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
            }
        )

    return JsonResponse({"posts": posts})


def posts(request):
    posts = []
    min_id = request.GET.get("min_id")
    max_id = request.GET.get("max_id")
    for post in Post.objects.filter(id__gte=min_id, id__lte=max_id):
        posts.append(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "is_new": post.id > 10,
            }
        )

    return render(request, "posts.html", context={"posts": posts})


class CreatePostView(View):
    def get(self, request):
        return render(request, "create_post.html", {"form": CreatePostForm()})

    def post(self, request):
        form = CreatePostForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "bad request"}, status=400)

            form.save()

        return JsonResponse({"ok": True})


class UserListView(ListView):
    model = User
    # template_name = 'users/list.html'
    context_object_name = "users"
    # queryset = User.objects.filter(gender='m')
    paginate_by = 1


class UserDetailView(DetailView):
    model = User


class UserCreateView(CreateView):
    model = User
    fields = [
        "username",
        "gender",
        "email",
    ]


class UserUpdateView(UpdateView):
    model = User
    fields = [
        "username",
        "gender",
        "email",
    ]
    template_name_suffix = "_update_form"


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("user-list")


class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return HttpResponse("Form submitted successfully!")
        # return super().form_valid(form)


class PostMethodOnlyMixin:
    def get(self, request):
        return HttpResponse("Send a POST request")


class SignUpView(View):
    def get(self, request):
        return render(request, "spotify/signup.html", context={"form": SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        # serializer = PostSerializer(request.data)

        if not form.is_valid():
            return render(request, "spotify/signup.html", context={"form": form})

        form.save()
        return HttpResponse("User signed up successfully!")


class LoginView(View):
    def get(self, request):
        return render(
            request, "spotify/login.html", context={"form": AuthenticationForm()}
        )

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse("Invalid credentials")
        dj_login(request, user)
        return HttpResponse("Logged in successfully!")


@csrf_exempt
def change_password(request):
    if request.method == "GET":
        return HttpResponse("Send a POST request")

    if not request.user.is_authenticated:
        return HttpResponse("401")

    old_password = request.POST.get("old_password")
    new_password1 = request.POST.get("new_password1")
    new_password2 = request.POST.get("new_password2")

    if new_password1 != new_password2:
        return HttpResponse("New passwords are not identical")

    if not request.user.check_password(old_password):
        return HttpResponse("Wrong old password")

    request.user.set_password(new_password1)
    request.user.save()

    return HttpResponse("Password changed successfully!")


@csrf_exempt
def logout(request):
    if request.method == "GET":
        return HttpResponse("Send a POST request")

    if not request.user.is_authenticated:
        return HttpResponse("401")

    dj_logout(request)

    return HttpResponse("Logged out successfully!")


class AboutUsView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_people"] = [
            "Ali",
            "Hassan",
            "Hesam",
        ]
        return context


@api_view(["GET"])
def ping(request):
    return Response({"ok": True})


class PingAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"ok": True, "ip": request.META["REMOTE_ADDR"]})


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostAPIView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        post_serializer = PostSerializer(Post.objects.all(), many=True)

        return Response({"ok": True, "data": post_serializer.data})

    def post(self, request):
        post_serializer = PostSerializer(data=request.data)
        if not post_serializer.is_valid():
            return Response({"ok": False, "message": post_serializer.errors})

        post_serializer.save()
        return Response({"ok": True, "message": "Post created successfully!"})


class SinglePostAPIView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostSerializer(instance=post)

        return Response({"data": post_serializer.data})

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostSerializer(instance=post, data=request.data, partial=True)
        if not post_serializer.is_valid():
            return Response({"ok": False, "message": post_serializer.errors})

        post_serializer.save()
        return Response({"ok": True, "message": "Post updated successfully!"})


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()

        return Response({"ok": True})


def cache_example(request):
    value = cache.get("my_key")
    cache.set("my_key", "hello, world!", 10)
    return HttpResponse(value)


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class ArtistViewSet(ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class AlbumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class CoverViewSet(ModelViewSet):
    serializer_class = CoverSerializer
    queryset = Cover.objects.all()


class TrackViewSet(ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class PlaylistViewSet(ModelViewSet):
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()


class PlaylistTrackViewSet(ModelViewSet):
    serializer_class = PlaylistTrackSerializer
    queryset = PlaylistTrack.objects.all()


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class UserSubscriptionViewSet(ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()


class CouponViewSet(ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class VoucherViewSet(ModelViewSet):
    serializer_class = VoucherSerializer
    queryset = Voucher.objects.all()


class VoucherRedeemViewSet(ModelViewSet):
    serializer_class = VoucherRedeemSerializer
    queryset = VoucherRedeem.objects.all()


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
