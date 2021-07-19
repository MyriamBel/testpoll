from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    name = models.CharField(max_length=255, verbose_name='Название опроса')
    description = models.TextField(verbose_name='Описание опроса', blank=True) #разрешаем не заполнять, в бд будет как ''
    start_date = models.DateField(verbose_name='Дата начала', null=True, blank=True) #разрешаем пустую строку и не заполнять
    end_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True) #разрешаем пустую строку и не заполнять

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date().today()
        super(Poll, self).save(*args, **kwargs)

    def prepare_database_save(self, field):
        if self.start_date:
            raise ValueError('Это поле не редактируется')
        super(Poll, self).save()


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    class Type:
        TEXT = 'TEXT'
        ONE = 'ONE'
        MANY = 'MANY'

        choice_type = [
            (TEXT, 'Текст'),
            (ONE, 'Один вариант ответа'),
            (MANY, 'Несколько вариантов ответа'),
        ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Опрос', related_name='questions')
    text = models.TextField(verbose_name='Вопрос')
    type = models.CharField(max_length=5, choices=Type.choice_type, default=Type.ONE, verbose_name='Тип ответов')

    def __str__(self):
        return self.text


class Choice(models.Model):
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    class Type:
        ANSWER = 'ANSWER'
        CHOICE = 'CHOICE'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='choices')
    text = models.CharField(max_length=255, verbose_name='Текст ответа')

    def __str__(self):
        return self.text

    def clean(self):
        if self.question.type == Question.Type.TEXT:
            raise ValidationError('Нельзя задавать ответы для вопроса, на который должен ответить сам пользователь')


class Vote(models.Model):
    class Meta:
        verbose_name = 'Вариант выбора'
        verbose_name = 'Вырианты выбора'
        unique_together = ("poll", "question", "choice", )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes_poll')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes_question', )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name='Вариант ответа', related_name='votes_choice')
    user = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} выбрал {self.choice}'


class UserCustomAnswer(models.Model):
    class Meta:
        verbose_name = 'Пользовательский ответ'
        verbose_name = 'Пользовательские ответы'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255)

    def __str__(self):
        return '{} ответил на вопрос {} так: {}'.format(self.user, self.question, self.text)
