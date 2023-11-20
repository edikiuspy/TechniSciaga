def user_is_authenticated(request):
    return {'user_is_authenticated': request.user.is_authenticated}