import json

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignInForm, SignUpForm, PasswordChangeForm
from .models import User, Qualification, Language, Task


@login_required
def index(request):
    if request.method == 'POST':
        return redirect('homepage')
    subs = User.objects.filter(chief=request.user)
    data = {
        'self': Task.objects.filter(performer=request.user),
        'subs': Task.objects.filter(performer__in=subs)
    }
    if request.user.is_admin:
        data['other'] = Task.objects.exclude(performer=request.user).exclude(performer__in=subs)
    return render(request, 'index.html', context=data)


def create_user(request):
    if not request.user.is_admin:
        return redirect('users')
    if request.method == 'POST':
        data = {
            'quals': list(map(int, request.POST.get('qualifications').split(','))),
            'langs': list(map(int, request.POST.get('languages').split(',')))
        }
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.qualifications.set(data['quals'])
            user.languages.set(data['langs'])
            return redirect('users')
    else:
        form = SignUpForm()
    data = {
        'form': form,
        'chiefs': User.objects.only('id', 'name'),
        'qualifications': [
            {'id': qual.id,
            'name': f'{qual.code} - {qual.name}'}
            for qual in Qualification.objects.all()
        ],
        'languages': Language.objects.all()
    }
    return render(request, 'create_user.html', data)


def edit_user(request):
    if not request.user.is_admin:
        return redirect('users')
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(id=data.get('id'))
        if not user:
            return redirect('users')
        user.name = data.get('name')
        user.chief = data.get('chief')
        user.save()
        user.qualifications.set(data.get('qualifications'))
        user.languages.set(data.get('languages'))
        return redirect(request.path)

    user_id = int(request.path[11:])
    user_edited = User.objects.get(id=user_id)
    data = {
        'id': user_edited.id,
        'current_chief': user_edited.chief,
        'name': user_edited.name,
        'chiefs': User.objects.exclude(id=user_id),
        'user_qualifications': list(map(str, user_edited.qualifications.values_list('id', flat=True))),
        'user_languages': list(map(str,user_edited.languages.values_list('id', flat=True))),
        'qualifications': Qualification.objects.all(),
        'languages': Language.objects.all(),
    }
    return render(request, 'edit_user.html', data)


def delete_user(request):
    if not request.user.is_admin or request.method != 'DELETE':
        return redirect('users')
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    user_id = data.get('user_id')
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users')


def sign_in(request):
    form = SignInForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                print('something went wrong')
    return render(request, 'login.html', {'form': form})


@login_required
def users(request):
    if request.method == 'POST':
        chief_id = request.POST.get('chief')
        password = request.POST.get('password')
        chief = User.objects.get(id=chief_id)
        user = User.objects.create_user(request.POST.get('name'),
                                        request.POST.get('email'),
                                        password,
                                        chief=chief)
        return redirect('users')
    usrs = User.objects.select_related('chief').only('id', 'name', 'chief__name')
    data = {
        'users': [
            {
                'id': user.id,
                'name': user.name,
                'chief': user.chief.name if user.chief else '-'
            }
            for user in usrs
        ],
    }
    return render(request, 'users.html', context=data)


@login_required
def profile(request):
    user_id = request.path[9:]
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if not request.user.check_password(data.get('old_password')):
            messages.error(request, 'Wrong old password')
        elif data.get('new_password1') != data.get('new_password2'):
            messages.error(request, 'Passwords don\'t match')
        else:
            request.user.set_password(data.get('new_password1'))
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect(f'profile/{request.user.id}')
    if not user_id.isdigit():
        return HttpResponse('Wrong user id')
    user = get_object_or_404(User.objects.select_related('chief').prefetch_related('qualifications', 'languages', 'subordinates'),
                             id=user_id)
    if user:
        data = {
            'user': user,
            'form': PasswordChangeForm,
        }
        return render(request, 'profile.html', data)
    else:
        return HttpResponse('Wrong user id')


def log_out(request):
    logout(request)
    return redirect('homepage')


def admin(request):
    if not request.user.is_admin:
        return redirect('homepage')
    if request.method == 'POST':
        data = request.POST
        code = data.get('code')
        name = data.get('name')
        if code:
            Qualification.objects.create(code=code, name=name)
        else:
            Language.objects.create(name=name)
        return redirect('admin')
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        code = data.get('code')
        name = data.get('name')
        if code:
            qual = Qualification.objects.get(id=id)
            qual.code = code
            qual.name = name
            qual.save()
        else:
            lang = Language.objects.get(id=id)
            lang.name = name
            lang.save()
    elif request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        obj_id = data.get('id')
        obj_type = data.get('type')
        if obj_type == 'q':
            Qualification.objects.get(id=obj_id).delete()
        elif obj_type == 'l':
            Language.objects.get(id=obj_id).delete()
    data = {
        'qualifications': Qualification.objects.all(),
        'languages': Language.objects.all()
    }
    return render(request, 'admin.html', context=data)
