from django.shortcuts import HttpResponse, render
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Count, Avg, Sum, Min, Max, F, Q
from django.views.decorators.csrf import csrf_exempt


from spotify.models import Person, Post, User
from spotify.forms import CreatePostForm


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


def create_post(request):
    if request.method == 'GET':
        return render(
            request,
            'create_post.html',
            {'form': CreatePostForm()}
        )
    form = CreatePostForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'bad request'}, status=400)

    form.save()

    return JsonResponse({'ok': True})
