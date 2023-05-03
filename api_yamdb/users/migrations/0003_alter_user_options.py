from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['last_name']},
        ),
    ]
