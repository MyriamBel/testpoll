from rest_framework import serializers, exceptions
from .models import Poll, Question, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):

    """Варианты ответов"""

    class Meta:
        model = Choice
        fields = '__all__'

    def validate(self, attrs):
        if attrs['question'].type == Question.Type.TEXT:
            raise exceptions.ValidationError(
                'Нельзя задавать ответы для вопроса, на который должен ответить сам пользователь')
        return attrs


class QuestionSerializer(serializers.ModelSerializer):

    """Вопросы"""

    choices = ChoiceSerializer(many=True, read_only=True)
    type = serializers.ChoiceField(choices=Question.Type.choice_type, default=Question.Type.ONE)

    class Meta:
        model = Question
        exclude = ('poll', )


class QuestionCreateSerializer(serializers.ModelSerializer):

    """Для создания вопросов"""

    type = serializers.ChoiceField(choices=Question.Type.choice_type, default=Question.Type.ONE)

    class Meta:
        model = Question
        fields = '__all__'


class AllActivePollsSerializer(serializers.ModelSerializer):

    """Опросы"""

    class Meta:
        model = Poll
        fields = '__all__'

    questions = QuestionSerializer(many=True, read_only=True)


class VoteSerializer(serializers.ModelSerializer):

    """Выбор пользователей"""

    class Meta:
        model = Vote
        fields = '__all__'
