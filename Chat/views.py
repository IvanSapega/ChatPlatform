from django.shortcuts import render, redirect, get_list_or_404
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as template_login
from .models import Chat, Message, User, AvailableUser
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, AddChatForm, SendMessageForm, FindPrivatesChatsForm, PasswordForPrivateChats


@login_required
def redirect_to_root_url(request):
    return redirect("/allchats/")


@login_required
def index(request):
    chat_list = Chat.objects.all()
    chat_count = Chat.objects.count()
    message_count = Message.objects.count()
    user_count = User.objects.count()
    if request.method == "POST":
        add_chat_form = AddChatForm(request.POST, request.FILES)
        if add_chat_form.is_valid():
            add_chat_form.save(request.user)
            return redirect("/allchats/", {"add_chat_form": add_chat_form,
                                           "username": request.user,
                                           "chat_list": chat_list,
                                           "chat_count": chat_count,
                                           "message_count": message_count,
                                           "user_count": user_count})
        else:
            return render(request, "Chat/main.html", {"add_chat_form": add_chat_form,
                                                      "username": request.user,
                                                      "chat_list": chat_list,
                                                      "chat_count": chat_count,
                                                      "message_count": message_count,
                                                      "user_count": user_count
                                                      })
    add_chat_form = AddChatForm()
    return render(request, "Chat/main.html", {"add_chat_form": add_chat_form,
                                              "username": request.user,
                                              "chat_list": chat_list,
                                              "chat_count": chat_count,
                                              "message_count": message_count,
                                              "user_count": user_count})


@login_required
def password_confirm(request, pk):
    current_chat = Chat.objects.get(pk=pk)
    if request.method == "POST":
        password_for_private_chats = PasswordForPrivateChats(request.POST)
        if password_for_private_chats.is_valid():
            password_for_private_chats.save(pk, request.user)
            return redirect("{0}".format(pk))
        else:
            return render(request, "Chat/pass.html", {"password_for_private_chats": password_for_private_chats,
                                                      "current_chat": current_chat})
    password_for_private_chats = PasswordForPrivateChats()
    return render(request, "Chat/pass.html", {"password_for_private_chats": password_for_private_chats,
                                              "current_chat": current_chat})


@login_required
def chat(request, pk):
    current_chat = Chat.objects.get(pk=pk)
    message_history = Message.objects.filter(chat=current_chat)
    chat_count = Chat.objects.count()
    message_count = Message.objects.count()
    user_count = User.objects.count()
    json_object = {"message": []}
    for key in json_object.keys():
        for message in message_history:
            if request.user == message.user:
                json_object[key].append({"username": message.user.username,
                                         "context": message.message_context,
                                         "date": str(message.date),
                                         "IsMy": True})
            else:
                json_object[key].append({"username": message.user.username,
                                         "context": message.message_context,
                                         "date": str(message.date),
                                         "IsMy": False})
    if request.method == "POST":
        send_message_form = SendMessageForm(request.POST)
        if send_message_form.is_valid():
            send_message_form.save(username=request.user, chat_id=pk)
            return redirect("/allchats/{0}".format(pk), {"send_message_form": send_message_form,
                                                                          "username": request.user,
                                                                          "chat": current_chat,
                                                                          "chat_count": chat_count,
                                                                          "message_count": message_count,
                                                                          "user_count": user_count})
        else:
            return render(request, "Chat/chat.html", {"send_message_form": send_message_form,
                                                      "username": request.user,
                                                      "chat": current_chat,
                                                      "chat_count": chat_count,
                                                      "message_count": message_count,
                                                      "user_count": user_count
                                                      })
    send_message_form = SendMessageForm()
    return render(request, "Chat/chat.html", {"send_message_form": send_message_form,
                                              "username": request.user,
                                              "chat": current_chat,
                                              "json": json.dumps(json_object),
                                              "chat_count": chat_count,
                                              "message_count": message_count,
                                              "user_count": user_count
                                              })


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        form.fields["username"].widget.attrs["class"] = "input"
        form.fields["email"].widget.attrs["class"] = "input"
        form.fields["password1"].widget.attrs["class"] = "input"
        form.fields["password2"].widget.attrs["class"] = "input"
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            template_login(request, new_user)
            return redirect("/login/")
        else:
            return render(request, "Chat/register.html", {"form": form})
    else:
        form = RegistrationForm()
        form.fields["username"].widget.attrs["class"] = "input"
        form.fields["email"].widget.attrs["class"] = "input"
        form.fields["password1"].widget.attrs["class"] = "input"
        form.fields["password2"].widget.attrs["class"] = "input"
        return render(request, "Chat/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        form.fields["username"].widget.attrs["class"] = "input"
        form.fields["password"].widget.attrs["class"] = "input"
        if form.is_valid():
            return template_login(request, "Chat/login.html")
        else:
            return render(request, "Chat/login.html", {"form": form})
    else:
        form = AuthenticationForm()
        form.fields["username"].widget.attrs["class"] = "input"
        form.fields["password"].widget.attrs["class"] = "input"
        return render(request, "Chat/login.html", {"form": form})





