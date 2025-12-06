from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyotp, qrcode, io, base64, json, requests, smtplib
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def jerald_cipher_atbash(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(65 + (25 - (ord(char) - 65)))
        else:
            result += char
    return result


def home(request):
    """Landing page"""
    return render(request, 'api/home.html')


def account_view(request):
    """Handles both login and signup for local accounts."""
    if request.method == 'POST':
     
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('projects')
            else:
                messages.error(request, "Invalid username or password.")

    
        elif 'signup' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('account')

    return render(request, 'login.html')


def logout_view(request):
    """Logs out both local and social users."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('account')


@login_required(login_url='account')
def projects(request):
    """Protected page — only accessible when logged in."""
    return render(request, 'projects.html')

def project1(request):
    return render(request, 'api/project1.html')

def project2(request):
    user = request.user if request.user.is_authenticated else None
    secret = pyotp.random_base32()
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=f"{user.username if user else 'guest'}@elitedev.com",
        issuer_name="EliteDev 2FA"
    )
    request.session['secret'] = secret
    return render(request, 'api/project2.html', {'otp_uri': otp_uri})


def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        secret = request.session.get('secret')
        totp = pyotp.TOTP(secret)
        verified = totp.verify(otp_input)
        return render(request, 'api/project2.html', {
            'verified': verified,
            'otp_uri': pyotp.totp.TOTP(secret).provisioning_uri(
                name="user@elitedev.com", issuer_name="EliteDev 2FA"
            )
        })
    return HttpResponse("Invalid request")

def project3(request):
    response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()
    joke = response.get("joke", "Why don’t scientists trust atoms? Because they make up everything!")
    encrypted = jerald_cipher_atbash(joke)
    qr = qrcode.make(encrypted)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return render(request, 'api/project3.html', {
        'joke': joke,
        'encrypted': encrypted,
        'qr_code': qr_base64
    })

def project4(request):
    return render(request, 'api/project4.html')


def api_security_demo(request):
    data = {
        "status": "success",
        "project": "Application Security Programming",
        "original_message": "Hello Secure World!",
        "encrypted_message": "Khoor#Vhfxuh#Zruog$",
        "note": "This is a simple demo of encryption logic (Caesar cipher)."
    }
    return JsonResponse(data)

students = []

def project5(request):
    return render(request, 'api/project5.html')


@csrf_exempt
def project5_api(request):
    global students
    if request.method == 'GET':
        return JsonResponse(students, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get("full_name")
            student_id = data.get("student_id")
            contact = data.get("contact_number")
            if not (name and student_id and contact):
                return JsonResponse({"error": "All fields are required."}, status=400)
            student = {
                "full_name": name,
                "student_id": student_id,
                "contact_number": contact
            }
            students.append(student)
            return JsonResponse(student, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid method."}, status=405)

recipients = []

def project6(request):
    return render(request, 'api/project6.html')


@csrf_exempt
def email_api(request):
    global recipients
    if request.method == 'GET':
        return JsonResponse({"recipients": recipients}, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get("action")

            if action == "add_recipient":
                email = data.get("email")
                if email:
                    recipients.append(email)
                    return JsonResponse({"message": "Recipient added", "recipients": recipients})
                return JsonResponse({"error": "Email required"}, status=400)

            elif action == "send_email":
                fact_api = "https://uselessfacts.jsph.pl/api/v2/facts/random"
                fact = requests.get(fact_api).json().get("text", "Here’s a fun fact!")

                sender_email = "cuerporhyverjohn@gmail.com"
                password = "bujk sxht olem liyu"

                for recipient in recipients:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = recipient
                    msg["Subject"] = "Daily Fun Fact"
                    msg.attach(MIMEText(fact, "plain"))

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.send_message(msg)

                return JsonResponse({"message": "Emails sent successfully!"})

            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
