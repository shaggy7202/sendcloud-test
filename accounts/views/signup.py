from django.contrib.auth import authenticate, forms, login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('feeds:list')

    def form_valid(self, form):
        new_user = form.save()

        # Authenticate new user
        new_user = authenticate(
            username=new_user.username,
            password=form.cleaned_data['password1'],
        )
        login(self.request, new_user)
        return super().form_valid(form)
