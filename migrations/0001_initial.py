# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table(u'support_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'support', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'content_type', 'object_id']
        db.create_unique(u'support_vote', ['user_id', 'content_type_id', 'object_id'])

        # Adding model 'Forum'
        db.create_table(u'support_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['Forum'])

        # Adding model 'Grade'
        db.create_table(u'support_grade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['Grade'])

        # Adding model 'Unit'
        db.create_table(u'support_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Grade'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['Unit'])

        # Adding model 'Topic'
        db.create_table(u'support_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['Topic'])

        # Adding model 'Lesson'
        db.create_table(u'support_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Unit'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['support.Forum'], unique=True)),
        ))
        db.send_create_signal(u'support', ['Lesson'])

        # Adding model 'Question'
        db.create_table(u'support_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Forum'])),
        ))
        db.send_create_signal(u'support', ['Question'])

        # Adding model 'TopicGrade'
        db.create_table(u'support_topicgrade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topic'])),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Grade'])),
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['support.Forum'], unique=True)),
        ))
        db.send_create_signal(u'support', ['TopicGrade'])

        # Adding model 'SupplementalMaterial'
        db.create_table(u'support_supplementalmaterial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('material_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Lesson'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['SupplementalMaterial'])

        # Adding model 'Answer'
        db.create_table(u'support_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer_text', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Question'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'support', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['question', 'answer_text', 'author']
        db.create_unique(u'support_answer', ['question_id', 'answer_text', 'author_id'])

        # Adding model 'LessonTopic'
        db.create_table(u'support_lessontopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Lesson'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.TopicGrade'])),
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['support.Forum'], unique=True)),
        ))
        db.send_create_signal(u'support', ['LessonTopic'])


    def backwards(self, orm):
        # Removing unique constraint on 'Answer', fields ['question', 'answer_text', 'author']
        db.delete_unique(u'support_answer', ['question_id', 'answer_text', 'author_id'])

        # Removing unique constraint on 'Vote', fields ['user', 'content_type', 'object_id']
        db.delete_unique(u'support_vote', ['user_id', 'content_type_id', 'object_id'])

        # Deleting model 'Vote'
        db.delete_table(u'support_vote')

        # Deleting model 'Forum'
        db.delete_table(u'support_forum')

        # Deleting model 'Grade'
        db.delete_table(u'support_grade')

        # Deleting model 'Unit'
        db.delete_table(u'support_unit')

        # Deleting model 'Topic'
        db.delete_table(u'support_topic')

        # Deleting model 'Lesson'
        db.delete_table(u'support_lesson')

        # Deleting model 'Question'
        db.delete_table(u'support_question')

        # Deleting model 'TopicGrade'
        db.delete_table(u'support_topicgrade')

        # Deleting model 'SupplementalMaterial'
        db.delete_table(u'support_supplementalmaterial')

        # Deleting model 'Answer'
        db.delete_table(u'support_answer')

        # Deleting model 'LessonTopic'
        db.delete_table(u'support_lessontopic')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'support.answer': {
            'Meta': {'unique_together': "(('question', 'answer_text', 'author'),)", 'object_name': 'Answer'},
            'answer_text': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Question']"})
        },
        u'support.forum': {
            'Meta': {'object_name': 'Forum'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'support.grade': {
            'Meta': {'ordering': "['order']", 'object_name': 'Grade'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.lesson': {
            'Meta': {'ordering': "['order']", 'object_name': 'Lesson'},
            'forum': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['support.Forum']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Unit']"})
        },
        u'support.lessontopic': {
            'Meta': {'object_name': 'LessonTopic'},
            'forum': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['support.Forum']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Lesson']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.TopicGrade']"})
        },
        u'support.question': {
            'Meta': {'object_name': 'Question'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {})
        },
        u'support.supplementalmaterial': {
            'Meta': {'ordering': "['order']", 'object_name': 'SupplementalMaterial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Lesson']"}),
            'material_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.topic': {
            'Meta': {'ordering': "['order']", 'object_name': 'Topic'},
            'grade': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['support.Grade']", 'through': u"orm['support.TopicGrade']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.topicgrade': {
            'Meta': {'object_name': 'TopicGrade'},
            'forum': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['support.Forum']", 'unique': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Grade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Topic']"})
        },
        u'support.unit': {
            'Meta': {'ordering': "['order']", 'object_name': 'Unit'},
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Grade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.vote': {
            'Meta': {'unique_together': "(('user', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['support']