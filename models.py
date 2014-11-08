from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Vote(models.Model):
	user = models.ForeignKey(User)
	value = models.IntegerField(default=0)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		unique_together = ("user", "content_type", "object_id")

	def __str__(self):
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

class Forum(models.Model):

	def sorted_questions(self):
		questions = self.question_set.all()
		return sorted(questions, key=lambda x: x.vote_count(), reverse=True)

	def __str__(self):
		return str(self.pk)

class Grade(models.Model):
	name = models.CharField(max_length=200)
	intro_text = models.TextField()
	order = models.IntegerField(default=0)
	class Meta:
		ordering = ["order"]

	def __str__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=200)
	grade = models.ForeignKey(Grade)
	order = models.IntegerField(default=0)
	class Meta:
		ordering = ["order"]	

	def __str__(self):
		return self.name + " of " + self.grade.name

class Topic(models.Model):
	name = models.CharField(max_length=200)
	intro_text = models.TextField()
	grade = models.ManyToManyField(Grade, through='TopicGrade')
	order = models.IntegerField(default=0)
	class Meta:
		ordering = ["order"]

	def __str__(self):
		return self.name

class Lesson(models.Model):
	name = models.CharField(max_length=200)
	intro_text = models.TextField()
	unit = models.ForeignKey(Unit)
	order = models.IntegerField(default=0)
	forum = models.OneToOneField(Forum)

	class Meta:
		ordering = ["order"]

	def __str__(self):
		return self.name + " of " + self.unit.name + " of " + self.unit.grade.name

	def sorted_questions(self):
		questions = self.forum.question_set.all()
		for lesson_topic in self.lessontopic_set.all():
			questions = questions | lesson_topic.forum.question_set.all()
		return sorted(questions, key=lambda x: x.vote_count(), reverse=True)


class Question(Votable):
	question_text = models.TextField()
	author = models.ForeignKey(User)
	forum = models.ForeignKey(Forum)

	def __str__(self):
		return self.question_text

	def sorted_answers(self):
		return sorted(self.answer_set.all(), key=lambda x: x.vote_count(), reverse=True)

class TopicGrade(models.Model):
	intro_text = models.TextField()
	topic = models.ForeignKey(Topic)
	grade = models.ForeignKey(Grade)	
	forum = models.OneToOneField(Forum)

	def __str__(self):
		return self.grade.name + " " + self.topic.name 

	def name(self):
		return self.grade.name + " " + self.topic.name 


class SupplementalMaterial(models.Model):
	name = models.CharField(max_length=200)
	material_file = models.FileField(upload_to='support/')
	lesson = models.ForeignKey(Lesson)
	author = models.ForeignKey(User)
	order = models.IntegerField(default=0)
	class Meta:
		ordering = ["order"]

	def __str__(self):
		return self.name

class Answer(Votable):
	answer_text = models.TextField()
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)

	class Meta:
		unique_together = ("question", "answer_text", "author")

	def __str__(self):
		return self.answer_text

class LessonTopic(models.Model):
	intro_text = models.TextField()
	lesson = models.ForeignKey(Lesson)
	topic = models.ForeignKey(TopicGrade)
	forum = models.OneToOneField(Forum)
	
	def __str__(self):
		return self.lesson.name + " " + self.topic.topic.name

	def name(self):
		return self.lesson.name + " " + self.topic.topic.name