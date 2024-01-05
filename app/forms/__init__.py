# ruff: noqa: F401
from .auth import (
    LoginForm,
    RegistrationForm,
    ForgotForm,
    ChangePasswordForm,
    PhoneRegistrationForm,
    VerificationCodeForm,
)
from .user import (
    UserForm,
    NewUserForm,
    EmailEditForm,
    PhoneEditForm,
    CardEditForm,
    NotificationsConfigForm,
)
from .chat import ChatPhoneForm, ChatAuthIdentityForm, ChatAuthPasswordForm
from .event import EventForm
from .location import LocationForm
