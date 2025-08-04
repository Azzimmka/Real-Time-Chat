from idlelib.configdialog import font_sample_text

from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
# Create your views here.

#TODO Представление для регистрации
def user_register(request):
    if request.method == 'POST':
        # Если это POST-запрос, то получаем данные из формы
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Если форма валидна, сохраняем пользователя
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            # Отправляем сообщение об успехе и перенаправляем на страницу входа
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return  redirect('login')
    else:
        # Если это GET-запрос, показываем пустую форму
        form = UserRegistrationForm()

    return render(request, 'chat/register.html', {'form': form})


#TODO Представление для входа
def user_login(request):
    if request.method == 'POST':
        # Если это POST-запрос, получаем данные из формы
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not  None:
                # Если пользователь существует и пароль верный, авторизуем его
                login(request, user)
                messages.success(request, 'Вы успешно вошли!')
                return  redirect('chat_list')
            else:
                # Если данные неверны, показываем ошибку
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()

    return  render(request, 'chat/login.html', {'form':form})


# TODO Представление для выхода
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')
