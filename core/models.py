from django.db import models


class Search(models.Model):
	search  = models.CharField(max_length=200, null=True)
	time  = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.search

	class Meta:
		verbose_name_plural='Searches'