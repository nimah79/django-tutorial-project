from django.shortcuts import HttpResponse, render
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Count, Avg, Sum, Min, Max, F, Q
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as dj_login


from spotify.models import Person, Post, User
from spotify.forms import ContactForm, CreatePostForm, SignUpForm


def hello(request):
    users = User.objects.annotate(post_count=Count('post'))
    response = '<html><body>'
    for user in users:
        response += f'{user.username}: {user.post_count}<br>'
    response += '</body></html>'

    return HttpResponse(response)


def index(request, name, number):
    # ~ & |
    people = Person.objects.exclude(id__lt=10)

    response = '<html><body>'
    for person in people:
        response += f'{person.id}<br>'
    response += '</body></html>'

    return JsonResponse([1, 2, 3], safe=False)


def post_details(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return JsonResponse({'error': 'not found'}, status=404)
    post_dict = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'gender': post.author.gender,
            'email': post.author.email,
        }
    }

    return JsonResponse(post_dict)


def author_posts(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return JsonResponse({'error': 'not found'}, status=404)
    posts = []
    # user.post_set.create(title='Test', content='Lorem ipsum 2')
    for post in user.post_set.all():
        posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
        })

    return JsonResponse({'posts': posts})


def posts(request):
    posts = []
    min_id = request.GET.get('min_id')
    max_id = request.GET.get('max_id')
    for post in Post.objects.filter(id__gte=min_id, id__lte=max_id):
        posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'is_new': post.id > 10,
        })

    return render(request, 'posts.html', context={'posts': posts})


class CreatePostView(View):
    def get(self, request):
        return render(
            request,
            'create_post.html',
            {'form': CreatePostForm()}
        )


    def post(self, request):
        form = CreatePostForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'error': 'bad request'}, status=400)

            form.save()

        return JsonResponse({'ok': True})


class UserListView(ListView):
    model = User
    # template_name = 'users/list.html'
    context_object_name = 'users'
    # queryset = User.objects.filter(gender='m')
    paginate_by = 1


class UserDetailView(DetailView):
    model = User


class UserCreateView(CreateView):
    model = User
    fields = [
        'username',
        'gender',
        'email',
    ]


class UserUpdateView(UpdateView):
    model = User
    fields = [
        'username',
        'gender',
        'email',
    ]
    template_name_suffix = '_update_form'


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user-list')


class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return HttpResponse('Form submitted successfully!')
        # return super().form_valid(form)


@csrf_exempt
def signup(request):
    if request.method == 'GET':
        return HttpResponse('Send a POST request')

    form = SignUpForm(request.POST)

    if not form.is_valid():
        return HttpResponse(f'{form.errors}')

    form.save()
    return HttpResponse('User signed up successfully!')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse('Send a POST request')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if not user:
        return HttpResponse('Invalid credentials')
    dj_login(request, user)
    return HttpResponse('Logged in successfully!')
