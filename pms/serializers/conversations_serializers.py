from rest_framework import serializers

from pms.models.conversations import Conversation, Comment, Reply

__author__ = 'Ashraful'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'text')


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'replies')


class ConversationSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'comment')
