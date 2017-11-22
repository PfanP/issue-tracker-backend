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
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'replies')

    def get_replies(self, obj):
        entries = obj.replies.order_by('-created_at', '-updated_at')
        data = ReplySerializer(entries, many=True).data
        return data


class ConversationSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'comments')

    def get_comments(self, obj):
        entries = obj.comments.order_by('-created_at', '-updated_at')
        data = CommentSerializer(entries, many=True).data
        return data
