from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from .models import UserProfile, Tasks
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import filters

from .serializers import UserProfileSerializer, TaskSerializer, LoginSerializer


# Create your views here.


# class TaskListView(generics.GenericAPIView,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.CreateModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin):
#     serializer_class = TaskSerializer
#     queryset = Tasks.objects.all().order_by('-id')
#     lookup_field = 'id'
#
#     def get(self, request, id=None):
#
#         if id:
#             return self.retrieve(request, id)
#         else:
#             return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#         # return Response(request.data)
#
#     def perform_create(self, serializer):
#         """ Set the user profile to the logged in user """
#         serializer.save(user=self.request.user)
#
#     def put(self, request, id=None):
#         return self.update(request, id)
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def delete(self, request, id=None):
#         return self.destroy(request, id)


class TaskOfUserAPIView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):

        user = Tasks.objects.filter(user=user_id)
        serializer = TaskSerializer(user, many=True)

        return Response(serializer.data)


class TaskAPIView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_object = Tasks.objects.all().order_by('-id')
        # many=True indicates that they are many objects to return not only one
        serializer = TaskSerializer(task_object, many=True)
        return Response(serializer.data, status=200)  # safe allow a list or non-dict objects to be into json

    def post(self, request):

        incoming_data = request.data
        serializer = TaskSerializer(data=incoming_data)

        if serializer.is_valid():
            serializer.save()
            # serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

        # return Response(data)


class TaskDetailAPIView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_object(self, id):

        try:
            return Tasks.objects.get(id=id)
        except Tasks.DoesNotExist as e:
            return Response({"error": "Given object not found"}, status=404)

    def get(self, request, task_id=None):

        instance = self.get_object(task_id)
        serializer = TaskSerializer(instance)
        return Response(serializer.data)

    def put(self, request, task_id=None):

        # return Response(request.data)
        """
        if we want to make partial update (patch)
        we will do the following in serializer initialization
        serializer = TaskSerializer(instance, data=incoming_data, partial=True)
        partial will tell django rest and serializer that update is going to be made is not updating the whole fields
        instead it will update some fields in even model

        """
        incoming_data = request.data
        instance = self.get_object(task_id)
        serializer = TaskSerializer(instance, data=incoming_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, task_id=None):
        instance = self.get_object(task_id)
        instance.delete()
        return Response({"result": "Data deleted"}, status=204)


@csrf_exempt
def task_counts(request):

    task_object = Tasks.objects.count()

    if request.method == "GET":

        return JsonResponse({"total": task_object}, safe=False)  # safe allow a list or non-dict objects to be into json

#    # return JsonResponse(serializer.errors, status=400)
#     elif request.method == "POST":
#         # converting POST data into json format by using JSONParser
#         data = JSONParser().parse(request)
#
#         serializer = TaskSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return JsonResponse(serializer.data, status=201)
#
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def task_details(request, task_id):
#
#     try:
#         instance = Tasks.objects.get(id=task_id)
#
#     except Tasks.DoesNotExist as e:
#         return JsonResponse({"error": "Given object not found"}, status=404)
#
#     if request.method == "GET":
#         serializer = TaskSerializer(instance)
#         return JsonResponse(serializer.data)  # safe allow a list or non-dict objects to be into json
#     # return JsonResponse(serializer.errors, status=400)
#     elif request.method == "PUT":
#         # converting POST data into json format by using JSONParser
#         data = JSONParser().parse(request)
#
#         serializer = TaskSerializer(instance, data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return JsonResponse(serializer.data, status=200)
#
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#
#         instance.delete()
#
#         return JsonResponse({"result": "Data deleted"}, status=204)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ ModelViewSet is magic it takes care of CRUD of existing django model"""

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        # token, created means if token is available return it or if it is not create new one(created is FALSE or TRUE)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):

    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        # remove the session of the logged in user
        django_logout(request)
        return Response(status=204)
