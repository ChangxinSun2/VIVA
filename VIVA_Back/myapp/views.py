from contextlib import nullcontext

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
#from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Show, Favorite
from django.http import JsonResponse
from django.db.models import Q


@api_view(['POST'])
def register_user(request):

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successful registration！"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User does not exist！"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.password == password:  # Verify Password
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful！",
            "user_id": user.id,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "role": user.role  # Returns the role field
        })
    else:
        return Response({"error": "Wrong password！"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reset_password(request):
    username = request.data.get('username')
    new_password = request.data.get('password')

    if not username or not new_password:
        return Response({"error": "Username and password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        user.password = new_password
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_shows(request):
    date = request.GET.get('date')
    address = request.GET.get('address')

    shows = Show.objects.all()


    if date and date != "null":
        shows = shows.filter(date=date)

    if address and address != "null":
        shows = shows.filter(address=address)

    result = []
    for show in shows:
        result.append({
            "s_id": show.s_id,  # Add the performance ID
            "s_name": show.s_name,
            "actor": show.actor,
            "picture": show.picture,
            "date": str(show.date),
            "address": show.address
        })

    return Response(result)

@api_view(['GET'])
def get_show_detail(request):
    show_id = request.GET.get('id')
    if not show_id:
        return Response({"error": "Missing ID"}, status=400)
    try:
        show = Show.objects.get(s_id=show_id)
        data = {
            "s_name": show.s_name,
            "actor": show.actor,
            "picture": show.picture,
            "description": show.description,
            "date": str(show.date),
            "address": show.address,
            "genre": show.genre,
            "link": show.link,
        }
        return Response(data)
    except Show.DoesNotExist:
        return Response({"error": "Show not found"}, status=404)

@api_view(['GET'])
def get_featured_shows(request):
    shows = Show.objects.all().order_by('s_id')[:8]
    result = []
    for show in shows:
        result.append({
            "s_id": show.s_id,
            "picture": show.picture,
            "s_name": show.s_name
        })
    return Response(result)

def search_show(request):
    query = request.GET.get('q', '')
    if query:
        shows = Show.objects.filter(
            Q(s_name__icontains=query) |
            Q(actor__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(genre__icontains=query)
        )[:20]
    else:
        shows = Show.objects.all()[:20]

    data = []
    for show in shows:
        data.append({
            'id': show.s_id,
            's_name': show.s_name,
            'picture': show.picture,
            'actor': show.actor,
            'date': str(show.date),
            'address': show.address
        })

    return JsonResponse({'results': data})

@api_view(['GET'])
def check_favorite(request):
    user_id = request.GET.get('user_id')
    show_id = request.GET.get('show_id')

    if not user_id or not show_id:
        return JsonResponse({'status': 'fail'})

    exists = Favorite.objects.filter(user_id=user_id, show_id=show_id).exists()
    return JsonResponse({'favorited': exists})

@api_view(['POST'])
def add_favorite(request):
    user_id = request.data.get('user_id')
    show_id = request.data.get('show_id')

    if not user_id or not show_id:
        return JsonResponse({'status': 'fail'})

    Favorite.objects.get_or_create(user_id=user_id, show_id=show_id)
    return JsonResponse({'status': 'added'})

@api_view(['DELETE'])
def remove_favorite(request):
    user_id = request.GET.get('user_id')
    show_id = request.GET.get('show_id')

    Favorite.objects.filter(user_id=user_id, show_id=show_id).delete()
    return JsonResponse({'status': 'removed'})

@api_view(['GET'])
def get_user_favorites(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'fail', 'message': 'Lack: user_id'})

    favorites = Favorite.objects.filter(user_id=user_id)
    result = []
    for fav in favorites:
        show = Show.objects.get(s_id=fav.show_id)
        result.append({
            'id': show.s_id,
            's_name': show.s_name,
            'picture': show.picture,
            'actor': show.actor,
            'date': str(show.date),
            'address': show.address
        })

    return JsonResponse({'results': result})

@api_view(['POST'])
def update_show(request):
    show_id = request.data.get('s_id')
    s_name = request.data.get('s_name')
    actor = request.data.get('actor')
    date = request.data.get('date')
    address = request.data.get('address')
    description = request.data.get('description')
    genre = request.data.get('genre')
    link = request.data.get('link')
    picture = request.data.get('picture')

    try:
        show = Show.objects.get(s_id=show_id)
        show.s_name = s_name
        show.actor = actor
        show.date = date
        show.address = address
        show.description = description
        show.genre = genre
        show.link = link
        show.save()
        return Response({"status": "success", "message": "Performance information updated"})
    except Show.DoesNotExist:
        return Response({"status": "fail", "message": "Show does not exist"})

@api_view(['DELETE'])
def delete_show(request):
    show_id = request.GET.get('s_id')
    try:
        show = Show.objects.get(s_id=show_id)
        show.delete()
        return JsonResponse({'status': 'success', 'message': '删除成功'})
    except Show.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': '演出不存在'})

@api_view(['POST'])
def create_show(request):
    s_name = request.data.get('s_name')
    actor = request.data.get('actor')
    date = request.data.get('date')
    address = request.data.get('address')
    description = request.data.get('description')
    genre = request.data.get('genre')
    link = request.data.get('link')
    picture = request.data.get('picture')

    show = Show.objects.create(
        s_name=s_name,
        actor=actor,
        date=date,
        address=address,
        description=description,
        genre=genre,
        link=link,
        picture=picture
    )
    return JsonResponse({'status': 'success', 'message': 'Successfully added performance', 'id': show.s_id})

@api_view(['GET'])
def get_all_show_details(request):
    shows = Show.objects.all()
    show_list = []
    for show in shows:
        show_list.append({
            's_id': show.s_id,
            's_name': show.s_name,
            'actor': show.actor,
            'date': str(show.date),
            'address': show.address,
            'genre': show.genre,
            'link': show.link,
            'description': show.description,
            'picture': show.picture,
        })
    return JsonResponse(show_list, safe=False)