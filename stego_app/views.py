# views.py (with login/signup logic)

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import steg_utils
import os
import uuid
import json

UPLOAD_DIR = "stego_app/static/uploaded_files"
SECRET_DB = os.path.join(UPLOAD_DIR, "secret_codes.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper to read/write JSON secrets
def load_secrets():
    if os.path.exists(SECRET_DB):
        with open(SECRET_DB, 'r') as f:
            return json.load(f)
    return {}

def save_secret(file_name, secret_code):
    secrets = load_secrets()
    secrets[file_name] = secret_code
    with open(SECRET_DB, 'w') as f:
        json.dump(secrets, f)

# ----------------- Auth -----------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'signup.html')

# ----------------- Dashboard -----------------
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ----------------- Image Steg -----------------
@login_required
def image_steg(request):
    if request.method == 'POST':
        action = request.POST['action']
        uploaded_file = request.FILES.get('image_file')
        secret_code = request.POST.get('secret_code')
        msg = request.POST.get('message')

        if uploaded_file:
            fs = FileSystemStorage(location=UPLOAD_DIR)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(UPLOAD_DIR, filename)
            print("Secret DB path:", SECRET_DB)

            if action == 'encrypt':
                unique_name = f"enc_{uuid.uuid4().hex[:6]}.png"
                out_path = os.path.join(UPLOAD_DIR, unique_name)
                steg_utils.encode_image(file_path, msg, out_path)
                save_secret(unique_name, secret_code)
                messages.success(request, f"Image encrypted as: {unique_name}")
                #debug
                print("Saving secret:", unique_name, secret_code)  # during encryption


            elif action == 'decrypt':
                secrets = load_secrets()
                if uploaded_file.name in secrets and secrets[uploaded_file.name] == secret_code:
                    msg = steg_utils.decode_image(file_path)
                    messages.success(request, f"Decrypted Message: {msg}")
                else:
                    messages.error(request, "Incorrect secret code or file!")
                #debug
                print("Looking for:", filename, "in", secrets)  # during decryption

    return render(request, 'image_steg.html')

# ----------------- Audio Steg -----------------
@login_required
def audio_steg(request):
    if request.method == 'POST':
        action = request.POST['action']
        uploaded_file = request.FILES.get('audio_file')
        secret_code = request.POST.get('secret_code')
        msg = request.POST.get('message')

        if uploaded_file:
            fs = FileSystemStorage(location=UPLOAD_DIR)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(UPLOAD_DIR, filename)

            if action == 'encrypt':
                unique_name = f"enc_{uuid.uuid4().hex[:6]}.wav"
                out_path = os.path.join(UPLOAD_DIR, unique_name)
                steg_utils.encode_audio(file_path, msg, out_path)
                save_secret(unique_name, secret_code)
                messages.success(request, f"Audio encrypted as: {unique_name}")

            elif action == 'decrypt':
                secrets = load_secrets()
                if uploaded_file.name in secrets and secrets[uploaded_file.name] == secret_code:
                    msg = steg_utils.decode_audio(file_path)
                    messages.success(request, f"Decrypted Message: {msg}")
                else:
                    messages.error(request, "Incorrect secret code or file!")

    return render(request, 'audio_steg.html')

# ----------------- Video Steg -----------------
@login_required
def video_steg(request):
    if request.method == 'POST':
        action = request.POST['action']
        uploaded_file = request.FILES.get('video_file')
        secret_code = request.POST.get('secret_code')
        msg = request.POST.get('message')

        if uploaded_file:
            fs = FileSystemStorage(location=UPLOAD_DIR)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(UPLOAD_DIR, filename)

            if action == 'encrypt':
                unique_name = f"enc_{uuid.uuid4().hex[:6]}.avi"
                out_path = os.path.join(UPLOAD_DIR, unique_name)
                steg_utils.encode_video(file_path, msg, out_path)
                save_secret(unique_name, secret_code)
                messages.success(request, f"Video encrypted as: {unique_name}")

            elif action == 'decrypt':
                secrets = load_secrets()
                if uploaded_file.name in secrets and secrets[uploaded_file.name] == secret_code:
                    msg = steg_utils.decode_video(file_path)
                    messages.success(request, f"Decrypted Message: {msg}")
                else:
                    messages.error(request, "Incorrect secret code or file!")

    return render(request, 'video_steg.html')
