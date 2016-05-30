from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {"posts":posts})
    #從資料庫拉出Post資料放進變數posts中,並請求打開'blog/post_list.html'#
    #然後將剛剛的變數post放到一個{"posts":posts}的template變數裡頭，準備給post_list.html使用#
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    if request.method == "POST":
        #檢查request.method是否已經被存入資料，然後透過下面這行把資料都丟入ＰostFrom格式裡頭#
        form = PostForm(request.POST)
        #PostForm是我們在froms.py設立的類別，是一個用來寫新ＰＯ文或修改ＰＯ文的表單#
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        #只有進入過blog/post_edit.html，才可能滿足這個條件#
        form = PostForm(request.POST,instance=post)#instance是什麼意思？#
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)#將舊資料插入PostForm中#
    return render(request, 'blog/post_edit.html', {'form': form})
