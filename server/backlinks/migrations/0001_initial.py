from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('org', '0002_website_only_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='BacklinkAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=253)),
                ('result', models.JSONField(blank=True, null=True)),
                ('status_job', models.CharField(blank=True, max_length=20, null=True)),
                ('task_id', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='backlink_audits', to='org.website')),
            ],
        ),
    ]
