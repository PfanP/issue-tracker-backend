from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from pms.models.conversations import Conversation, Comment
from pms.serializers.conversations_serializers import ConversationSerializer, CommentSerializer, ReplySerializer

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


class ConversationDetailsView(APIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.filter()

    def get(self, request, *args, **kwargs):
        data = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        current_user = request.user.profile.pk
        if 'comment' in data.keys() and data.get('comment') is True:
            # Here will Comment save
            comment_serializer = CommentSerializer(data=data)
            if comment_serializer.is_valid(raise_exception=True):
                comment = comment_serializer.save(author_id=current_user)
                if comment:
                    conv = self.queryset.get(pk=kwargs.get('pk'))
                    conv.comment_id = comment.pk
                    conv.save()
            return Response(data=comment_serializer.data)
        if 'reply' in data.keys() and data.get('reply') is True:
            # Here will be reply save
            reply_serializer = ReplySerializer(data=data)
            comment_pk = data.get('comment_id')
            if reply_serializer.is_valid(raise_exception=True):
                reply = reply_serializer.save(author_id=current_user)
                comment = Comment.objects.get(pk=comment_pk)
                comment.replies.add(reply)
            return Response(data=reply_serializer.data)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)


class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter()
