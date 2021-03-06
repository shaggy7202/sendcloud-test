# Generated by Django 3.0.7 on 2020-06-14 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0012_periodictask_expire_seconds'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to=settings.AUTH_USER_MODEL)),
                ('fetcher', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.PeriodicTask')),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('created_by', 'url')},
            },
        ),
    ]
