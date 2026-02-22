# Generated migration for Match model

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team_name', models.CharField(max_length=100, verbose_name='主队中文名')),
                ('home_team_logo', models.CharField(max_length=50, verbose_name='主队英文缩写')),
                ('home_team_score', models.IntegerField(default=0, verbose_name='主队得分')),
                ('away_team_name', models.CharField(max_length=100, verbose_name='客队中文名')),
                ('away_team_logo', models.CharField(max_length=50, verbose_name='客队英文缩写')),
                ('away_team_score', models.IntegerField(default=0, verbose_name='客队得分')),
                ('match_date', models.DateField(verbose_name='比赛日期')),
                ('match_time', models.TimeField(blank=True, null=True, verbose_name='比赛时间')),
                ('status', models.CharField(
                    choices=[('upcoming', '未开始'), ('live', '进行中'), ('finished', '已结束')],
                    default='upcoming',
                    max_length=20,
                    verbose_name='比赛状态'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '比赛',
                'verbose_name_plural': '比赛',
                'db_table': 'match',
                'ordering': ['-match_date', '-match_time'],
            },
        ),
    ]
