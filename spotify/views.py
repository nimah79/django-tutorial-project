from django.shortcuts import HttpResponse
from django.db.models import Count, Avg, Sum, Min, Max, F, Q


from spotify.models import Person


def hello(request):
    # Person.objects.filter(id__gt=1)
	people_statistics = Person.objects.aggregate(
        count=Count('age'),
        average=Avg('age'),
        sum=Sum('age'),
        min=Min('age'),
        max=Max('age'),
    )
	response = '<html><body>'
	response += str(people_statistics) + '<br>'
	response += '</body></html>'

	return HttpResponse(response)


def index(request, name, number):
	return HttpResponse(f'<html><body>Name = {name}<br>Number = {number}</body></html>')
