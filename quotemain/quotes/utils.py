from .models import Quote, Author, Tag


def get_quotes_with_details():
    quotes = Quote.objects.select_related("author").prefetch_related("tags").all()

    quote_details = []
    for quote in quotes:
        author = quote.author
        tags = quote.tags.all()

        quote_detail = {
            "text": quote.text,
            "created_at": quote.created_at,
            "author": {
                "fullname": author.fullname,
                "born_date": author.born_date,
                "born_location": author.born_location,
                "description": author.description,
                "created_at": author.created_at,
            },
            "tags": [{"name": tag.name} for tag in tags],
        }
        quote_details.append(quote_detail)

    return quote_details