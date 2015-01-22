from datetime import datetime 
from django.db import models
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import markdown
import bleach

ALLOWED_TAGS_UNKNOWN_USER = [
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'strong',
    'ul',
]
class Vote(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def __unicode__(self):
        self.content_type

class Votable(models.Model):
    votes = GenericRelation(Vote)

    class Meta:
        abstract = True

    def vote_count(self):
        aggregate = self.votes.aggregate(Sum('value'))
        if aggregate['value__sum'] == None:
            return 0
        else:
            return aggregate['value__sum']

    def set_vote(self, user, value):
        if(user.is_authenticated):
            v = self.votes.filter(user= user)
            if v.count() == 0:
                new_vote = self.votes.create(user= user, value=value)
                new_vote.save()
            else:
                v.update(value= value)

class GradeGroup(models.Model):
    name = models.CharField(max_length=200)
    intro_text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __unicode__(self): 
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=200)
    intro_text = models.TextField()
    order = models.IntegerField(default=0)
    grade_group = models.ForeignKey(GradeGroup, blank=True, null=True)
    class Meta:
        ordering = ["order"]

    def __unicode__(self):
        return self.name

    def intro_html(self):
        return markdown.markdown(bleach.clean(self.intro_text))

class Unit(models.Model):
    name = models.CharField(max_length=200)
    intro_text = models.TextField()
    grade = models.ForeignKey(Grade)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ["order"]    

    def __unicode__(self):
        return self.name + " of " + self.grade.name

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    intro_text = models.TextField()
    unit = models.ForeignKey(Unit)
    order = models.IntegerField(default=0)
    week_length = models.IntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __unicode__(self):
        return self.name + " of " + self.unit.name + " of " + self.unit.grade.name

    def intro_html(self):
        return markdown.markdown(bleach.clean(self.intro_text))

    def get_absolute_url(self):
        return reverse('support:lesson', args=[str(self.id)])    

class LessonCategoryType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class LessonCategory(models.Model):
    category_type = models.ForeignKey(LessonCategoryType)
    lesson = models.ForeignKey(Lesson)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __unicode__(self):
        return self.lesson.name + " " + self.category_type.name

    def sorted_posts(self):
        posts = self.post_set.filter(status='P', replying_to=None)
        return sorted(posts, key=lambda x: x.vote_count(), reverse=True)


class Post(Votable):
    PUBLISHED = 'P'
    FLAGGED = 'F'
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (FLAGGED, 'Flagged'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PUBLISHED)
    author = models.ForeignKey(User)
    content_text = models.TextField()
    lesson_category = models.ForeignKey(LessonCategory)
    replying_to = models.ForeignKey('self',blank=True, null=True, related_name='replies')
    is_question = models.BooleanField(default=False)
    date_time = models.DateTimeField(default=datetime.now)


    def content_html(self):
        if self.author.groups.filter(name='Moderators').exists() or self.author.groups.filter(name='Contributors').exists():
            return markdown.markdown(bleach.clean(self.content_text))
        else:
            return bleach.clean(markdown.markdown(self.content_text), tags=ALLOWED_TAGS_UNKNOWN_USER, strip=True)

    def __unicode__(self):
        return self.content_text

    def get_absolute_url(self):
        if hasattr(self.lesson_category, 'lesson'):
            return reverse('support:lesson', args=[str(self.lesson_category.lesson.id)])    + "#post_" + str(self.id)
        return ""

    def sorted_replies(self):
        posts = self.replies.filter(status='P')
        return sorted(posts, key=lambda x: x.vote_count(), reverse=True)

class SupplementalMaterial(models.Model):
    name = models.CharField(max_length=200)
    material_file = models.FileField(upload_to='support/')
    author = models.ForeignKey(User)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ["order"]

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='support/avatar/', blank=True)
    intro_text = models.TextField()

    def __unicode__(self):
        return self.user.username

    def group(self):
        if self.user.groups.filter(name='Moderators').exists():
            return "Moderator"
        elif self.user.groups.filter(name='Contributors').exists():
            return "Contributor"
        else:
            return ""

    def is_moderator(self):
        return self.user.groups.filter(name='Moderators').exists()

    def is_contributor(self):
        return self.user.groups.filter(name='Contributors').exists()



