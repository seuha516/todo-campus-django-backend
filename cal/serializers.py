from rest_framework import serializers
from .models import Calendar

class CalendarSerializer(serializers.ModelSerializer):
     class Meta:
        model = Calendar
        fields = ('num', 'username', 'name', 'color', 'content', 'location', 'start', 'end', 'repeat')