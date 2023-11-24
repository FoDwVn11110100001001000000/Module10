from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import QuoteForm, AuthorForm
from .models import Tag, Author
from .utils import get_quotes_with_details


def main(request, page=1):
    quotes = get_quotes_with_details()
    per_page = 10
    paginator = Paginator(list(quotes), per_page=per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            choice_authors = Author.objects.filter(
                fullname__in=request.POST.getlist("author")
            )
            new_quote.author = choice_authors.first()
            new_quote.tags.set(choice_tags)
            new_quote.save()

            return redirect("quotes:root")
    else:
        form = QuoteForm()

    return render(
        request,
        "quotes/add_quote.html",
        {"tags": tags, "authors": authors, "form": form},
    )


def author_details(request, author_fullname):
    # Retrieve the author details using the provided fullname
    author = Author.objects.get(fullname=author_fullname)

    return render(request, "quotes/author_details.html", {"author": author})