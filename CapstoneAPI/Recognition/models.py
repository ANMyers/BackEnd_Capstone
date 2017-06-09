from django.contrib.auth.models import *
from django.db import models

class Project(models.Model):
	"""
	Project model is pertaining to each user's project.

	Contains:
		name(string): Name of the project.
		algorithm(string): Name of the algorithm used in the project.
		user(user instance): foreign key related to user table.

	Author:
		Adam Myers
	"""
	name = models.CharField(max_length=50)
	algorithm = models.CharField(max_length=50)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)

class ProjectDataset(models.Model):
	"""
	ProjectDataset model is pertaining to each user's dataset for a related project.

	Contains:
		dataset(string): One individual dataset as part of the whole dataset collection.
		user(user instance): foreign key related to user table.
		project(project instance): foreign key related to project table.

	Author:
		Adam Myers
	"""
	dataset = models.CharField(max_length=255)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	project = models.ForeignKey(
		Project,
		on_delete=models.CASCADE,
	)