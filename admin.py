from django.contrib import admin
from support.models import Grade, Unit, Lesson, SupplementalMaterial, Question, Answer, Topic, TopicGrade, Vote, LessonTopic, Forum

admin.site.register(Grade)
admin.site.register(Unit)
admin.site.register(SupplementalMaterial)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Topic)
admin.site.register(Vote)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum')

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

@admin.register(TopicGrade)
class TopicGradeAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum')

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

@admin.register(LessonTopic)
class LessonTopicAdmin(admin.ModelAdmin):
    exclude = ('forum',)
    list_display = ('__str__', 'forum')

    def save_model(self, request, obj, form, change):
        if change == False:
            forum = Forum.objects.create()
            forum.save()
            obj.forum = forum
        obj.save()

# Register your models here.
