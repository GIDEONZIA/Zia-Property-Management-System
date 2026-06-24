from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0004_alter_mpesaauditlog_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE django_q_task ALTER COLUMN started DROP NOT NULL;",
            reverse_sql="ALTER TABLE django_q_task ALTER COLUMN started SET NOT NULL;"
        ),
    ]