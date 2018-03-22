from django.db import models

class Category(models.Model):
    
    id = models.AutoField(primary_key=True)
    category = models.CharField('Category', max_length=20)
    title = models.CharField('Title', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.FileField(upload_to='tips/images/')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]
