from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from octofit_tracker import settings

from django.apps import apps

User = get_user_model()

# Define models for teams, activities, leaderboard, workouts if not already defined
# For demonstration, we will use Django's ORM and assume models exist

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team = apps.get_model('octofit_tracker', 'Team')
        Activity = apps.get_model('octofit_tracker', 'Activity')
        Leaderboard = apps.get_model('octofit_tracker', 'Leaderboard')
        Workout = apps.get_model('octofit_tracker', 'Workout')
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            User(email='tony@marvel.com', username='IronMan', team=marvel),
            User(email='steve@marvel.com', username='CaptainAmerica', team=marvel),
            User(email='bruce@marvel.com', username='Hulk', team=marvel),
            User(email='clark@dc.com', username='Superman', team=dc),
            User(email='bruce@dc.com', username='Batman', team=dc),
            User(email='diana@dc.com', username='WonderWoman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        # Create activities
        Activity.objects.create(user=users[0], type='Run', duration=30, calories=300)
        Activity.objects.create(user=users[1], type='Swim', duration=45, calories=400)
        Activity.objects.create(user=users[3], type='Bike', duration=60, calories=500)

        # Create workouts
        Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes', difficulty='Medium')
        Workout.objects.create(name='Strength Training', description='Strength for all heroes', difficulty='Hard')

        # Create leaderboard
        Leaderboard.objects.create(user=users[0], score=1000)
        Leaderboard.objects.create(user=users[3], score=950)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
