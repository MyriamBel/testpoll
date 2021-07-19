from rest_framework import generics, permissions
from .models import Poll, Question, Choice, Vote
from .serializers import AllActivePollsSerializer, QuestionSerializer, ChoiceSerializer, \
    QuestionCreateSerializer, VoteSerializer
from django.utils import timezone
from django.db.models import Q
from rest_framework import pagination


class ActivePollsView(generics.ListAPIView):
    """Просмотр всех активных опросов"""

    serializer_class = AllActivePollsSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        print(self.request.COOKIES)
        queryset = Poll.objects.filter(Q(end_date__gte=timezone.now().date().today()) | Q(end_date=None)).order_by(
            'start_date')
        return queryset


class CreatePollView(generics.CreateAPIView):
    """Создание нового опроса"""

    serializer_class = AllActivePollsSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UpdatePollView(generics.UpdateAPIView):
    """Изменение опроса"""

    serializer_class = AllActivePollsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Poll.objects.get(id=self.kwargs['pk'])
        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        print(self.request)
        if self.request.method in ['PUT', 'PATCH']:
            setattr(serializer_class.Meta, 'read_only_fields', ('start_date',))
        else:
            delattr(serializer_class.Meta, 'read_only_fields')
        return serializer_class


class DeletePollView(generics.DestroyAPIView):
    """Удаление опроса"""

    serializer_class = AllActivePollsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Poll.objects.get(id=self.kwargs['pk'])
        return queryset


class DetailPollView(generics.ListAPIView):
    """Просмотр Вопросов в опросе"""

    serializer_class = QuestionSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        queryset = Question.objects.filter(poll=self.kwargs['pk'])
        return queryset


class CreateQuestionView(generics.CreateAPIView):
    """Создание Вопросов для опроса"""

    serializer_class = QuestionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UpdateQuestionView(generics.UpdateAPIView):
    """Изменение вопроса"""

    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Question.objects.get(id=self.kwargs['pk'])
        return queryset


class DeleteQuestionView(generics.DestroyAPIView):
    """Удаление вопроса"""

    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Question.objects.get(id=self.kwargs['pk'])
        return queryset


class CreateChoiceView(generics.CreateAPIView):
    """Создание ответов для опроса"""

    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UpdateChoiceView(generics.UpdateAPIView):
    """Изменение ответа"""

    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Choice.objects.get(id=self.kwargs['pk'])
        return queryset


class DeleteChoiceView(generics.DestroyAPIView):
    """Удаление ответа"""

    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = Choice.objects.get(id=self.kwargs['pk'])
        return queryset


class VoteViewSet(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data.update({'user': request.COOKIES['sessionid']})
        request.data._mutable = False
        return super(VoteViewSet, self).create(request, *args, **kwargs)
