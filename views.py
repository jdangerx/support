from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse

from support.models import Grade, Topic, Lesson, Question, Answer, SupplementalMaterial, TopicGrade, Forum
from support.forms import SignUpForm, SupplementalMaterialForm

def index(request):
	all_grades = Grade.objects.all()
	all_topics = Topic.objects.all()
	context = {'all_grades': all_grades, 'all_topics': all_topics}
	return render(request, 'support/index.html', context)

def grade(request, grade_id):
	grade = get_object_or_404(Grade, pk=grade_id)
	return render(request, 'support/grade.html', {'grade': grade})

def topic(request, topic_id):
	topic = get_object_or_404(Topic, pk=topic_id)
	return render(request, 'support/topic.html', {'topic': topic})

def lesson(request, lesson_id):
	lesson = get_object_or_404(Lesson, pk=lesson_id)
	user_is_moderator = False
	if request.user.is_authenticated() and request.user.groups.filter(name='moderator').count() > 0:
		user_is_moderator = True
	return render(request, 'support/lesson.html', {'lesson': lesson, 'user_is_moderator': user_is_moderator})

def topic_grade(request, topic_grade_id):
	topic_grade = get_object_or_404(TopicGrade, pk=topic_grade_id)
	return render(request, 'support/topic_grade.html', {'topic_grade': topic_grade})

def ask(request):
	if request.method == 'POST':	
		question_text = request.POST['question']
		forum_id = request.POST['forum']
		forum = get_object_or_404(Forum, pk=forum_id)
		if(request.user.is_authenticated):
			q = Question.objects.create(question_text=question_text, author= request.user, forum= forum )
			q.save()

		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		else: 
			next_page = request.path     
		return HttpResponseRedirect(next_page)
	else: 
		return render(request, 'support/index.html', {'all_grades': Grades.objects.all(), 'all_topics': Topics.objects.all()})

def up_vote_question(request, question_id):
	if(request.user.is_authenticated):
		question = get_object_or_404(Question, pk=question_id)
		question.set_vote(request.user, 1)

		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		if next_page:
			return HttpResponseRedirect(next_page)
		
		return render(request, 'support/lesson.html', {'lesson': question.get_lesson()})

def down_vote_question(request, question_id):
	if(request.user.is_authenticated):
		question = get_object_or_404(Question, pk=question_id)
		question.set_vote(request.user, -1)

		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		if next_page:
			return HttpResponseRedirect(next_page)
		
		return render(request, 'support/lesson.html', {'lesson': question.get_lesson()})

def answer(request):
	if request.method == 'POST':	
		question = get_object_or_404(Question, pk=request.POST['question'])
		answer_text = request.POST['answer']
		if(request.user.is_authenticated):
			a = question.answer_set.create(answer_text= answer_text, author= request.user )
			a.save()

		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		else: 
			next_page = request.path     
		return HttpResponseRedirect(next_page)
	else: 
		return render(request, 'support/index.html', {'all_grades': Grades.objects.all(), 'all_topics': Topics.objects.all()})

def up_vote_answer(request, answer_id):
	if(request.user.is_authenticated):
		answer = get_object_or_404(Answer, pk=answer_id)
		answer.set_vote(request.user, 1)

		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		if next_page:
			return HttpResponseRedirect(next_page)
		return render(request, 'support/lesson.html', {'lesson': answer.question.get_lesson()})

def down_vote_answer(request, answer_id):
	if(request.user.is_authenticated):
		answer = get_object_or_404(Answer, pk=answer_id)
		answer.set_vote(request.user, -1)
		if('next' in request.POST or 'next' in request.GET):
			next_page = request.POST.get('next', request.GET.get('next'))
			# Security check -- don't allow redirection to a different host.
			if not is_safe_url(url=next_page, host=request.get_host()):
				next_page = request.path
		if next_page:
			return HttpResponseRedirect(next_page)	
		
		return render(request, 'support/lesson.html', {'lesson': answer.question.get_lesson()})

def sign_up(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/support/')
	else:
		form = SignUpForm()

	return render(request, 'support/sign_up.html', {'form': form})

def upload_supplemental_material(request, lesson_id):
	lesson = get_object_or_404(Lesson, pk=lesson_id)
	if request.user.is_authenticated and request.user.groups.filter(name='moderator').exists():
		if request.method == 'POST':	
			sm = SupplementalMaterial.objects.create(author=request.user, lesson=lesson, order=0)
			form = SupplementalMaterialForm(request.POST, request.FILES, instance=sm)
			form.save()
			return HttpResponseRedirect('/support/')
		else:
			form = SupplementalMaterialForm()

		return render(request, 'support/upload_supplemental_material.html', {'form': form, 'lesson':lesson})
	else:
		return HttpResponseRedirect('/support/')