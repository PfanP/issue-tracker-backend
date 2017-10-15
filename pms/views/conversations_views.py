from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from pms.models.conversations import Conversation, Comment
from pms.serializers.conversations_serializers import ConversationSerializer, CommentSerializer

__author__ = 'Ashraful'


class IssueConversationView(RetrieveAPIView):
    serializer_class = ConversationSerializer

    def get_object(self):
        issue_pk = self.kwargs.get('pk')
        queryset = Conversation.objects.get(issue_id=issue_pk)
        return queryset


class ConversationView(ListCreateAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.filter()


class ConversationDetailsView(RetrieveAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.filter()


class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter()
