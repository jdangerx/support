from django.contrib import admin
from support.models import Grade, GradeGroup, Unit, Lesson, SupplementalMaterial, Vote, LessonCategory, LessonCategoryType, UserProfile, Post, WechatSummary
from django.contrib.auth.models import User

class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'vote_count')
admin.site.register(Post, PostAdmin)

admin.site.register(Vote)
admin.site.register(UserProfile)
admin.site.register(LessonCategoryType)
admin.site.register(WechatSummary)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    list_editable = ['order']

admin.site.register(Grade, OrderAdmin)
admin.site.register(Unit, OrderAdmin)
admin.site.register(SupplementalMaterial, OrderAdmin)
admin.site.register(GradeGroup, OrderAdmin)

class LessonCategoryInline(admin.TabularInline):
    model = LessonCategory

class LessonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    list_editable = ['order']
    inlines = [
        LessonCategoryInline,
        ]
admin.site.register(Lesson,LessonAdmin)
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