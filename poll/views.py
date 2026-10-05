from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.views import APIView
from poll.serializers import UserSerializer,PollSerializer,ChoiceSerializer,VoteSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from poll.models import *
from rest_framework import serializers
# Create your views here.




class UserCreateView(CreateAPIView):
    serializer_class=UserSerializer

class PollView(CreateAPIView,ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerializer
    queryset=Poll.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class PollListView(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerializer
    queryset=Poll.objects.all()


class PollRetrieveView(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerializer
    queryset=Poll.objects.all()

class PollDeleteView(DestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerializer
    queryset=Poll.objects.all()

class ChoiceView(CreateAPIView):
    serializer_class=ChoiceSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        poll_id=self.kwargs.get('pk')
        pollobj=Poll.objects.get(id=poll_id)
        return serializer.save(poll_object=pollobj)

class VoteCreateView(CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=VoteSerializer

    def perform_create(self, serializer):
        pid=self.kwargs.get('pk')
        print(pid)
        poll_object=Poll.objects.get(id=pid)
        valid_choice_object=Choice.objects.filter(poll_object=poll_object)
        choice_object=serializer.validated_data.get('choice_object')
        # choice_object=Choice.objects.get(id=choice_id)
        if choice_object not in valid_choice_object:
            raise serializers.ValidationError("Invalid Choice for poll")
        return serializer.save(poll_object=poll_object,owner_object=self.request.user)

    
        
