from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/main.html', context)
