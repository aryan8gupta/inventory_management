from bson import ObjectId
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponseRedirect

import bcrypt 
import jwt
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from Inventify.settings import DB, PUBLIC_KEY
# from Inventify.deployment import DB, PUBLIC_KEY
from .models import YourModel

import requests
import base64
import time
from django.http import JsonResponse


# QR-Code Generating / Template----------------------------------------------------------->
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

LABEL_WIDTH_MM = 50
LABEL_HEIGHT_MM = 38
PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
TOP_MARGIN_MM = 10
LEFT_MARGIN_MM = 10
GAP_MM = 0

def mm_to_pt(mm_val):
    return mm_val * mm

def generate_qr_code(data, filename="temp_qr.png"):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename

def create_vertical_qr_pdf(data_list, output_file="vertical_qr_labels.pdf"):
    c = canvas.Canvas(output_file, pagesize=(mm_to_pt(PAGE_WIDTH_MM), mm_to_pt(PAGE_HEIGHT_MM)))

    label_width = mm_to_pt(LABEL_WIDTH_MM)
    label_height = mm_to_pt(LABEL_HEIGHT_MM)
    x_qr = mm_to_pt(LEFT_MARGIN_MM + 30)  # QR shifted right to make space for text
    x_text = mm_to_pt(LEFT_MARGIN_MM)     # Text on left
    y = mm_to_pt(PAGE_HEIGHT_MM - TOP_MARGIN_MM - LABEL_HEIGHT_MM)

    for i, item in enumerate(data_list):
        product_name = item.get("name", f"Product {i+1}")
        qr_data = item.get("url", "")

        qr_img = generate_qr_code(qr_data)
        c.drawImage(qr_img, x_qr, y, width=label_width, height=label_height)

        # Draw product name text
        c.setFont("Helvetica", 10)
        c.drawString(x_text, y + label_height / 2, product_name)

        y -= (label_height + mm_to_pt(GAP_MM))

        if y < mm_to_pt(10):
            c.showPage()
            y = mm_to_pt(PAGE_HEIGHT_MM - TOP_MARGIN_MM - LABEL_HEIGHT_MM)

    c.save()
    print(f"PDF saved: {output_file}")

# Example with product names
data_list = [
    {"name": "Black T-Shirt", "url": "https://example.com/item/1"},
    {"name": "Denim Jeans", "url": "https://example.com/item/2"},
    {"name": "Green Kurti", "url": "https://example.com/item/3"},
    {"name": "Formal Shirt", "url": "https://example.com/item/4"},
    # Add more...
]

# Uncomment this to create pdf.
# create_vertical_qr_pdf(data_list)
# --------------------------------------------------------------------->


PINCEL_API_URL = "https://pincel.app/api/clothes-swap"
PINCEL_API_KEY = "d7982ad0-58e5-4899-b0db-e063a8e70448"

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


def exchange(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'exchange.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


def sales(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'sales.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



def scan_qr(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'scan.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        garment_image = request.FILES.get('garment_image')
        cloth_image = request.FILES.get('cloth_image')

        if not garment_image or not cloth_image:
            return JsonResponse({"error": "Both images are required."})

        # Send images to Pincel API
        # files = {
        #     'garment_image': (garment_image.name, garment_image.read(), garment_image.content_type),
        #     'cloth_image': (cloth_image.name, cloth_image.read(), cloth_image.content_type),
        #     "category": "upper_body",
        #     "action": "startPrediction"
        # }

        def encode_image(image):
            return base64.b64encode(image.read()).decode('utf-8')

        model_image_base64 = encode_image(garment_image)
        garment_image_base64 = encode_image(cloth_image)

        headers = {
            'X-API-Key': PINCEL_API_KEY,
            'Content-Type': 'application/json',
        }

        payload1 = {
            "model_image": f"data:image/jpeg;base64,{model_image_base64}",
            "garment_image": f"data:image/jpeg;base64,{garment_image_base64}",
            "category": "upper_body", 
            "action": "startPrediction"
        }

        try:
            response1 = requests.post(PINCEL_API_URL, json=payload1, headers=headers)
            data1 = response1.json()
            print(data1)

            payload2 = {
                "predictionId": data1['prediction'],
                "action": "getPrediction"
            }
            while True:
                response2 = requests.post(PINCEL_API_URL, json=payload2, headers=headers)
                data2 = response2.json()
                print(data2)

                if response2.status_code == 200:
                    status = data2.get('status')

                    if status == 'succeeded':
                        print("✅ Prediction completed! Image URL:", data2.get('output'))
                        return JsonResponse(data2)
                    elif status == 'failed':
                        print("❗ Prediction failed:", data2.get('error', 'Unknown error'))
                        return None
                    else:
                        print("⏳ Processing... Checking again in 5 seconds.")
                else:
                    print("❗ Error:", data2.get('error', 'Unknown error'))
                    return None

                time.sleep(5)  # Wait 5 seconds before checking again

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def add_products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    plan = "premium"

    # if request.method == 'POST':
    #     try:
    #         if request.POST.get("form_type") == 'add1':
    #             original_image = request.POST.get("original_image")
    #             print(original_image)
    #     except:
    #         return render(request, 'add_products.html',  { 'dashboard': 
	# 												   dashboard, 'user_type': user_type, 'first_name': user_name})

            

    return render(request, 'add_products.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'plan': plan})


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
                barcodeInput = request.POST.get("barcodeInput1")
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
                barcode_doc['left_quantity'] = int(barcode_doc['left_quantity']) + 1

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
    user_email = data.get('email')

    users_id_doc = DB.users.find_one({'email': user_email})

    employees_doc = list(DB.employees.find({'user_id': users_id_doc['_id']}))

    if request.method == 'POST':
        print("1")
        employee_email = request.POST.get("email")
        employee_firstname = request.POST.get("first_name")
        employee_lastname = request.POST.get("last_name")
        employee_mobile = request.POST.get("mobile")
        employee_age = request.POST.get("age")
        employee_address = request.POST.get("address")
        employee_salary = request.POST.get("salary")

        DB.employees.find_one_and_update(
            {"email": employee_email}, {'$set': 
                {
                'first_name': employee_firstname,
                'last_name': employee_lastname,
                'mobile': employee_mobile,
                'age': employee_age,
                'address': employee_address,
                'salary': employee_salary,
                }
            }
        )
        print("2")
        employees_doc1 = list(DB.employees.find({'user_id': users_id_doc['_id']}))
        print("3")

        return render(request, 'employee.html', { 'dashboard': 
												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc1, 'show': '0'}) 
            
    else:
        return render(request, 'employee.html', { 'dashboard': 
													dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc, 'show': '0'})



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
                employees_doc = list(DB.employees.find({'user_id': user_id}))
                return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc, 'show': '0'})

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'employee_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})
            
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
        if '@' in a:
            DB.employees.delete_one({'email': a})
            DB.users.delete_one({'email': a})
            return redirect("/employee/")
        else:
            DB.shops.delete_one({'shop_contact_number': a})
            return redirect("/shops/")
    except:
        return redirect("/shops/")
    


def detail(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    try:
        a = request.GET.get('q', '')
        employee_detail = DB.employees.find_one({'email': a})
        return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'employee_detail': employee_detail, 'show': '1'})
    except:
        return redirect("/employee/")
    

    
def update(request):
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

    if request.method == 'POST':
        employee_email = request.POST.get("email")
        employee_firstname = request.POST.get("first_name")
        employee_lastname = request.POST.get("last_name")
        employee_mobile = request.POST.get("mobile")
        employee_age = request.POST.get("age")
        employee_address = request.POST.get("address")
        employee_salary = request.POST.get("salary")

        DB.employees.find_one_and_update(
            {"email": employee_email}, {'$set': 
                {
                'first_name': employee_firstname,
                'last_name': employee_lastname,
                'mobile': employee_mobile,
                'age': employee_age,
                'address': employee_address,
                'salary': employee_salary,
                }
            }
        )
        employees_doc1 = list(DB.employees.find({'user_id': users_id_doc['_id']}))

        return render(request, 'employee.html', { 'dashboard': 
												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc1, 'show': '0'}) 
    else:
        try:
            a = request.GET.get('q', '')
            employee_detail = DB.employees.find_one({'email': a})
            return render(request, 'employee.html', { 'dashboard': 
	    												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employee_detail': employee_detail, 'show': '2'})
        except:
            return redirect("/employee/")
    
    
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get("email")
            login_password = request.POST.get("password")

            user_doc = DB.users.find_one({"email": email})
            # user_doc = DB.users.find_one()
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
        logger.error("Failed System of logging in .")
        return render(request, 'login.html')



def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie("t")
    return response
