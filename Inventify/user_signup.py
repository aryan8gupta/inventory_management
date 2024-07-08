from Inventify.settings import DB
from views import generate_password


def user_signup():
    first_name = 'Aryan'
    last_name = 'Gupta'
    email = 'aryan@gmail.com'
    password = generate_password('ayan123')
    # password = generate_password('Paheli79871')
    # password = generate_password('aman')

    user_dict = {
	  "login_type": "username-pass",
	  "first_name": first_name,
	  "last_name": last_name,
	  "email": email,
	  "password": password,
	  "user_type": 'Shop Owners',
	}
    DB.users.insert_one(user_dict)
user_signup()