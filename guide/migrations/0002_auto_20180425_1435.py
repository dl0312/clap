# Generated by Django 2.0.4 on 2018-04-25 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AchievementMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_reason', models.CharField(max_length=64)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guide.Achievement')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievementmember_invites', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Image')),
                ('icon', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='guide.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guide.Game')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamemember_invites', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guide.Post'),
        ),
        migrations.AlterField(
            model_name='wikiimage',
            name='image',
            field=models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='game',
            name='members',
            field=models.ManyToManyField(through='guide.GameMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievement',
            name='members',
            field=models.ManyToManyField(through='guide.AchievementMember', to=settings.AUTH_USER_MODEL),
        ),
    ]