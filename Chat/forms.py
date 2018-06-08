from django import forms
import hashlib
from .models import User, Chat, AvailableUser, Message
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class AddChatForm(forms.Form):
    image = forms.ImageField(required=False, widget=forms.FileInput())
    is_private = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                                                                      'id': 'checkbox'}))
    chat_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'creation'}))
    chat_link = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'creation'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'creation'}))

    def save(self, user):
        hash = hashlib.md5(self.cleaned_data["password"].encode())
        if self.cleaned_data["image"]:
            chat = Chat(
                 image=self.cleaned_data["image"],
                 is_private=self.cleaned_data["is_private"],
                 chat_name=self.cleaned_data["chat_name"],
                 chat_link="@" + self.cleaned_data["chat_link"],
                 pass_hash=hash.hexdigest())
            chat.save()
        else:
            chat = Chat(
                is_private=self.cleaned_data["is_private"],
                chat_name=self.cleaned_data["chat_name"],
                chat_link="@" + self.cleaned_data["chat_link"],
                pass_hash=hash.hexdigest())
            chat.save()
        admin_user = AvailableUser(chat=chat, user=user, is_admin=True)
        admin_user.save()
        return chat


class SendMessageForm(forms.Form):
    message_context = forms.CharField(required=True, widget=forms.TextInput(attrs={"id": "chat-text-input"}))

    def save(self, username, chat_id):
        message = Message(message_context=self.cleaned_data["message_context"], chat_id=chat_id, user=username)
        message.save()
        return message


class FindPrivatesChatsForm(forms.Form):
    search_query = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "search"}))

    def try_to_get_pk_for_private_chat(self):
        if Chat.objects.filter(chat_link=self.cleaned_data["search_query"]).count() > 0:
            return Chat.objects.filter(chat_link=self.cleaned_data["search_query"]).values("pk").get("pk")


class PasswordForPrivateChats(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'input'}))

    def get_chat(self, pk, user):
        chat = Chat.objects.get(pk=pk)
        hash1 = hashlib.md5(self.cleaned_data["password"].encode())
        if chat.pass_hash == hash1.hexdigest():
            new_user_in_chat = AvailableUser(chat=chat, user=user, is_admin=False)
            new_user_in_chat.save()
            return new_user_in_chat
        else:
            raise ValidationError("Incorrect password")
