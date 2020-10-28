from rest_framework import serializers
from polls_app.models import Question, RegisteredVote


class RegisteredVoteDetailSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='question_text', read_only=True)
    choice = serializers.SlugRelatedField(slug_field='choice', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = RegisteredVote
        fields = "__all__"
