import json
import os

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from ctm import settings
from .forms import SignInForm, SignUpForm, PasswordChangeForm, TaskCreationForm
from .models import User, Qualification, Language, Task, ArchiveTask


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.is_admin,
        login_url='/',
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required
def index(request):
    if request.method == 'POST':
        data = request.POST
        task_id = data.get('task_id')
        task = Task.objects.get(id=task_id)
        if not task:
            messages.error(request, 'Invalid task ID')
            return redirect('homepage')
        if task.report_required:
            report = request.FILES.get('report')
            if not report:
                messages.error(request, 'A report appendix is required for this task')
                return redirect('homepage')
            report_path = os.path.join(settings.UPLOAD_ROOT, f'{task_id} ' + report.name)
            with open(report_path, 'wb+') as file:
                for chunk in report.chunks():
                    file.write(chunk)
        archive = ArchiveTask.objects.from_task(task)
        archive.save()
        task.delete()
        return redirect('homepage')
    subs = User.objects.filter(chief=request.user)
    data = {
        'self': Task.objects.filter(performer=request.user),
        'subs': Task.objects.filter(performer__in=subs),
        'is_chief': bool(subs),
    }
    if request.user.is_admin:
        data['other'] = Task.objects.exclude(performer=request.user).exclude(performer__in=subs)
    return render(request, 'index.html', context=data)


@admin_required
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


@admin_required
def edit_user(request):
    if request.method == 'PUT':
        print(request.body)
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(id=data.get('id'))
        if not user:
            return redirect('users')
        user.name = data.get('name')
        user.chief = User.objects.get(id=data.get('chief'))
        user.save()
        user.qualifications.set(data.get('qualifications').split(','))
        user.languages.set(data.get('languages').split(','))
        return redirect('users')

    user_id = int(request.path[11:])
    user_edited = User.objects.get(id=user_id)
    data = {
        'user_id': user_edited.id,
        'current_chief': user_edited.chief,
        'name': user_edited.name,
        'chiefs': User.objects.exclude(id=user_id),
        'user_qualifications': list(map(str, user_edited.qualifications.values_list('id', flat=True))),
        'user_languages': list(map(str,user_edited.languages.values_list('id', flat=True))),
        'qualifications': Qualification.objects.all(),
        'languages': Language.objects.all(),
    }
    return render(request, 'edit_user.html', data)


@admin_required
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
    if request.user.is_authenticated:
        return redirect('homepage')
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
                'email': user.email,
                'chief': user.chief.name if user.chief else '-'
            }
            for user in usrs
        ],
    }
    return render(request, 'users.html', context=data)


@login_required
def profile(request):
    user_id = request.path[9:]
    if request.method == 'GET' and not user_id.isdigit():
        return HttpResponse('Wrong user id')
    if request.method == 'POST':
        data = request.POST
        if not request.user.check_password(data.get('old_password')):
            messages.error(request, 'Wrong old password')
        elif data.get('new_password1') != data.get('new_password2'):
            messages.error(request, 'Passwords don\'t match')
        else:
            request.user.set_password(data.get('new_password1'))
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully')
    if not user_id:
        user_id = request.user.id
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


@admin_required
def admin(request):
    #if not request.user.is_admin:
    #    return redirect('homepage')
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


@login_required
def create_task(request):
    if request.method == 'POST':
        data = request.POST
        form = TaskCreationForm(data)
        if form.is_valid():
            task = form.save()
            return redirect('homepage')
        else:
            return redirect('create_task')
    data = {
        'form': TaskCreationForm(),
        'performers': request.user.subordinates.all(),
        'qualifications': Qualification.objects.all(),
        'languages': Language.objects.all()
    }
    return render(request, 'create_task.html', data)


@admin_required
def archive(request):
    tasks = ArchiveTask.objects.all()
    task_id = request.GET.get('task_id')
    if task_id:
        if not ArchiveTask.objects.get(id=task_id):
            messages.error(request, 'Task not found. Invalid ID')
            return redirect(request.META.get('HTTP_REFERER', 'archive'))
        report_path = ''
        for file in os.listdir(os.path.join(settings.UPLOAD_ROOT)):
            if file.startswith(f'{task_id} '):
                report_path = os.path.join(settings.UPLOAD_ROOT, file)
                break
        if not report_path:
            if tasks.get(id=task_id).report_required:
                messages.error(request, 'Report not found')
            else:
                messages.error(request, 'Report was not neccessary for this task')
            return redirect(request.META.get('HTTP_REFERER', 'archive'))
        with open(report_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
            return response
    data = {
        'tasks': [
            {
                'id': task.id,
                'name': task.name,
                'performer': task.performer,
                'deadline': task.deadline,
                'completion_date': task.completion_date,
                'report': task.report_required,
            }
            for task in tasks
        ]
    }
    return render(request, 'archive.html', data)


@login_required
def split_task(request):
    task_id = None
    data = {}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        task_id = data.get('task_id')
    else:
        task_id = request.path[12:]
    if not task_id or type(task_id) != int and not task_id.isdigit():
        messages.error(request, 'Invalid task ID')
        return redirect('homepage')
    task = Task.objects.get(id=task_id)
    if not task:
        messages.error(request, 'Task doesn\'t exist')
        return redirect('homepage')
    if request.method == 'POST':
        for subtask in data.get('subtasks'):
            new_task = Task(
                name=subtask['name'],
                deadline=subtask['deadline'],
                performer=User.objects.get(id=subtask['perf_id']),
                report_required=task.report_required,
                language_required=Language.objects.get(id=subtask['lang_id']),
            )
            new_task.save()
            new_task.qualifications_required.set(subtask['quals_id'].split(','))
        return redirect('homepage')
    form = TaskCreationForm()
    data = {
        'task': task,
        'form': form,
        'performers': [
            {
                'id': user.id,
                'name': user.name,
                'qualifications': list(user.qualifications.values_list('id', flat=True)),
                'languages': list(user.languages.values_list('id', flat=True))
            }
            for user in request.user.subordinates.all()
        ],
        'qualifications': Qualification.objects.all(),
        'languages': Language.objects.all(),
    }
    data['performers'].insert(0, {
        'id': request.user.id,
        'name': request.user.name,
        'qualifications': list(request.user.qualifications.values_list('id', flat=True)),
        'languages': list(request.user.languages.values_list('id', flat=True))
    })
    return render(request, 'split_task.html', data)


def invalid(request):
    return redirect('homepage')
