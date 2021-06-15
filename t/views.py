from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Spots
from .models import Edges
from .forms import SearchForm

# Create your views here.

def home(request):
    print(request.POST)
    spots = Spots.objects.all()

    edges = Edges.objects.all()

    source = destination = day = budget = category = None
    time = daytime = flag = 0

    route = []
    t = []
    ts = []
    tt = []
    #path = {}

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        day = request.POST.get('day')
        if request.POST.get('budget') != '':
            budget = int(request.POST.get('budget'))
        category = request.POST.get('category')
        print("s=", source, ", d=", destination, ", dy=", day, ", b=", budget, ", c=", category)
    
        if source != None:
            route.append(source)
        if destination != None:
            route.append(destination)
            if request.POST.get('budget') != '':
                budget = budget - 500 - Edges.objects.filter(n1=source, n2=destination).values_list('cost', flat=True)[0]
                print(budget)

        #print("route=",route)

        for edge in edges:
            # eliminate this loop
            # for edge in edges:
            #     if edge.n1 == destination and edge.n2 not in route:
            #         t.append(edge.n2)
            #         path[edge.n2]=edge.n1
            #         print(path)
            
            t = list(Edges.objects.filter(n1=destination).exclude(n2__in=route).values_list('n2', flat=True))

            print("t=",t)

            ts = Spots.objects.filter(name__in=t).values_list('name', flat=True).order_by('rating')            

            print("ts=",ts)

            t = list(ts)

            tt.extend(t)
            print("tt=", tt)
            if t:
                destination = t.pop()
                tt.remove(destination)
                print("tt=", tt)
                print("new d=", destination)
                #source = path[destination]
                source = Edges.objects.filter(n2=destination).values_list('n1', flat=True)[0]
                print("new s=", source)
            elif not t and tt:
                destination = tt.pop()
                print("tt=", tt)
                print("new d=", destination)
                #source = path[destination]
                source = Edges.objects.filter(n2=destination).values_list('n1', flat=True)[0]
                print("new s=", source)

            if destination not in route:
                if request.POST.get('budget') != '':
                    time = time + Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                    print(time)
                    daytime = daytime + Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                    print("daytime= ", daytime)
                    budget = budget - Edges.objects.filter(n1=source, n2=destination).values_list('cost', flat=True)[0]
                    print("budget = ", budget)
                    if daytime > 9*60:
                        daytime = Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                        print("new daytime= ", daytime)
                        time = time + 15*60
                        budget = budget - 800
                        print("new day budget = ", budget)
                if budget < 0:
                    flag = 1
                    break
                route.append(destination)
            if flag == 1:
                break

        print("route=",route)

        #return HttpResponseRedirect('#')


    return render(request, 'index.html', {'spots':spots, 'route':route})
    