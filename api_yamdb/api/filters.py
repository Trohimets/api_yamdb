import django_filters
from reviews.models import Title

class TitleFilter(django_filters.FilterSet):
    
    class Meta:
        model = Title
        fields = {
            'genre__name': ['contains'],
            'category__name': ['contains'],
            'year': ['exact'],
            'name': ['exact']
        }