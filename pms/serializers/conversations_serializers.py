from rest_framework import serializers

from core.serializers.profile_serializers import ProfileLiteSerializer
from pms.models.conversations import Conversation, Comment, Reply

__author__ = 'Ashraful'


class ReplySerializer(serializers.ModelSerializer):
    author = ProfileLiteSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'author', 'text')


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileLiteSerializer(read_only=True)
    replies = ReplySerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'replies')


class ConversationSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'comment')
