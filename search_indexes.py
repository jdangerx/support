from haystack import indexes
from support.models import Post, Lesson

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content_text')

    def get_model(self):
        return Post

class LessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='intro_text')

    def get_model(self):
        return Lesson