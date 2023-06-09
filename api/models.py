from django.db import models
from django.utils.timezone import now
from passlib.context import CryptContext
from secrets import token_hex
from datetime import datetime

schemes = ['pbkdf2_sha512']
CRYPT_CONTEXT = CryptContext(schemes=schemes)


class ApplicantCredit(models.Model):
    GENDER = [
        ("X", "No binari"),
        ("M", "Male"),
        ("F", "Female"),
    ]

    dni = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    gender = models.CharField(max_length=200, choices=GENDER)
    email = models.CharField(max_length=200)
    mount = models.IntegerField()
    status = models.BooleanField()

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)


class User(models.Model):

    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    @classmethod
    def hash_password(cls, password) -> str:
        '''
        Hash password
        '''
        if not password:
            return None
        return CRYPT_CONTEXT.hash(password)
    
    @classmethod
    def check_password(cls, password, hash_):
        if not hash_:
            return False
        try:
            return CRYPT_CONTEXT.verify_and_update(password, hash_)
        except ValueError:
            return False

    @classmethod
    def get_login(cls, user, password):
        valid, new_hash = User.check_password(password, hash_=user.password)
        if valid:
            session = Session().get_session(user.id)
            session.user = user
            session.save()
            if new_hash:
                user.password = new_hash
                user.save()

        return session if valid else False
    
    def save(self, *args, **kwargs):
        _hash = self.hash_password(self.password)
        self.password = _hash
        super().save(*args, **kwargs)


class Session(models.Model):

    session = models.CharField(max_length=200, default=token_hex(None))
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def expired(self):
        now = datetime.now()
        timestamp = self.date
        return abs(timestamp - now) > self.timeout()

    @classmethod
    def timeout(cls):
        return datetime.timedelta(seconds=3600)

    @classmethod
    def get_session(cls, user_id:int):
        try:
            session = Session.objects.get(user=user_id)
            if not session.expired():
                return session
            else:
                session.delete()
        finally:
            session = Session()
            session.user = user_id
            session.save()
        return session