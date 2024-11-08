from rest_framework import serializers
from .models import Entry, Audio


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ["file", "uploaded_at"]
