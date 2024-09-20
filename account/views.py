from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.contrib import messages
from hotel.models import Guest
from datetime import datetime, date, timedelta
import random
from account.models import *
from rooms.models import *
from hotel.models import *
from .forms import *



def register_page(request):
    form = createUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =='POST':
            form = createUserForm(request.POST)
            if form.is_valid():
                if(len(User.objects.filter(email = request.POST.get("email"))) != 0):
                    messages.error(
                        request , 'Cet adress email est deja utilise' )
                    return redirect('login')
                
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name="guest")
                user.groups.add(group)

                curGuest = Guest(
                    user = user, phonneNumber = request.post.get("phoneNumber"))
                curGuest.save()

                messages.success(
                    request, 'Le compte invite a ete cree avec succes son nom est' + username)
                
                return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def add_employe(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"


    form = createUserForm()
    form2 = ROLES()
    form3 = createEmployeeForm()

    if request.method == 'POST':
        post = request.POST.copy() 
        post['phoneNumber'] = "+237" + post['phoneNumber']
        request.POST = post

        form = createUserForm(request.POST)
        form2 = ROLES(request.POST)
        form3 = createEmployeeForm(request.POST)

        
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save()
            employee = form3.save()
            employee.user = user
            employee.save()


            username = form.cleaned_data.get('username')

            role = form2.cleaned_data.get('username')

            group = Group.objects.get(name=role)
            user.groups.add(group)

            messages.success(
                request, role + 'compte cree avec succes pour ' + username)
            
            return redirect('employees')
        

    context = {
        'form':form,
        'form2':form2,
        'form3':form3,
        "role":role
    }  

    return render(request, path + "add-employee.html", context)  


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method =="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request , username=username , password=password)

            if user is not None:
                login(request , user)
                return redirect('home')
            else:
                messages.info(request, "le mot de passe ou userame est incorrect")

        
        context = {}
        return render(request , 'accounts/login.html', context)
    

def logout_user(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def guets(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"


#Booking.objects.all() , .values("guest") : On extrait uniquement les valeurs de la colonne "guest" (invité)
#annotate pour compter combien de réservations chaque invité a faite .order_by("-total") : On ordonne les résultats par le nombre total de réservations, en ordre décroissant (du plus grand au plus petit).


#topRange contient une liste d'invités triés selon le nombre de réservations qu'ils ont effectuées.

    topRange = Booking.objects.all().values("guest").annotate(
        total = Count("guest")).order_by("-total")
    
    topLimit = 10
    topList = []

    for t in topRange:
        if len(topList) > 10:
            break
        else:
            topList.append(Guest.objects.get(id=t.get("guest")))


        
        # recupere les reservation des 30 derniers jours
    
    bookings = Booking.objects.all()
    fd = datetime.combine(date.today()-timedelta(days=30),datetime.min.time())
    ld = datetime.combine(date.today(), datetime.min.time)

    guests = []


#Ce code parcourt toutes les réservations et vérifie si elles se chevauchent avec une période donnée. 
#Si c'est le cas, il ajoute chaque invité unique à la liste guests. Cela permet d'obtenir une liste des invités ayant réservé durant cette période spécifique.

    for b in bookings:
        if b.endDate >= fd.date() and b.startDate <=ld.date():
            if b.guest not in guests:
                guests.append(b.guest)


    if request.method  == "POST":
        if "filterDate" in request.POST:
            
            if request.POST.get("f_day") == "" and request.POST.get("l_day") == "":
                guests = Guest.objects.all()

                context = {
                    "role":role,
                    "guests":guets,
                    "fd":"",
                    "ld":""

                }

                return render(request , path + "guests.html",context)
#Ce code vérifie si aucune date de début n'a été fournie. Si c'est le cas, il définit fd à une date par 
#défaut (le 1er janvier 1970), souvent utilisée comme valeur de référence ou pour indiquer une absence de date.
            if request.POST.get("f_day") == "":
                fd = datetime.strftime("1970-01-01", '%Y-%m-%d')
            else:
                fd = request.POST.get("f_day") 
                fd  = datetime.strftime(fd , '%Y-%m-%d')

            if request.POST.get("l_day") == "":
                ld = datetime.strftime("2030-01-01", '%Y-%m-%d')
            else:
                ld = request.POST.get("l_day")
                ld = datetime.strftime(ld , '%Y-%m-%d')

            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ld.date():
                    if b.guest not in guests:
                        guests.append(b.guest)

            if "filterGuest" in request.POST:
                guests = Guest.objects.all()
                users = User.objects.all()
                if (request.POST.get("id")):
                    users = users.filter(
                        id__contains=request.POST.get(("id"))
                    )
                    guests = guests.filter(user__id=users)

                if (request.POST.get("name") != ""):
                    users = users.filter(
                         Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                    guests = guests.filter(user__in=users)


                if(request.POST.get("email") != "" ):
                    guests = users.filter(email__contains=request.POST.get("email"))
                    guests = guets.filter(user__in=users)

                if(request.POST.get("number") != ""):
                    guests = guests.filter(
                        phoneNumber__contains=request.POST.get("number"))
                    

                context = {
                    "role": role,
                    "guests":guests,
                     "id": request.POST.get("id"),
                    "name": request.POST.get("name"),
                    "email": request.POST.get("email"),
                    "number": request.POST.get("number")
                    
                }
                return render(request, path + "guests.html", context)
    if "top" in request.POST:
        topRange = Booking.objects.all().values("guest").annotate(
            total = Count("guest")).order_by("-total")
        topList = []
        topLimit = request.POST.get("top")
        for t in topRange:
            if len(topList) >= topLimit:
                break
            else:
                topList.append(Guest.objects.get(id=t.get("guest")))
        context = {
            "role":role,
            "guests":guets,
            "topList":topList,
            "tolLimit":topLimit,
            "fd":fd,
            "ld":ld

        }
        return render(request , path + "guests.html", context)
    
    context = {
        "role": role,
        "guests": guests,
        "topList": topList,
        "topLimit": topLimit,
        "fd": fd,
        "ld": ld
    }
    return render(request, path + "guests.html", context)


@login_required(login_url='login')
def employees(request):

        role = str(request.user.groups.all()[0])
        path = role + "/"

        employees = Employee.objects.all()

        if request.method == "POST":
            if "filter" in request.POST:
                users = User.objects.all()
                if (request.POST.get("id")!= ""):
                    users = users.filter(
                        id__contains=request.POST.get("id"))
                    employees = employees.filter(user__in=users)

                if (request.)
                    




