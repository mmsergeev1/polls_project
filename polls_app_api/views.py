import logging
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import polls_app
from polls_app.models import Question, RegisteredVote
from .serializers import RegisteredVoteDetailSerializer


logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class RegisteredVoteDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            logging.debug(f'username = {user.username}')
            registered_votes = RegisteredVote.objects.filter(user=user)
            logging.debug(f'registered votes = {registered_votes}')
            serializer = RegisteredVoteDetailSerializer(registered_votes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (User.DoesNotExist, polls_app.models.RegisteredVote.DoesNotExist):
            logging.debug(f"anonymous_user_id = {pk}")
            registered_votes = RegisteredVote.objects.filter(anonymous_user_id=pk)
            if len(registered_votes) == 0:
                return Response({"message": "Нет опросов с таким ID пользователя"}, status=status.HTTP_404_NOT_FOUND)
            logging.debug(f'registered votes = {registered_votes}')
            serializer = RegisteredVoteDetailSerializer(registered_votes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
