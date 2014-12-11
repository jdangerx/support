from django.contrib import admin
from support.models import Grade, Unit, Lesson, SupplementalMaterial, Question, Answer, Topic, TopicGrade, Vote, LessonTopic, Forum, UserProfile
from django.contrib.auth.models import User

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'vote_count')
admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer, QuestionAdmin)
admin.site.register(Vote)
admin.site.register(UserProfile)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    list_editable = ['order']
admin.site.register(Grade, OrderAdmin)
admin.site.register(Unit, OrderAdmin)
admin.site.register(SupplementalMaterial, OrderAdmin)
admin.site.register(Topic, OrderAdmin)

#@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum','order')
    list_editable = ['order']

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

#@admin.register(TopicGrade)
class TopicGradeAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum')

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

#@admin.register(LessonTopic)
class LessonTopicAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum')

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff' ,'karma', 'group')

    def karma(self, obj):
        karma = 0
        for question in obj.question_set.all():
            karma += 1
            karma += question.vote_count()
        for answer in obj.answer_set.all():
            karma += 5
            karma += answer.vote_count()
        return karma

    def group(self, obj):
        if obj.groups.filter(name='Moderators').exists():
            return "Moderator"
        elif obj.groups.filter(name='Contributors').exists():
            return "Contributor"
        else:
            return ""


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(TopicGrade, TopicGradeAdmin)
admin.site.register(LessonTopic, LessonTopicAdmin)