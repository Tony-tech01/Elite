from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import datetime

class Team(models.Model):
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Team Name")
    location = models.CharField(max_length=100, verbose_name="Team Location")
    founded_year = models.PositiveIntegerField(validators=[MinValueValidator(1800), MaxValueValidator(datetime.date.today().year)])
    coach = models.CharField(max_length=100)
    league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True, blank=True,)
    logo = models.ImageField(upload_to='team_logo', null=True, blank=True, default ='team_logo/main_logo.svg')

    def __str__(self):
        return f"{self.name} ({self.location})"

class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    POSITION_CHOICES = [
        ('Prop', 'Prop'),
        ('Hooker', 'Hooker'),
        ('Lock', 'Lock'),
        ('Flanker', 'Flanker'),
        ('Number Eight', 'Number Eight'),
        ('Scrum Half', 'Scrum Half'),
        ('Fly Half', 'Fly Half'),
        ('Centre', 'Centre'),
        ('Wing', 'Wing'),
        ('Full Back', 'Full Back'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    nationality = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    current_worth = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Height in cm
    date_of_birth = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='players')
    # spouse = models.CharField(max_length=100, blank=True, null=True)
    # children = models.PositiveIntegerField(default=0)
    # dummy_field = models.CharField(max_length=10, default='dummy')

    def __str__(self):
        return self.name


class PerformanceStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='performance_stats')
    matches_played = models.PositiveIntegerField(default=0)
    tries_scored = models.PositiveIntegerField(default=0)
    successful_tackles = models.PositiveIntegerField(default=0)
    overall_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Stats for {self.player.name}"

class Scout(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    organization = models.CharField(max_length=100,)
    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                    validators=[RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Enter a valid phone number")])
    role = models.CharField(max_length=100, choices=[("head scout", "Head Scout"), ("assistant", "Assistant")])
    created_at = models.DateTimeField(auto_now_add=True)
    teams = models.ManyToManyField(Team, related_name='scouts')

    def __str__(self):
        return self.user.username

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    category = models.CharField(max_length=50, default='rugby')

    def __str__(self):
        return self.title

class PastMatch(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='past_matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='past_matches_as_team2')
    match_date = models.DateField()
    match_time = models.TimeField()
    venue = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} on {self.match_date} at {self.match_time}"

class UpcomingMatch(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    match_date = models.DateField()
    match_time = models.TimeField()
    venue = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} on {self.match_date} at {self.match_time}"