from django.db import models
from authentication import views


# Create your models here.
class Expense(models.Model):
	name = models.CharField(max_length = 50)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	owner = models.CharField(max_length = 15)


class UserGroup(models.Model):
	name = models.CharField(max_length = 50)
	group_owner = models.ForeignKey(views.User, on_delete=models.CASCADE, related_name="group_owner")
	members = models.ManyToManyField(views.User, blank = True, related_name="members")
	expenses = models.ManyToManyField(Expense, through='ExpenseMembership', blank = True, related_name="expenses")

	def add_member_togroup(self, username):
		if not username in self.members.all():
			self.members.add(username)
			return True
		else:
			return False

	def remove_member_fromgroup(self, username):
		if username in self.members.all():
			self.members.remove(username)
			return True
		else:
			return False

	def get_group_owner(self):
		return self.group_owner.get_username()

	def get_group_name(self):
		return self.name
		
		
class GroupList(models.Model):
	list_owner = models.OneToOneField(views.User, on_delete=models.CASCADE, related_name="list_owner")
	groups = models.ManyToManyField(UserGroup, through='Membership', blank = True, related_name="groups")
		
	def add_group(self, username):
		if not username in self.groups.all():
			self.groups.add(username)
			return True
		else:
			return False

	def remove_group(self, username):
		if username in self.groups.all():
			self.groups.remove(username)
			return True
		else:
			return False

	def __str__(self):
		return self.list_owner.get_username()


class Membership(models.Model):
    grouplist = models.ForeignKey(GroupList, on_delete=models.CASCADE)
    usergroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE)


class ExpenseMembership(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    usergroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE)