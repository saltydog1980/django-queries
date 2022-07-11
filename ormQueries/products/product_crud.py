from unicodedata import category
from .models import Product 
from django.db.models import Avg, Q, Max
from django.db.models.functions import Length

class ProductCrud:
    @classmethod
    def get_all_products(cls):
        return Product.objects.all()

    @classmethod
    def find_by_model(cls, model):
        return Product.objects.get(model__iexact=model)

    @classmethod
    def last_record(cls):
        return Product.objects.all().last()
        # return list(Product.objects.all())[Product.objects.count()-1]

    @classmethod
    def by_rating(cls, rating):
        return Product.objects.filter(rating__exact=rating)

    @classmethod
    def by_rating_range(cls, rating1, rating2):
        return Product.objects.filter(rating__range=(rating1, rating2))

    @classmethod
    def by_rating_and_color(cls, rating, color):
        return Product.objects.filter(rating__exact=rating).filter(color__exact=color)

    @classmethod
    def by_rating_or_color(cls, rating, color):
        return Product.objects.filter(rating__exact=rating) | Product.objects.filter(color__exact=color)

    @classmethod
    def no_color_count(cls):
        return Product.objects.filter(color__isnull=True).count()
    
    @classmethod
    def below_price_or_above_rating(cls, price, rating1):
        return Product.objects.filter(price_cents__lt=price) | Product.objects.filter(rating__gt=rating1) 

    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        return Product.objects.all().order_by('category', '-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls, like):
        return Product.objects.filter(manufacturer__icontains=like)

    @classmethod
    def manufacturer_names_for_query(cls, name):
        return list(Product.objects.filter(manufacturer__icontains=name).values_list('manufacturer', flat=True))

    @classmethod
    def not_in_a_category(cls, category):
        return Product.objects.exclude(category__iexact=category)

    @classmethod
    def limited_not_in_a_category(cls, category, limit):
        return Product.objects.exclude(category__iexact=category)[:limit]

    @classmethod
    def category_manufacturers(cls, category):
        return list(Product.objects.filter(category__iexact=category).values_list('manufacturer', flat=True))

    @classmethod
    def average_category_rating(cls, category1):
        return Product.objects.aggregate(rating__avg=Avg('rating', filter=Q(category=category1)))

    @classmethod
    def greatest_price(cls):
        return Product.objects.aggregate(price_cents__max=Max('price_cents'))

    @classmethod
    def longest_model_name(cls):
        # Product.objects.annotate(model_length = (Length('model'))).order_by('-model_length')[:1][0].pk
        return Product.objects.annotate(model_length = (Length('model'))).order_by('-model_length')[:1][0].pk

    @classmethod
    def ordered_by_model_length(cls):
        # Product.objects.annotate(model_length = (Length('model'))).order_by('-model_length')[:1][0].pk
        return Product.objects.order_by(Length('model'))
