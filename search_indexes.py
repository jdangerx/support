from haystack import indexes
from support.models import Question, Answer, Lesson

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='question_text')

    def get_model(self):
        return Question

class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='answer_text')

    def get_model(self):
        return Answer

class LessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Lesson