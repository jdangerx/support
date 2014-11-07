# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('intro_text', models.TextField()),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('intro_text', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('forum', models.OneToOneField(to='support.Forum')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intro_text', models.TextField()),
                ('forum', models.OneToOneField(to='support.Forum')),
                ('lesson', models.ForeignKey(to='support.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(to='support.Forum')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplementalMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('material_file', models.FileField(upload_to=b'')),
                ('order', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(to='support.Lesson')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('intro_text', models.TextField()),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intro_text', models.TextField()),
                ('forum', models.OneToOneField(to='support.Forum')),
                ('grade', models.ForeignKey(to='support.Grade')),
                ('topic', models.ForeignKey(to='support.Topic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('grade', models.ForeignKey(to='support.Grade')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'content_type', 'object_id')]),
        ),
        migrations.AddField(
            model_name='topic',
            name='grade',
            field=models.ManyToManyField(to='support.Grade', through='support.TopicGrade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lessontopic',
            name='topic',
            field=models.ForeignKey(to='support.TopicGrade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='unit',
            field=models.ForeignKey(to='support.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='support.Question'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'answer_text', 'author')]),
        ),
    ]
