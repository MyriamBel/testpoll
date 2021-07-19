from django.urls import include, path
from .views import ActivePollsView, DetailPollView, UpdatePollView, DeletePollView, CreatePollView
from .views import CreateQuestionView, UpdateQuestionView, DeleteQuestionView
from .views import CreateChoiceView, UpdateChoiceView, DeleteChoiceView, VoteViewSet


urlpatterns = [
    path('polls/', include([
        path('', ActivePollsView.as_view()),
        path('<int:pk>/', DetailPollView.as_view()),
        path('<int:pk>/questions/<int:question_pk>/answers/', VoteViewSet.as_view()),
        path('create/', CreatePollView.as_view()),
        path('update/<int:pk>/', UpdatePollView.as_view()),
        path('delete/<int:pk>/', DeletePollView.as_view()),
    ]
    )),
    path('questions/', include([
        path('create/', CreateQuestionView),
        path('update/<int:pk>/', UpdateQuestionView.as_view()),
        path('delete/<int:pk>/', DeleteQuestionView.as_view()),
    ])),
    path('choices/', include([
        path('create/', CreateChoiceView.as_view()),
        path('update/<int:pk>/', UpdateChoiceView.as_view()),
        path('delete/<int:pk>/', DeleteChoiceView.as_view()),
    ])),
    path('answers/', include([
        path('', CreateChoiceView.as_view()),
    ]))

]

