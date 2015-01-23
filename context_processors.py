from support.models import Post, WechatSummary
from datetime import datetime, timedelta

def global_app_variables(request):
    wechat_summaries = WechatSummary.objects.all().order_by('-published')
    recent_questions = Post.objects.filter(is_question=True, status='P').order_by('-published')
    hottest_posts = Post.objects.filter(status='P', published__gte=datetime.now()-timedelta(days=7))
    hottest_posts = filter(lambda post: post.vote_count()>0,hottest_posts)
    hottest_posts = sorted(hottest_posts, key=lambda x: x.vote_count(), reverse=True)
    return {'recent_questions': recent_questions,'hottest_posts': hottest_posts, 'wechat_summaries': wechat_summaries}