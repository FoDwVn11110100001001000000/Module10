import os

from pymongo import MongoClient
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotemain.settings")
django.setup()

from quotes.models import Quote, Tag, Author

client = MongoClient("mongodb+srv://mattiabianchi77:Jqc3Ug6V3ZVDs6e3@cluster0.jluqaed.mongodb.net/")

db = client.module08

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )
quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exists_quote = bool(len(Quote.objects.filter(text=quote["text"])))

    if not exists_quote:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(text=quote["text"], author=a)

        for tag in tags:
            q.tags.add(tag)