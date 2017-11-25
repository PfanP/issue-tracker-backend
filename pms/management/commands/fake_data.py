from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from core.models import Profile
from pms.models import *


USER_NAMES = ('robin', 'ashraful', 'john', 'jasica')
FAKE_PROJECT_NAMES = (
        'Internship Project', 'School Management System', 'Static Generator Maker', 'Sales Tracker', 
        'Survey Monitor', 'Railway Tacking System', 'Home Monitor System', 'Data Mining with ML & NLP'
    )

FAKE_DESCRIPTION = "<p><h4>This is dummy description. Applicatioble for all issues and projects.</h4>\
</p><p><strong>Overview&nbsp;</strong></p><p>This is dummy description for this issue. Actually, the software\
 is under construction. So, it's impossible to show from real life data. So that I'm creating issue.</p>\
 <p><br></p><p><strong>What is working?</strong></p><ul><li>Issue manipulation.</li><li>Project's overview.</li>\
 <li>Report generation form issues (Daily, Monthly, Total overview)</li><li>Role based access permission by <strong>Admin.</strong>\
 </li><li>Unit Testing facility from settings module.</li><li>User based dashboard.</li><li>Searching in every view.</li><li>\
 Shorting in table column.</li><li>Report Export facilities.</li></ul>"

FAKE_ISSUE_TITLES = (
    "Enabled searching in every view.", "Add google font so that, it can show in evert browser and every size of screen.",
    "Added user based dashboard.", "Add user's activity report.", "Add some chart reports like LineChart, PieChart etc..",
    "Please make sperated each functionality when test runner view ",  "Add User own profile view", "Fixed Reponsive Design Issue."
)


class Command(BaseCommand):
    def create_projects(self):
        for fp in FAKE_PROJECT_NAMES:
            try:
                project, _created = Project.objects.get_or_create(name=fp)
                if _created:
                    project.description = FAKE_DESCRIPTION
                    project.website = "https://project.iashraful.me"
                    project.save()
                    print("Created -- {0}".format(fp))
                elif project and not _created:
                    print("Already Exist -- {0}".format(fp))
                else:
                    print("Not created with unknown errors.")
            except Exception as error:
                print(error)

    def create_issues(self):
        for project in Project.objects.all():
            for title in FAKE_ISSUE_TITLES:
                try:
                    issue = Issue.objects.filter(title=title, project_id=project.pk).first()
                    if not issue:
                        issue = Issue()

                    issue.title = title
                    issue.description = FAKE_DESCRIPTION,
                    issue.project_id = project.pk
                    issue.assigned_to_id = Profile.objects.filter(user__username='john').first().pk
                    issue.author_id = Profile.objects.filter(user__username='jasica').first().pk
                    issue.save()
                except Exception as exp:
                    print(exp)
            print("Issues Created or Updated for project -- {0}".format(project.name))

    def handle(self, *args, **options):
        # Creating projects
        self.create_projects()

        # Creating Issues
        self.create_issues()