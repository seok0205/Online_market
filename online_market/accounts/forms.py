from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):    # 비밀번호 수정 경로 커스텀 할 수 있게 UserChangeForm의 생성자 메서드를 오버라이딩
        super().__init__(*args, **kwargs)
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")  # reverse: url_name으로부터 url을 찾아가는 함수
            self.fields["password"].help_text = password_help_text

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()    # 현재 활성화된 user model, User를 model로 사용
        fields = UserCreationForm.Meta.fields