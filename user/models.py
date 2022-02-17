from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, nickname, password, **extra_fields):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        if not nickname:
            raise ValueError('must have user nickname')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            password=password
        )
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, nickname, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'User'
    """
        유저 프로파일 사진
        유저 닉네임 -> 화면에 표기되는 이름
        유저 이름 -> 실제 사용자 이름
        유저 이메일 주소 -> 회원가입할 때 사용하는 아이디
        비밀번호 -> 디폴트 쓰자
    """
    objects = UserManager()

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=24)
    nickname = models.CharField(max_length=24, unique=True)
    profile_image = models.ImageField(null=True, upload_to="uploads/%Y/%m/%d", blank=True)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

@property
def is_staff(self):
    return self.is_admin
