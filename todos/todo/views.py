from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, "todo/home.html")


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "todo/loginuser.html",
                {"form": AuthenticationForm(), "error": "Неверные данные для входа"},
            )
        else:
            login(request, user)
            return redirect("currenttodos")


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


def signupuser(request):
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("currenttodos")
            except IntegrityError:
                return render(
                    request,
                    "todo/signupuser.html",
                    {
                        "form": UserCreationForm(),
                        "error": "Такой пользователь уже существует. Задайте другое.",
                    },
                )
        else:
            return render(
                request,
                "todo/signupuser.html",
                {
                    "form": UserCreationForm(),
                    "error": "Пароли не совпадают",
                },
            )


def currenttodos(request):
    todos = Todo.objects.all()
    return render(request, "todo/currenttodos.html", {"todos": todos})


def createtodo(request):
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form": TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect("currenttodos")
        except ValueError:
            return render(
                request,
                "todo/createtodo.html",
                {
                    "form": TodoForm(),
                    "error": "Переданы не верные данные. Прпробуйте еще раз.",
                },
            )


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    return render(request, "todo/viewtodo.html", {"todo": todo})
