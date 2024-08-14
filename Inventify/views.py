import json
from bson import ObjectId
from django.contrib.auth import authenticate, login, logout;
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

import bcrypt 
import jwt
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from Inventify.settings import DB, PUBLIC_KEY

product_list1 = []

def generate_password(a):
    bytes = a.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    return hash



def generate_token(user_dict):
    token = jwt.encode({"exp": datetime.now() + timedelta(days=7) , **user_dict}, PUBLIC_KEY, algorithm="HS256")
    return token


def verify_token(token):
    
    decoded_token = {}  
    if token:
        try:
            decoded_token = jwt.decode(token, PUBLIC_KEY, algorithms="HS256", options={"verify_exp": False})
        except Exception as e:
            return False, {}
    else:
        return False, {}
    
    return True, decoded_token





def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'home.html')
def analytics(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'analytics.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



def dashboard(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    if user_type == 'Employee':
        return render(request, 'barcode.html', {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})

    return render(request, 'dashboard.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})




@csrf_exempt
def products_add(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    

    if request.method == 'POST':
        try:
            products_name = request.POST.get("product_name")
            products_doc = DB.products.find_one({"product_name": products_name})
            if not products_doc:

                products_name = request.POST.get("product_name")
                products_quantity = request.POST.get("quantity")
                products_cost_price = request.POST.get("cost_price")
                products_selling_price = request.POST.get("selling_price")
                products_expiry_date = request.POST.get("expiry_date")
                products_barcode = request.POST.get("barcode")
                products_image = request.POST.get("img")

                products_profit = (int(products_selling_price) - int(products_cost_price)) * int(products_quantity)

                a = request.GET.get('q', '')

                products_dict = {
	                "product_name": products_name,
	                "bought_quantity": products_quantity,
	                "left_quantity": products_quantity,
	                "cost_price": products_cost_price,
	                "selling_price": products_selling_price,
	                "expiry_date": products_expiry_date,
	                "profit": products_profit,
	                "barcode": products_barcode,
	                "image": products_image,
                    "user_id": ObjectId(a),

	            }
                DB.products.insert_one(products_dict)

                products_details1 = list(DB.products.find({'user_id': ObjectId(a)}))

                return render(request, 'products.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name,  'products_details': products_details1})
                
            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'products_add.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})
            
    else:
        return render(request, 'products_add.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



def products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
     
    if user_type == "Admin":
    
        b = request.GET.get('q', '')
        users_doc = DB.users.find_one({"email": b})
        product_user_id = users_doc['_id']
        
        products_details1 = list(DB.products.find({'user_id': product_user_id}))

        return render(request, 'products.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_details': products_details1, "users_id": product_user_id})
    
    elif user_type == "Shop Owners":
        user_email = data.get('email')
        users_doc = DB.users.find_one({"email": user_email})
        product_user_id = users_doc['_id']

        products_details = list(DB.products.find({'user_id': product_user_id}))

        return render(request, 'products.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_details': products_details, "users_id": product_user_id})




def products_sold(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')

    users_id_doc = DB.users.find_one({'email': user_email})

    products_doc = list(DB.products_sold.find({'user_id': users_id_doc['_id']}))
    
    return render(request, 'products_sold.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_doc': products_doc})



def contact_us(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    return render(request, 'contact_us.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



@csrf_exempt
def barcode(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    

    num = '0'
    sum1 = 0
    product_name_list = [] 
    global product_list1

    if request.method == 'POST':
        try:
            if request.POST.get("form_type") == 'rm_data1':
                barcodeInput = request.POST.get("barcodeInput")
                number = '1'

                barcode_doc = DB.products.find_one({"barcode": barcodeInput})

                new_quantity = int(barcode_doc['left_quantity']) - 1

                DB.products.find_one_and_update({'barcode': barcodeInput}, {'$set': {'left_quantity': new_quantity}})

                if barcode_doc:
            
                    product_list1.append(barcode_doc)
                    for data in product_list1:

                        sum1 = sum1 + int(data['selling_price'])

                    return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_data': product_list1, 'barcode_doc': barcode_doc, 'num': number, 'totalMoney' : sum1})
                else:
                    raise Exception


            elif request.POST.get("form_type") == 'delete_data':
                deleted_product_barcode = request.POST.get("deleted_product")
                number = '1'

                barcode_doc = DB.products.find_one({"barcode": deleted_product_barcode})

                for i in range(len(product_list1)):
                    if product_list1[i]['barcode'] == deleted_product_barcode:
                        del product_list1[i]
                        break

                for data in product_list1:

                        sum1 = sum1 + int(data['selling_price'])

                return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_data': product_list1, 'barcode_doc': barcode_doc, 'num': number, 'totalMoney' : sum1})


            elif request.POST.get("form_type") == 'rm_data2':
                number1 = '2'

                for data in product_list1:

                    product_name_list.append(data['product_name']) 

                    sum1 = sum1 + int(data['selling_price'])

                    products_dict = {
	                    "product_name": data['product_name'],
	                    "cost_price": data['cost_price'],
	                    "selling_price": data['selling_price'],
	                    "expiry_date": data['expiry_date'],
	                    "profit": data['profit'],
	                    "barcode": data['barcode'],
	                    "image": data['image'],
	                    "date_time": datetime.now(),
                        "user_id": data['user_id'],
	                }
                    DB.products_sold.insert_one(products_dict)

                a = len(product_list1)

                return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_product_name': product_name_list, 'num': number1, 'scanned_quantity': a, 'scanned_quantity_totalPrice': sum1})
            
            else:
                raise Exception
            
        except:
            messages.warning(request, "Outside Product")
            num = '0'
            return render(request, 'barcode.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'num': num})
            
    else:
        product_list1 = []
        return render(request, 'barcode.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'num': num})



    

def employee(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



@csrf_exempt
def employee_signup(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_email = data.get('email')
    user_name = data.get('first_name')
    
    
    if request.method == 'POST':
        try:
            employee_email = request.POST.get("email")
            employee_doc = DB.users.find_one({"email": employee_email})

            if not employee_doc:

                employee_firstname = request.POST.get("first_name")
                employee_lastname = request.POST.get("last_name")
                employee_mobile = request.POST.get("mobile")
                employee_age = request.POST.get("age")
                employee_address = request.POST.get("address")
                employee_salary = request.POST.get("salary")

                employee_password = request.POST.get("password")


                user_doc = DB.users.find_one({"email": user_email})
                user_id = user_doc['_id']

                employee_dict = {
	                "first_name": employee_firstname,
	                "last_name": employee_lastname,
	                "mobile": employee_mobile,
	                "age": employee_age,
	                "address": employee_address,
	                "salary": employee_salary,
	                "email": employee_email,
	                "password": generate_password(employee_password),
	                "user_type": 'Employee',
                    "user_id": user_id,
	            }
                user_dict = {
                    "login_type": "username-pass",
	                "first_name": employee_firstname,
	                "last_name": employee_lastname,
	                "email": employee_email,
	                "password": generate_password(employee_password),
	                "user_type": 'Employee',
	            }

                DB.employees.insert_one(employee_dict)
                DB.users.insert_one(user_dict)
                return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'employee_signup.html')
            
    else:
        return render(request, 'employee_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})






def shops(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    shops_details = list(DB.shops.find({"user_type": "Shops"}))
    
    return render(request, 'shops.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shops_details': shops_details})




def shops_add(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    if request.method == 'POST':
        try:
            shop_contact = request.POST.get("shop_contact")
            shops_doc = DB.shops.find_one({"shop_contact_number": shop_contact})

            if not shops_doc:

                shop_name = request.POST.get("shop_name")
                shop_address = request.POST.get("shop_address")
                shop_contact = request.POST.get("shop_contact")
       
                shops_dict = {
	                "shop_name": shop_name,
	                "shop_address": shop_address,
	                "shop_contact_number": shop_contact,
	                "user_type": 'Shops',
	            }

                DB.shops.insert_one(shops_dict)

                return redirect("/shops/")

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'shops_add.html')
            
    else:
        return render(request, 'shops_add.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})




def users_details(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    shop_owners_details = list(DB.users.find({'user_type': 'Shop Owners'}))

    
    return render(request, 'users_details.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shop_owners_details': shop_owners_details})


@csrf_exempt
def users_signup(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    if request.method == 'POST':
        try:
            users_email = request.POST.get("email")
            users_doc = DB.users.find_one({"email": users_email})

            if not users_doc:

                users_firstname = request.POST.get("first_name")
                users_lastname = request.POST.get("last_name")
                users_mobile = request.POST.get("mobile")
                users_age = request.POST.get("age")
                users_shop_name = request.POST.get("shop_name")
                users_shop_address = request.POST.get("shop_address")

                users_password = request.POST.get("password")


                users_dict = {
	                "first_name": users_firstname,
	                "last_name": users_lastname,
	                "mobile": users_mobile,
	                "age": users_age,
	                "shop_name": users_shop_name,
	                "shop_address": users_shop_address,
	                "email": users_email,
	                "password": generate_password(users_password),
	                "user_type": 'Shop Owners',
	            }

                DB.users.insert_one(users_dict)

                shop_owners_details = list(DB.users.find({'user_type': 'Shop Owners'}))

                return render(request, 'users_details.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name,  'shop_owners_details': shop_owners_details})

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'users_signup.html')
            
    else:
        return render(request, 'users_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



def delete(request):
    try:
        a = request.GET.get('q', '')
        print(a)
        DB.shops.delete_one({'shop_contact_number': a})
        return redirect("/shops/")
    except:
        return redirect("/shops/")
    
    

@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get("email")
            login_password = request.POST.get("password")

            user_doc = DB.users.find_one({"email": email})
            if user_doc:
                userBytes = login_password.encode('utf-8')
                doc_pass = user_doc['password']
                result = bcrypt.checkpw(userBytes, doc_pass)
                if result:
                    email = user_doc.get("email")
                    user_type = user_doc.get("user_type")
                    first_name = user_doc.get("first_name")
                    user_dict = {
                        "email": email,
                        "user_type": user_type,
                        "first_name": first_name,
                    } 
                    jwt_token = generate_token(user_dict)
                    response = HttpResponseRedirect('/dashboard')
                    response.set_cookie("t", jwt_token)
                    user_doc = DB.users.find_one_and_update({"email": email}, {"$set":{"token":jwt_token}})
                    return response
                else:
                    raise Exception
            else:
                raise Exception

        return render(request, 'login.html', {})
    except:
        messages.warning(request, "Invalid ID or Password")
        return render(request, 'login.html')



def logout(request):
	response = HttpResponseRedirect('/')
	response.delete_cookie("t")
	return response
