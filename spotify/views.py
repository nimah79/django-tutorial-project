from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Count, Avg, Sum, Min, Max, F, Q


from spotify.models import Person, Post, User


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
	user.post_set.create(title='Test', content='Lorem ipsum 2')
	for post in user.post_set.all():
		posts.append({
			'id': post.id,
			'title': post.title,
			'content': post.content,
		})

	return JsonResponse({'posts': posts})
