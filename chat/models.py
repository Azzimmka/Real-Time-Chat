

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# TODO Модель UserProfile для хранения дополнительной информации о пользователе
class UserProfile(models.Model):
    # OneToOneField создает связь "один к одному".
    # У каждого UserProfile есть один связанный User и наоборот.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Поле для email
    # blank=True, null=True означают, что поле может быть пустым.
    email = models.CharField(max_length=250, blank=True, null=True)

    # Поле для аватара. upload_to указывает, куда загружать файлы.
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Поле для краткого описания
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

# ُTODO Модель для чата
class Chat(models.Model):
    is_group_chat = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True)

    # Связь "многие-ко-многим". Chat может иметь много участников, и Participant
    # может быть во многих чатах.
    participants = models.ManyToManyField(UserProfile, related_name='chats')
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL, # При удалении сообщения, поле будет Null
        null=True,
        blank=True,
        related_name='last_in_chat'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f'Чат с {self.participants.first()}'


# Модель для сообщений
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Сообщение от {self.author} в чате {self.chat}"

    class Meta:
        ordering = ['timestamp']



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()





