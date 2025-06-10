from django.shortcuts import render, redirect
from .models import Player, PerformanceStat, Team, News, UpcomingMatch, Scout
from .forms import RegistrationForm, TeamForm, DonationForm, PlayerAddForm, PlayerUpdateForm, PerformanceStatAddForm, PerformanceStatUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from mpesa_api.core.mpesa import Mpesa
mpesa = Mpesa()
from rest_framework import viewsets
from .serializers import PlayerSerializer, TeamSerializer, PerformanceStatSerializer



# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    

class PerformanceStatViewSet(viewsets.ModelViewSet):
    queryset = PerformanceStat.objects.all()
    serializer_class = PerformanceStatSerializer
    

def mpesa_callback(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return HttpResponse(status=405)

def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "See u soon")
    return render(request, "base/logout.html")

def login_user(request):
    next_url = request.GET.get('next') or request.POST.get('next') or '/dashboard/'
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me", False)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect(next_url)
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, 'base/login.html', {'next': next_url})
    

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_user")
    else:
        form = RegistrationForm()

    return render(request, "base/register.html", {"form": form})


from django.utils import timezone

def home(request):
    now = timezone.localtime(timezone.now())    
    rugby_news = News.objects.filter(category__iexact='rugby').order_by('-date')[:5]
    
    
    upcoming_matches = UpcomingMatch.objects.filter(
        match_date__gte=now.date()
    ).exclude(
        match_date=now.date(), match_time__lte=now.time()
    ).order_by('match_date', 'match_time')

    past_matches = UpcomingMatch.objects.filter(
        match_date__lt=now.date()
    ).union(
        UpcomingMatch.objects.filter(match_date=now.date(), match_time__lte=now.time())
    ).order_by('-match_date', '-match_time')

    
    context = {
        'rugby_news': rugby_news,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches
    }
    return render(request, 'base/home.html', context)

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        context = {
            'name': name,
            'email': email,
            'message': message
        }

        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')
    return render(request, 'base/contact.html')

@login_required(login_url='login_user')
def dashboard(request):
    context = {
        'players': Player.objects.all(),
        'scouts': Scout.objects.all(),
        'teams': Team.objects.all(),
        'upcoming_matches': UpcomingMatch.objects.filter(match_date__gte=timezone.now().date()),
    }
    return render(request, 'base/dashboard.html', context)


def player_list(request):
    query = request.GET.get('name', '')
    if query:
        players = Player.objects.filter(name__icontains=query)
    else:
        players = Player.objects.all()
    
    context={'players': players}
    return render(request, 'base/player_list.html', context)

@login_required(login_url='login_user')
def player_detail(request, pk):
    player = Player.objects.get(id=pk)
    context = {'player': player}
    return render(request, 'base/player_detail.html', context)

@login_required(login_url='login_user')
def add_player(request):
    player_form = PlayerAddForm(request.POST or None)
    stat_form = PerformanceStatAddForm(request.POST or None)
    if request.method == 'POST':
        if player_form.is_valid() and stat_form.is_valid():
            player = player_form.save()
            stat = stat_form.save(commit=False)
            stat.player = player
            stat.save()
            return redirect('player_list')
    context = {'form': player_form, 'stat_form': stat_form}
    return render(request, 'base/add_player.html', context)

@login_required(login_url='login_user')
def update_stat(request, pk):
    stat = PerformanceStat.objects.get(id=pk)
    form = PerformanceStatUpdateForm(request.POST, instance=stat)
    if request.method == 'POST':
            form = PerformanceStatUpdateForm(request.POST, instance=stat)
            if form.is_valid():
             form.save()
            return redirect('player_detail', pk=pk)
    context = {'form': form, 'stat': stat}
    return render(request, 'base/update_stat.html', context)

@login_required(login_url='login_user')
def delete_player(request, pk):
    player = Player.objects.get(id=pk)
    context = {"player": player}
    if request.method == "POST":
        player.delete()
        return redirect('player_list')
    return render(request, 'base/delete_player.html', context)

def team_list(request):
    query = request.GET.get('name', '')
    if query:
        teams = Team.objects.filter(name__icontains=query)
    else:
        teams =  Team.objects.all()
    
    context ={'teams': teams}
    return render(request, "base/team_list.html", context)

@login_required(login_url='login_user')
def profile(request):
    try:
        scout = request.user.scout
    except AttributeError:
        
        messages.error(request, "You do not have a profile. Please contact the admin.")
        return redirect('dashboard')
    return render(request, "base/profile.html", {"scout": scout})

@login_required(login_url='login_user')
def team_detail(request, pk):
    team = Team.objects.get(id=pk)
    players = team.players.all()  
    context = {'team': team, 'players': players}
    return render(request, 'base/team_detail.html', context)

@login_required(login_url='login_user')
def add_team(request):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_list',)
    context = {'form': form}    
    return render(request, 'base/add_team.html', context)


@login_required(login_url='login_user')
def delete_team(request, pk):
    team = Team.objects.get(id=pk)
    context = {"team": team}
    if request.method == "POST":
        team.delete()
        return redirect('team_list')
    return render(request, 'base/delete_team.html', context)


@login_required(login_url='login_user')
def news_detail(request, pk):
    news = News.objects.get(id=pk)
    context = {'news': news}
    return render(request, 'base/news_detail.html', context)

def donate(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            amount = form.cleaned_data['amount']

            mpesa = Mpesa()
            try:
                response = mpesa.stk_push(
                    phone,  # phone number
                    amount,  # amount
                    "Stadium Contribution"  # account_reference
                    # is_paybill=True  # optional, defaults to True
                )
                messages.success(request, f"Payment request sent to {phone}. Complete payment on your phone.")
            except Exception as e:
                messages.error(request, f"Payment failed: {str(e)}")
            return redirect('dashboard')
    else:
        form = DonationForm()
    return render(request, 'base/donate.html', {'form': form})

@login_required(login_url='login_user')
def update_player(request, pk):
    player = Player.objects.get(id=pk)
    stat, created = PerformanceStat.objects.get_or_create(player=player)
    player_form = PlayerUpdateForm(request.POST or None, instance=player)
    stat_form = PerformanceStatUpdateForm(request.POST or None, instance=stat)
    if request.method == 'POST':
        if player_form.is_valid() and stat_form.is_valid():
            player_form.save()
            stat_form.save()
            return redirect('player_detail', pk=pk)
    context = {
        'form': player_form,
        'stat_form': stat_form,
        'player': player
    }
    return render(request, 'base/update_player.html', context)


