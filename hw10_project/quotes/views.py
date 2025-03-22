from django.shortcuts import render
from .utils import get_mongodb
from django.core.paginator import Paginator

# Create your views here.

def main(request, page=1):
    db = get_mongodb()

    quotes = list(db.quotes.find())
    authors = list(db.authors.find())
    authors_dict = {author["_id"]: author["fullname"] for author in authors}
    for quote in quotes:
        quote["author"] = authors_dict.get(quote["author"])
    per_page=10
    paginator=Paginator(quotes, per_page)
    quotes_on_page=paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes":quotes_on_page})


