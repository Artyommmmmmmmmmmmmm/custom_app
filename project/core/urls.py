from django.urls import path, include
from django.views.generic import TemplateView
from .views import ArticleList, AddArticle, ArticleDetail, ArticleChange, ArticleDelete, CommentList, delete_comment, reply_comment

urlpatterns = [
    path('', ArticleList.as_view(), name='list'),
    path('<int:pk>', ArticleDetail.as_view(), name='detail'),
    path('change/<int:pk>', ArticleChange.as_view(), name='change'),
    path('add/', AddArticle.as_view(), name='add'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete'),
    path('comments/<int:pk>', CommentList.as_view(), name='comments'),
    path('comments/delete/<int:pk>', delete_comment, name='delcomment'),
    path('comments/reply/<int:pk>', reply_comment, name='repcomment'),
]