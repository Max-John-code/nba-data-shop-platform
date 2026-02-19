# Generated migration for adding player_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_type',
            field=models.CharField(
                choices=[('ranking', '联盟榜单'), ('star', '现役球星')],
                default='ranking',
                max_length=20,
                verbose_name='类型'
            ),
        ),
    ]
