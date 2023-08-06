def time(hours):
	if hours == 24:
		import datetime
		today = datetime.datetime.now()
		date_time = today.strftime("%H:%M")
		print(date_time)
	elif hours == 12:
		import datetime
		today = datetime.datetime.now()
		date_time = today.strftime("%I:%M")
		print(date_time)