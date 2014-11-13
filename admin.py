from django.contrib import admin
from support.models import Grade, Unit, Lesson, SupplementalMaterial, Question, Answer, Topic, TopicGrade, Vote, LessonTopic, Forum


admin.site.register(Question)
admin.site.register(Answer)

admin.site.register(Vote)

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

admin.site.register(Lesson, LessonAdmin)
admin.site.register(TopicGrade, TopicGradeAdmin)
admin.site.register(LessonTopic, LessonTopicAdmin)