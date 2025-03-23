from django.shortcuts import render, redirect, get_object_or_404

from .forms import AuthorForm, QuoteForm
from .utils import get_mongodb
from django.core.paginator import Paginator
from .models import Quote, Author, Tag


# Create your views here.

def main(request, page=1):
    quotes = Quote.objects.all()
    authors_dict = {author.id: author.fullname for author in Author.objects.all()}
    for quote in quotes:
        quote.author_name = authors_dict.get(quote.author_id)
    per_page=10
    paginator=Paginator(quotes, per_page)
    quotes_on_page=paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes":quotes_on_page})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author_form.html', {'form': form})

    return render(request, 'quotes/add_author_form.html', {'form': AuthorForm()})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author']
            print(author_name)
            print(Author.objects.filter(fullname=author_name).first())
            author = Author.objects.filter(fullname=author_name).first()
            # print(author_name,author)


            tags_str = form.cleaned_data['tags']  # Получаем теги как строку
            tag_names = [tag.strip() for tag in tags_str.split(',')]  # Разбиваем и убираем пробелы

            # Находим существующие теги или создаём новые
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)  # Если нет - создаёт
                tags.append(tag)

            # Создаём объект Quote
            quote = form.save(commit=False)
            quote.author = author
            quote.save()

            # Добавляем теги к цитате
            quote.tags.set(tags)
            #
            # quote = form.save(commit=False)  # Создаём объект Quote, но не сохраняем
            # quote.author = author  # Присваиваем найденного автора
            # quote.save()
            # # form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote_form.html', {'form': form})

    return render(request, 'quotes/add_quote_form.html', {'form': QuoteForm()})