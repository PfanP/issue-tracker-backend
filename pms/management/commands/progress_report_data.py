import random
from datetime import datetime
from django.core.management import BaseCommand

from pms.models import Project

__author__ = 'Ashraful'
FAKE_PROJECT_NAMES = (
    'Internship Project', 'School Management System', 'Static Generator Maker', 'Sales Tracker',
    'Survey Monitor', 'Railway Tacking System', 'Home Monitor System', 'Data Mining with ML & NLP'
)


class Command(BaseCommand):
    def update_data(self):
        for fake_project_name in FAKE_PROJECT_NAMES:
            project = Project.objects.filter(name__icontains=fake_project_name).first()
            print("Updating... {0}".format(fake_project_name))

            for issue in project.issue_set.all():
                issue.created_at = datetime.now().replace(month=random.randrange(8, 12), day=15)
                issue.progress = random.randrange(15, 85)
                issue.save()

    def handle(self, *args, **options):
        self.update_data()
