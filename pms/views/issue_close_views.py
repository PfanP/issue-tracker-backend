from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pms.models import Issue
from pms.helpers.enums import IssueStatusEnum

__author__ = "Ashraful Islam"


class IssueCloseView(APIView):
	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		data = request.data

		status, issues_pks = None, []

		if 'issue_close' in data.keys():
			status = data['issue_close']
		if 'issues' in data.keys():
			issues_pks = data['issues']

		if status and issues_pks:
			Issue.objects.filter(pk__in=issues_pks).update(status=IssueStatusEnum.CLOSE.value)
			return Response(data=request.data)
		return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
