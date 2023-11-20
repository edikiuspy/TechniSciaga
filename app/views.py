import wikipedia
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm, TitleForm, ContentForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
wikipedia.set_lang('pl')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')

def custom_permission_denied(request, exception):
    return render(request, 'permission_denied.html', status=403)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto utworzone dla {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def logined_view(request):
    #posts = Post.objects.filter(author=request.user)
    posts = Post.objects.all()
    context = {
        'title': 'Profile',
        'welcome_message': f'Witaj, {request.user.username}!',
        'posts': posts,
    }
    return render(request, 'profile.html', context)
def logout_view(request):
    logout(request)
    return redirect('home')
def home_view(request):
    context = {
        'title': 'Witam',
        'welcome_message': 'To moja strona na ściągi',
    }
    return render(request, 'home.html', context)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('profile')
        else:
            return render(request, 'post_form.html', {'form': form})
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    '''if post.author != request.user:
        return render(request, 'permission_denied.html')'''
    context = {'post': post, }
    # if post.file:
    #     print(os.path.abspath('static')+post.file.url.replace(".zip",'').replace('/static',''))
    #     path=os.path.abspath('static')+post.file.url.replace(".zip",'').replace('/static','')
    #     file_list = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(path) for f in filenames]
    #     if os.path.exists(os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static','')):
    #         path2=os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static','')
    #
    #         [file_list.append(os.path.join(dirpath,f)) for (dirpath, dirnames, filenames) in os.walk(path2) for f in filenames]
    #     context['file_list']=file_list
    return render(request, 'post_detail.html', context)
@login_required
def post_edit_wiki(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return render(request, 'permission_denied.html')

    if request.method == 'POST':
        if 'title-form' in request.POST:
            form = TitleForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post title updated.')
                return redirect('post_detail', pk=post.pk)
        elif 'content-form' in request.POST:
            form = ContentForm(request.POST, instance=post)

            if form.is_valid():
                form.save()
                messages.success(request, 'Post content updated.')
                return redirect('post_detail', pk=post.pk)
        else:
            tempdict = request.POST.copy()
            tempdict['content'] = wikipedia.page(tempdict['content']).summary
            request.POST = tempdict
            print(request.POST)
            form = PostForm(request.POST, instance=post)

            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated.')
                return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        title_form = TitleForm(instance=post)
        content_form = ContentForm(instance=post)
    return render(request, 'post_edit_wiki.html',
                  {'form': form, 'title_form': title_form, 'content_form': content_form, 'post': post})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return render(request, 'permission_denied.html')

    if request.method == 'POST':
        if 'title-form' in request.POST:
            form = TitleForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post title updated.')
                return redirect('post_detail', pk=post.pk)
        elif 'content-form' in request.POST:
            form = ContentForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post content updated.')
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated.')
                return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        title_form = TitleForm(instance=post)
        content_form = ContentForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'title_form': title_form, 'content_form': content_form, 'post': post})




@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return render(request, 'permission_denied.html')

    post.delete()
    return redirect('profile')
# @login_required
# def upload_file(request):
#     form = PostForm(request.POST)
#     if form.is_valid():
#         post = form.save(commit=False)
#         if request.FILES.get('file'):
#             post.file=request.FILES['file']
#         post.author = request.user
#         post.save()
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         with open(f'static/{file.name}', 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
#         if file.name.endswith('.zip'):
#             with zipfile.ZipFile(file, 'r') as zip_ref:
#                 zip_ref.extractall("static/")
#                 for name in zip_ref.namelist():
#
#
#                     if os.path.splitext(name.split("/")[-1])[1]==".html":
#                         path=f"templates/{file.name.replace('.zip','')}"
#                         os.makedirs(path,exist_ok=True)
#                         try:
#                             shutil.move(f"static/{name}",path)
#                             with open(f'templates/{name}', 'r+') as f:
#                                 content = f.read()
#                                 soup = BeautifulSoup(content, 'html.parser')
#                                 for tag in soup.find_all():
#                                     if tag.has_attr('href') and not tag.has_attr('data'):
#                                         href = tag['href']
#                                         if not href.startswith('http') and not href.startswith(
#                                                 '#') and not href.startswith('mailto:'):
#                                             new_href = "{% static '" + name.split("/")[0]+"/"+href + "' %}"
#                                             tag['href'] = new_href
#                                     elif tag.has_attr("src") and not tag.has_attr("data"):
#                                         src = tag["src"]
#                                         if not src.startswith("http") and not src.startswith(
#                                                 "#") and not src.startswith("mailto:"):
#                                             new_src = "{% static '" + name.split("/")[0] + "/" + src + "' %}"
#                                             tag["src"] = new_src
#                                 new_content = str(soup)
#                                 f.seek(0, 0)
#                                 f.write('{% load static %}\n' + new_content)
#
#
#
#                         except:
#                             pass
#
#                     path = os.path.abspath('static')+post.file.url.replace(".zip",'').replace('/static','')
#                     file_list = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(path) for f in
#                                  filenames]
#                     print(os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static',''))
#                     if os.path.exists(os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static','')):
#                         print(os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static',''))
#                         path2 = os.path.abspath('templates')+post.file.url.replace(".zip",'').replace('\static','')
#
#                         [file_list.append(os.path.join(dirpath, f)) for (dirpath, dirnames, filenames) in os.walk(path2)
#                          for f in filenames]
#             os.remove(f'static/{file.name}')
#             return render(request, 'upload_success.html', {'file_list': file_list})
#         return redirect('profile')
#     else:
#         return redirect('post_create')
# def display_file(request, file_name):
#     file_path = file_name
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as file:
#             content_type = mimetypes.guess_type(file_path)[0]
#             if content_type is None:
#                 content_type = 'application/octet-stream'
#             if content_type.startswith('text/html'):
#                 template_engine = engines['django']
#                 template = template_engine.from_string(file.read().decode('utf-8'))
#                 context = {}
#                 rendered_template = template.render(context)
#                 response = HttpResponse(rendered_template, content_type=content_type)
#             else:
#                 response = HttpResponse(file.read())
#                 response['Content-Type'] = content_type
#             response['Content-Disposition'] = f'inline; filename="{file_name}"'
#             return response
#     else:
#         raise Http404