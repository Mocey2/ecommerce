# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogHeader, Article, Commentaire
from django.contrib.auth.decorators import login_required

def blog_list_view(request):
    header = BlogHeader.objects.first()
    articles = Article.objects.select_related('auteur', 'categorie').prefetch_related('tags')
    return render(request, 'blog/blog.html', {
        'header': header,
        'articles': articles
    })


def blog_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    commentaires = article.commentaires.filter(parent__isnull=True).select_related('utilisateur')

    if request.method == 'POST':
        if request.user.is_authenticated:
            contenu = request.POST.get('comment')
            parent_id = request.POST.get('parent_id')
            parent = Commentaire.objects.filter(id=parent_id).first() if parent_id else None

            if contenu:
                Commentaire.objects.create(
                    article=article,
                    utilisateur=request.user,
                    contenu=contenu,
                    parent=parent
                )
                return redirect('blog-detail', slug=slug)
        else:
            return redirect('login')

    articles_recents = Article.objects.exclude(id=article.id).order_by('-date_publication')[:3]

    return render(request, 'blog/blog-single.html', {
        'article': article,
        'commentaires': commentaires,
        'articles_recents': articles_recents,
    })
