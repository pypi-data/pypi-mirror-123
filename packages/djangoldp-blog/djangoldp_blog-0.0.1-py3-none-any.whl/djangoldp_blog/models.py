from django.db import models
from djangoldp.models import Model
from django.contrib.auth import get_user_model

class Article(Model):
    title = models.TextField()
    text = models.TextField(null=True)
    picture = models.URLField(blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        auto_author = 'author'
        owner_field = 'author'
        ordering = ['-dateCreated']
        container_path = "articles"
        rdf_type = 'hd:article'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']

    def __str__(self):
        return '{}'.format(self.title)