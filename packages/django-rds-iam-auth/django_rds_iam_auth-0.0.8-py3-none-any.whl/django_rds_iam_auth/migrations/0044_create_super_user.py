from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('django_rds_iam_auth', '0043_auto_20210915_1647'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.conf import settings

        from django_rds_iam_auth.models import User
        superuser = User.objects.create_superuser(
            username=settings.DJANGO_SU_NAME,
            email=settings.DJANGO_SU_EMAIL,
            password=settings.DJANGO_SU_PASSWORD)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
