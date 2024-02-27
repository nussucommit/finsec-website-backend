from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) #default length of 100 for name fields
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role_id = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True) #assume we do not want to cascade delete
    subcomm = models.CharField(max_length=100) #subcomms assumed to be a name field

    def __str__(self):
        return str({"user_id": self.user_id, "name": self.name, "email": self.email, "role_id": self.role_id, "subcomm": self.subcomm})

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return str({"role_id": self.role_id, "role_name": self.role_name})
