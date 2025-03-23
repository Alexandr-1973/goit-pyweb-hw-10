from django.shortcuts import render
from .utils import get_mongodb
from django.core.paginator import Paginator
from .models import Quote, Author

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


