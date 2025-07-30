from django.urls import path
from . import views

urlpatterns = [
    path('all/',view=views.get_all_resources),
    path('<int:resource_id>/',view=views.get_resource),
    path('author/<int:author_id>/',view=views.get_resources_by_author),
    path('subject/<int:subject_id>/',view=views.get_resources_by_subject),
    path('add/',view=views.add_resource),
    path('update/<int:resource_id>/',view=views.update_resource),
    path('delete/<int:resource_id>/',view=views.delete_resource),
    path('report/<int:resource_id>/',view=views.report_resource),
    #question
    path('question/<int:question_id>/',view=views.get_question),
    path('question/add/',view=views.add_question),
    path('question/update/<int:question_id>/',view=views.update_question),
    path('question/delete/<int:question_id>/',view=views.delete_question),
    path('question/report/<int:question_id>/',view=views.report_question),
    path('question/subject/<int:subject_id>/',view=views.get_question_by_subject),
    path('question/author/<int:author_id>/',view=views.get_questions_by_author),
    #reply
    path('reply/<int:reply_id>/',view=views.get_reply),
    path('reply/add/',view=views.add_reply),
    path('reply/update/<int:reply_id>/',view=views.update_reply),
    path('reply/delete/<int:reply_id>/',view=views.delete_reply),
    path('reply/report/<int:reply_id>/',view=views.report_reply),
    path('reply/question/<int:question_id>/',view=views.get_replies_by_question),
    #image
    path('question/images/<int:qst_id>/view/',view=views.get_qst_images),
    path('reply/images/<int:reply_id>/view/',view=views.get_reply_images),
    path('question/images/<int:qst_id>/upload/',view=views.add_images_to_qst),
    path('reply/images/<int:reply_id>/upload/',view=views.add_images_to_reply),
    path('question/images/<int:qst_id>/delete/',view=views.delete_qst_images),
    path('reply/images/<int:reply_id>/delete/',view=views.delete_reply_images),

]
