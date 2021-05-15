from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Spots
from .models import Edges
from .forms import SearchForm

# Create your views here.

def home(request):

    spots = Spots.objects.all()

    edges = Edges.objects.all()

    # source = None
    # destination = None

    q = []
    t = []
    ts = []

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sfdata = form.cleaned_data
            source = sfdata['source']
            destination = sfdata['destination']

    
            if source is not None:
                q.append(source)
            if destination is not None:
                q.append(destination)

            for edge in edges:
                for edge in edges:
                    if edge.n1 == destination and edge.n2 not in q:
                        t.append(edge.n2)

                ts = Spots.objects.filter(name__in=t).values_list('name', flat=True).order_by('rating')
                t = list(ts)
                if t:
                    destination = t.pop()
                if destination not in q:
                    q.append(destination)

            return HttpResponseRedirect('#')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()


    # sform = SearchForm()
    # if sform.is_valid():
    #     sfdata = sform.cleaned_data
    #     source = sfdata['source']
    #     destination = sfdata['destination']
        
    # q = []
    # t = []
    
    # if source is not None:
    #     q.append(source)
    # if destination is not None:
    #     q.append(destination)

    # for edge in edges:
    #     for edge in edges:
    #         if edge.n1 == destination and edge.n2 not in q:
    #             t.append(edge.n2)

    #     ts = Spots.objects.filter(name__in=t).values_list('name', flat=True).order_by('rating')
    #     t = list(ts)
    #     if t:
    #         destination = t.pop()
    #     if destination not in q:
    #         q.append(destination)



    return render(request, 'index.html', {'spots':spots, 'q':q, 't':t, 'ts':ts, 'form':form})
    