from django.db import models

class User_Model(models.Model):
    department = models.CharField(max_length=20)
    user_id = models.CharField(max_length=70)

    def __str__(self):
        return self.department

class Store_Model(models.Model):
    store_name = models.CharField(max_length=20)
    first_menu_name = models.CharField(max_length=20)
    first_menu_image = models.ImageField(upload_to='images/')
    contents = models.CharField(max_length=100,blank=True)
    naver_map_URL = models.URLField()
    favorite = models.BooleanField(blank=True)

    def __str__(self):
        return self.store_name

