from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    verbose_name = "Custom User"
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=1024)
    role = models.CharField(max_length=255, default='user')


    class Meta:
        db_table = "users"  # Explicitly specify the database table name as `users`
        managed = True  # Let Django only use this table, not manage it (will not create or modify this table)

class Show(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    address = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "show_info"
        managed = True

class Favorite(models.Model):
    f_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    show_id = models.CharField(max_length=255)

    class Meta:
        db_table = "favorite"
        managed = True