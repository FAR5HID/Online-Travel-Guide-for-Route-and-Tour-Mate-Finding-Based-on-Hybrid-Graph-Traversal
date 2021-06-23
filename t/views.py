from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Spots
from .models import Edges
import datetime
import calendar
#from datetime import date
import requests
#from .forms import SearchForm

# Create your views here.

def home(request):
    print(request.POST)
    spots = Spots.objects.all()

    edges = Edges.objects.all()

    source = destination = dest = day = budget = category = date = None
    time = daytime = flag = 0

    route = []
    t = []
    ts = []
    tt = []
    holidays = {}
    #path = {}

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        dest = destination
        if request.POST.get('date'):
            date = str(request.POST.get('date'))
        print(date)
        if request.POST.get('day'):
            day = int(request.POST.get('day'))
        if request.POST.get('budget'):
            budget = int(request.POST.get('budget'))
        category = request.POST.get('category')
        print("s=", source, ", d=", destination, ", dy=", day, ", b=", budget, ", c=", category)
        
        if date:
            actual_day = day
            print("actldy ", actual_day)
            if not day:
                actual_day = 1
            for days in range(actual_day):
                strp_date = datetime.datetime.strptime(date, "%m/%d/%Y").date() + datetime.timedelta(days=days)
                #print("strpdt = ", strp_date)
                weekday = calendar.day_name[strp_date.weekday()]
                #print(weekday)

                url = 'https://holidays.abstractapi.com/v1/'
                payload = {'api_key': 'a47e699029cc4ac88d3b0632338c02d3', 'country': 'BD', 'year': strp_date.year, 'month': strp_date.month, 'day': strp_date.day}
                response = requests.get(url, params=payload)
                holiday = response.json()
                print(holiday)
                if holiday:
                    holidays[strp_date] = holiday[0]['name']
                    #print("\ntyp = ", holiday[0]['name'])
                elif weekday == 'Friday' or weekday == 'Saturday':
                    holidays[strp_date] = weekday
                    #print(weekday)

        if source:
            route.append(source)
        if destination:
            route.append(destination)
            if request.POST.get('budget'):
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

            if category:
                ts = Spots.objects.filter(name__in=t, category__contains=[category]).values_list('name', flat=True).order_by('rating')
            else:
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
                if request.POST.get('budget') and not request.POST.get('day'):
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
                    
                if request.POST.get('day') and not request.POST.get('budget'):
                    daytime = daytime + Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                    print("daytime= ", daytime)
                    if daytime > 9*60:
                        daytime = Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                        print("new daytime= ", daytime)
                        day = day - 1
                        print("rem day = ", day)
                
                if request.POST.get('budget') and request.POST.get('day'):
                    time = time + Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                    print(time)
                    daytime = daytime + Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                    print("daytime= ", daytime)
                    budget = budget - Edges.objects.filter(n1=source, n2=destination).values_list('cost', flat=True)[0]
                    print("budget = ", budget)
                    if daytime > 9*60:
                        daytime = Edges.objects.filter(n1=source, n2=destination).values_list('minute', flat=True)[0]
                        print("new daytime= ", daytime)
                        day = day - 1
                        print("rem day = ", day)
                        time = time + 15*60
                        budget = budget - 800
                        print("new day budget = ", budget)                

                if day and day+1 < 2:
                    flag = 1
                    break
                if budget and budget < 0:
                    flag = 1
                    break
                if (budget and day) and (day+1 < 2 or budget < 0):
                    flag = 1
                    break

                route.append(destination)
            
            if flag == 1:
                break

        print("route=",route)

        #return HttpResponseRedirect('#')


    return render(request, 'index.html', {'spots':spots, 'route':route, 'dest':dest, 'holidays':holidays})
    