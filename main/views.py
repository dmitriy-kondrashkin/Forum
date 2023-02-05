from django.shortcuts import render, redirect
from .forms import PostCreateForm

# Create your views here.
def feed (request):
    return render(request, 'main/home.html')

def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('/')
    else:
        form = PostCreateForm()
    return render(request,'post_create.html', {'form':form})
