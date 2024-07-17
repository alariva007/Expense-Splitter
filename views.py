from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import GroupList, UserGroup, Membership
from friends.models import FriendList

# Create your views here.
def groups_list(request):
	
	# Determining the current_user (logged in account)
	current_user = request.user

	# Determining the current_user's group list object
	current_user_grouplist = None
	grouplists = GroupList.objects.all()
	for grouplist in grouplists:
		if grouplist.list_owner.get_username() == current_user.get_username():
			current_user_grouplist = grouplist

	# Generating context data (groups_toload) to be sent to frontend
	if current_user_grouplist == None:
		context = {"groups_toload": None}
	else:
		context = {"groups_toload": current_user_grouplist.groups.all()}	

	# Resolving form submission (create group button clicks)
	if request.method == "POST":
		group_name = request.POST.get('group_name')

		# Handling Error: Checking for group name uniqueness
		if UserGroup.objects.filter(name = group_name):
			messages.error(request, "That Group Name is Already Taken!")
			return redirect('groups_list')

		# Creating the group and saving it to the database
		new_group = UserGroup(name = group_name, group_owner = current_user)
		new_group.save()
		new_group.members.add(current_user)

		# Creating Query Relationships for the Group and its owner
		membership = Membership(usergroup = new_group, grouplist = current_user_grouplist)
		membership.save()

		messages.success(request, "Group Successfully Created and Added to your Group's List'!")
		
	# Generating context data (groups_toload) to be sent to frontend
	context = {"groups_toload": current_user_grouplist.groups.all()}

	return render(request, "groups/groups_list.html", context)


def group_page(request): 
	context = {}

	# Determining the current_user (logged in account)
	current_user = request.user
	current_user_username = current_user.get_username()

	# Resolving form submissions (several cases)
	if request.method == "POST":
		name_group_toload = request.POST.get('group_name')
		group_toupdate = None

		# Handling Error Case(s): group does not exist / user not member of group
		if UserGroup.objects.filter(name = name_group_toload): # group does exist	
			groups = UserGroup.objects.all()
			isUserInGroup = False
			for group in groups:
				if group.get_group_name() == name_group_toload:
					isUserInGroup = True
					group_toupdate = group
					context.update({'group_name': group.get_group_name()})
					context.update({'members': group.members.all()})				
					# Determining status of visiting group member for frontend
					if group.get_group_owner() == current_user_username:
						context.update({'member_identity': "owner"})
					else: 
						context.update({'member_identity': "member"})						
			if not isUserInGroup: # user is not member of group
				messages.error(request, "You are NOT a Member of that Group! You cannot View it's Page.")
				return redirect('groups_list')						
		else: # group does not exist
			messages.error(request, "Group does NOT Exist! Try Creating a New Group with that Name.")
			return redirect('groups_list')

		# Handling add/remove group member requests
		if "add_member" or "remove_member" in request.POST:
			subject_username = request.POST.get('username')
			subject_user = None

			# Locating subject_user object passed by current_user (if it exists)
			users = User.objects.all()
			for user in users:
				if user.get_username() == subject_username:
					subject_user = user

			# Handling Error Case: subject_user does not exist
			if subject_user is None:				
				messages.error(request, "No User Registered with that Username! User does not Exist.")
				return render(request, "groups/group_page.html", context)

			# Handling Error Case: current_user matches subject_user
			if current_user.get_username() == subject_user.get_username():
				messages.error(request, "Cannot Add/Remove yourself to/from your Own Group!")
				return render(request, "groups/group_page.html", context)

			# Determining the subject_user's group list object
			subject_user_grouplist = None
			grouplists = GroupList.objects.all()
			for grouplist in grouplists:
				if grouplist.list_owner.get_username() == subject_username:
					subject_user_grouplist = grouplist

			# Executing add_member requests
			if "add_member" in request.POST:
				
				# Determining the current_user's friend's list object
				current_user_friendlist = None
				friendlists = FriendList.objects.all()
				for friendlist in friendlists:
					if friendlist.user.get_username() == current_user.get_username():
							current_user_friendlist = friendlist

				# Handling Error Case: subject_user not in current_user's friend list
				isAFriend = False
				for friend in current_user_friendlist.friends.all():
					if friend.get_username() == subject_username:
						isAFriend = True
				if not isAFriend:
					messages.error(request, "Cannot Add a User NOT in your Friends List!")
					return render(request, "groups/group_page.html", context)

				# Handling Error Case: subject_user already in the group
				isInGroup = False
				for member in group_toupdate.members.all():
					if member.get_username() == subject_username:
						isInGroup = True
				if isInGroup:
					messages.error(request, "Cannot Add a User already in the Group!")
					return render(request, "groups/group_page.html", context)

				# Adding member to the group
				group_toupdate.members.add(subject_user)
				group_toupdate.save()
				membership = Membership(usergroup = group_toupdate, grouplist = subject_user_grouplist)
				membership.save()
				print(group_toupdate.members.all())

			# Executing remove_member requests
			if "remove_member" in request.POST:
				
				# Handling Error Case: subject_user not in the group
				isInGroup = False
				for member in group_toupdate.members.all():
					if member.get_username() == subject_username:
						isInGroup = True
				if not isInGroup:
					messages.error(request, "Cannot Remove a User NOT already in the Group!")
					return render(request, "groups/group_page.html", context)

				# Removing member from the group
				group_toupdate.members.remove(subject_user)
				group_toupdate.save()

		# Handling add/remove expense requests (TODO)


	return render(request, "groups/group_page.html", context)