from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Count, Q

from support.models import Grade, GradeGroup, Lesson, Post, SupplementalMaterial, LessonCategory
from support.forms import SignUpForm, SupplementalMaterialForm


#helper function for sorting users by votes
def user_votes(user):
    votes = 0
    for post in user.post_set.all():
        votes += post.vote_count()
    return votes

def index(request):
    all_grades_groups = GradeGroup.objects.all()
    all_users = User.objects.annotate(Count('post')).filter(Q(post__count__gt=0))
    all_users = sorted(all_users, key=lambda user: user_votes(user), reverse=True)
    context = {'all_grades_groups': all_grades_groups, 'all_users': all_users}
    return render(request, 'support/index.html', context)

def grade_group(request, grade_group_id):
    grade_group = get_object_or_404(GradeGroup, pk=grade_group_id)
    return render(request, 'support/grade_group.html', {'grade_group': grade_group})

def lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    user_is_moderator = False
    user_is_contributor = False
    if request.user.is_authenticated() and request.user.groups.filter(name='Moderators').exists():
        user_is_moderator = True
    if request.user.is_authenticated() and request.user.groups.filter(name='Contributors').exists():
        user_is_contributor = True
    return render(request, 'support/lesson.html', {'lesson': lesson, 'user_is_moderator': user_is_moderator, 'user_is_contributor': user_is_contributor})


def create_post(request, lesson_category_id):
    if request.method == 'POST':    
        content_text = request.POST['content_text']
        is_question = False
        print(request.POST)
        if 'is_question' in request.POST:
            is_question = True
        reply_to = None
        if 'reply_to' in request.POST:
            reply_to =  get_object_or_404(Post, pk=int(request.POST['reply_to']))
        lessonCategory = get_object_or_404(LessonCategory, pk=lesson_category_id)
        if(request.user.is_authenticated):
            p = Post.objects.create(content_text=content_text, author= request.user, lesson_category= lessonCategory, 
                is_question=is_question, replying_to=reply_to )
            p.save()

        if('next' in request.POST or 'next' in request.GET):
            next_page = request.POST.get('next', request.GET.get('next'))
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path
        else: 
            next_page = request.path     
        return HttpResponseRedirect(next_page)
    else: 
        all_grades_groups = GradeGroup.objects.all()
        all_users = User.objects.annotate(Count('post')).filter(Q(post__count__gt=0))
        all_users = sorted(all_users, key=lambda user: user_votes(user), reverse=True)
        context = {'all_grades_groups': all_grades_groups, 'all_users': all_users}
        return render(request, 'support/index.html', context)

def up_vote(request, post_id):
    if(request.user.is_authenticated):
        post = get_object_or_404(Post, pk=post_id)
        post.set_vote(request.user, 1)

        if('next' in request.POST or 'next' in request.GET):
            next_page = request.POST.get('next', request.GET.get('next'))
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path
        if next_page:
            return HttpResponseRedirect(next_page)
        
        return render(request, 'support/lesson.html', {'lesson': post.lesson_category.lesson})

def down_vote(request, post_id):
    if(request.user.is_authenticated):
        post = get_object_or_404(Post, pk=post_id)
        post.set_vote(request.user, -1)

        if('next' in request.POST or 'next' in request.GET):
            next_page = request.POST.get('next', request.GET.get('next'))
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path
        if next_page:
            return HttpResponseRedirect(next_page)
        
        return render(request, 'support/lesson.html', {'lesson': post.lesson_category.lesson})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated and request.user.id == post.author.id:
        post.content_text = request.POST['content_text']
        post.save()

        if('next' in request.POST or 'next' in request.GET):
            next_page = request.POST.get('next', request.GET.get('next'))
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path
        if next_page:
            return HttpResponseRedirect(next_page)


def flag_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.status = 'F'
    post.save();

    if('next' in request.POST or 'next' in request.GET):
        next_page = request.POST.get('next', request.GET.get('next'))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path
    if next_page:
        return HttpResponseRedirect(next_page)    

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/support/login/')
    else:
        form = SignUpForm()

    return render(request, 'support/sign_up.html', {'form': form})

def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'support/user.html', {'user': user})

def upload_supplemental_material(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists():
        if request.method == 'POST':    
            sm = SupplementalMaterial.objects.create(author=request.user, forum=forum, order=0)
            form = SupplementalMaterialForm(request.POST, request.FILES, instance=sm)
            form.save()
            return HttpResponseRedirect(forum.get_absolute_url())
        else:
            form = SupplementalMaterialForm()

        return render(request, 'support/upload_supplemental_material.html', {'form': form, 'forum':forum})
    else:
        return HttpResponseRedirect('/support/')