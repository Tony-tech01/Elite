from django.db import migrations

def create_leagues(apps, schema_editor):
    League = apps.get_model('Elite', 'League')
    leagues = [
        'Super Rugby',
        'Top 14',
        'Premiership Rugby',
        'United Rugby Championship',
        'Major League Rugby',
    ]
    for name in leagues:
        League.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('Elite', '0006_alter_team_league'),
    ]

    operations = [
        migrations.RunPython(create_leagues),
    ]