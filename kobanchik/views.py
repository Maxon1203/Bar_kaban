from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import *


def main(request):
    return render(request, 'main.html')


def bar_list(request):
    bars = Bar.objects.all()
    return render(request, 'bars/bar_map_search.html', {'bars': bars})


def bar_detail(request, pk):
    bar = Bar.objects.get(id=pk)
    review = Review.objects.get()

    context = [
        {'bar': bar},
        {'review': review}
    ]
    return render(request, 'bars/bar_detail.html', context)


from django.views.generic import ListView, DetailView


class TopBarListView(ListView):
    model = Bar
    template_name = 'bars/bar_reating.html'

    def get_queryset(self):
        context = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        context = context.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        if search_query:
            context = context.filter(name__icontains=search_query)
        return context


class ListFest(ListView):
    model = Festival
    template_name = 'bars/bar_festival.html'

    def get_queryset(self):
        context = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        if search_query:
            context = context.filter(name__icontains=search_query)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BarSearchForm(self.request.GET)
        return context


class ListBars(ListView):
    model = Bar
    template_name = 'bars/bar_list.html'
    context_object_name = 'bars'

    def get_queryset(self):
        context = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        if search_query:
            context = context.filter(name__icontains=search_query)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BarSearchForm(self.request.GET)
        return context


class DetailBar(DetailView):
    model = Bar
    template_name = 'bars/bar_detail.html'

    def get_queryset(self):
        return Bar.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


from .forms import *


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            CustomUser.objects.create(user=user, avatar=form.cleaned_data.get('avatar'))
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registr.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('list_bar')

        messages.error(request, 'Что-то пошло не так')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def log_out(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('auth_form')


from django.contrib.auth.decorators import login_required


def ProfileUser(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'user/profile_user.html', {'user': user})


@login_required
def add_comment(request, review_id):
    bar = Bar.objects.get(pk=review_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user.customuser
            comment.bar = bar
            comment.save()
            return redirect('list_bar')
    else:
        form = CommentForm()
    return render(request, 'user/add_comment.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})


@login_required
def add_to_favorites(request, bar_id):
    bar = get_object_or_404(Bar, pk=bar_id)
    user = request.user.customuser
    user.liked_bars.add(bar)
    return redirect('bar_detail', pk=bar_id)


def delete_to_favorites(request, bar_id):
    bar = get_object_or_404(Bar, id=bar_id)
    request.user.customuser.liked_bars.remove(bar)
    return redirect('profile', pk=request.user.customuser.pk)
