from rest_framework import serializers
from poll.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["email","username","password","phone","id"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChoiceSerializer(serializers.ModelSerializer):
    votes=serializers.SerializerMethodField()
    voters=serializers.SerializerMethodField()
    class Meta:
        model=Choice
        fields="__all__"
        read_only_fields=["id","poll_object"]
    def get_votes(self,object):
        votes_qs=Vote.objects.filter(choice_object=object)
        return votes_qs.count()
    def get_voters(self,object):
        votes_qs=Vote.objects.filter(choice_object=object)
        return votes_qs.values_list('owner_object__username',flat=True)


class PollSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)
    choices=serializers.SerializerMethodField()
    total_vote=serializers.SerializerMethodField()
    class Meta:
        model=Poll
        fields="__all__"
        read_only_fields=["owner","created_at","is_active"]
    def get_choices(self,object):
        choice_qs=Choice.objects.filter(poll_object=object)
        serializer_instance=ChoiceSerializer(choice_qs,many=True)
        return serializer_instance.data
    def get_total_vote(self,object):
        votes_qs=Vote.objects.filter(poll_object=object)
        # sreializer_instance=VoteSerializer(votes_qs,many=True)
        return votes_qs.count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields="__all__"
        read_only_fields=["id","poll_object","owner_object","created_at"]