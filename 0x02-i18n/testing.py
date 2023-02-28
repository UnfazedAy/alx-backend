import datetime

now = datetime.datetime.now()
formatted_date = now.strftime("%b %d, %Y, %I:%M:%S %p")

print(formatted_date)
