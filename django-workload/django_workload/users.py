# This application has no real users.
# Instead, we select a random user id from those available in the database.
import random
from functools import wraps

from .models import UserModel


def require_user(view):
    user_ids = None

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        nonlocal user_ids
        if user_ids is None:
            user_ids = [u.id for u in UserModel.objects.all()]
        user_id = random.choice(user_ids)
        request.user = UserModel.objects.get(id=user_id)
        return view(request, *args, **kwargs)
    return wrapper
