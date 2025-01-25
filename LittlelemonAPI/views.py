from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from . import models, serializers

class HomeView(APIView):
    def get(self, request):
        return Response('The home view.', status.HTTP_200_OK)

class ThrottleCheckView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        return Response({"message": "Throttle check."})

class ManagerAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        managers = Group.objects.get(name="Manager")
        serialized_item = serializers.UserSerializer(managers, many=True)
        return Response(serialized_item.data)

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": f'User {username} is set as manager.'})

    def delete(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": f'User {username} is deleted from manager group.'})

class GroupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serialized_item = serializers.GroupSerializer(Group.objects.all(), many=True)
        return Response(serialized_item.data)

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = models.Category.objects.all()
        serialized_item = serializers.CategorySerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)

    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = serializers.CategorySerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        item = get_object_or_404(models.Category, pk=id)
        serialized_item = serializers.CategorySerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)

    def put(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.Category, pk=id)
        serialized_item = serializers.CategorySerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)

    def patch(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.Category, pk=id)
        serialized_item = serializers.CategorySerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)

    def delete(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.Category, pk=id)
        item.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class MenuItemView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        items = models.MenuItem.objects.all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = serializers.MenuItemSerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)

    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = serializers.MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)

class MenuItemDetailView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, id):
        item = get_object_or_404(models.MenuItem, pk=id)
        serialized_item = serializers.MenuItemSerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)

    def put(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.MenuItem, pk=id)
        serialized_item = serializers.MenuItemSerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)

    def patch(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.MenuItem, pk=id)
        serialized_item = serializers.MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)

    def delete(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(models.MenuItem, pk=id)
        item.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class ManagerSetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": f'User {username} is set as manager.'}, status.HTTP_201_CREATED)

    def get(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        managers = User.objects.filter(groups=Group.objects.get(name="Manager"))
        serialized_item = serializers.UserSerializer(managers, many=True)
        return Response(serialized_item.data)

class ManagerDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=id)
        if user.groups.filter(name='Manager').exists():
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message": f'User {user.username} is not manager now.'}, status.HTTP_200_OK)
        return Response({"message": "This user is not a manager"}, status.HTTP_400_BAD_REQUEST)

class DeliverySetView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        crews = Group.objects.get(name="Delivery crew")
        crews.user_set.add(user)
        return Response({"message": f'User {username} is set as delivery crew.'}, status.HTTP_201_CREATED)

    def get(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        crews = User.objects.filter(groups=Group.objects.get(name="Delivery crew"))
        serialized_item = serializers.UserSerializer(crews, many=True)
        return Response(serialized_item.data)
