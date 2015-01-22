# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Answer', fields ['question', 'answer_text', 'author']
        db.delete_unique(u'support_answer', ['question_id', 'answer_text', 'author_id'])

        # Deleting model 'TopicGrade'
        db.delete_table(u'support_topicgrade')

        # Deleting model 'Answer'
        db.delete_table(u'support_answer')

        # Deleting model 'Topic'
        db.delete_table(u'support_topic')

        # Deleting model 'Forum'
        db.delete_table(u'support_forum')

        # Deleting model 'Question'
        db.delete_table(u'support_question')

        # Deleting model 'LessonTopic'
        db.delete_table(u'support_lessontopic')

        # Adding model 'LessonCategory'
        db.create_table(u'support_lessoncategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Lesson'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['LessonCategory'])

        # Adding model 'Post'
        db.create_table(u'support_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_text', self.gf('django.db.models.fields.TextField')()),
            ('lesson_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.LessonCategory'])),
            ('replying_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Post'], null=True)),
            ('is_question', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'support', ['Post'])

        # Removing M2M table for field forum on 'SupplementalMaterial'
        db.delete_table(db.shorten_name(u'support_supplementalmaterial_forum'))

        # Deleting field 'Lesson.forum'
        db.delete_column(u'support_lesson', 'forum_id')


    def backwards(self, orm):
        # Adding model 'TopicGrade'
        db.create_table(u'support_topicgrade', (
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['support.Forum'], unique=True)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Grade'])),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topic'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['TopicGrade'])

        # Adding model 'Answer'
        db.create_table(u'support_answer', (
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('answer_text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Question'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['question', 'answer_text', 'author']
        db.create_unique(u'support_answer', ['question_id', 'answer_text', 'author_id'])

        # Adding model 'Topic'
        db.create_table(u'support_topic', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'support', ['Topic'])

        # Adding model 'Forum'
        db.create_table(u'support_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['Forum'])

        # Adding model 'Question'
        db.create_table(u'support_question', (
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('question_text', self.gf('django.db.models.fields.TextField')()),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Forum'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['Question'])

        # Adding model 'LessonTopic'
        db.create_table(u'support_lessontopic', (
            ('forum', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['support.Forum'], unique=True)),
            ('intro_text', self.gf('django.db.models.fields.TextField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.TopicGrade'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Lesson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'support', ['LessonTopic'])

        # Deleting model 'LessonCategory'
        db.delete_table(u'support_lessoncategory')

        # Deleting model 'Post'
        db.delete_table(u'support_post')

        # Adding M2M table for field forum on 'SupplementalMaterial'
        m2m_table_name = db.shorten_name(u'support_supplementalmaterial_forum')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supplementalmaterial', models.ForeignKey(orm[u'support.supplementalmaterial'], null=False)),
            ('forum', models.ForeignKey(orm[u'support.forum'], null=False))
        ))
        db.create_unique(m2m_table_name, ['supplementalmaterial_id', 'forum_id'])

        # Adding field 'Lesson.forum'
        db.add_column(u'support_lesson', 'forum',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['support.Forum'], unique=True),
                      keep_default=False)


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
        u'support.grade': {
            'Meta': {'ordering': "['order']", 'object_name': 'Grade'},
            'grade_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.GradeGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.gradegroup': {
            'Meta': {'ordering': "['order']", 'object_name': 'GradeGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.lesson': {
            'Meta': {'ordering': "['order']", 'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Unit']"}),
            'week_length': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'support.lessoncategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'LessonCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Lesson']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'content_text': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_question': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lesson_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.LessonCategory']"}),
            'replying_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Post']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'})
        },
        u'support.supplementalmaterial': {
            'Meta': {'ordering': "['order']", 'object_name': 'SupplementalMaterial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.unit': {
            'Meta': {'ordering': "['order']", 'object_name': 'Unit'},
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['support.Grade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'support.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
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