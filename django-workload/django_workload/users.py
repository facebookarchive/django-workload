# This application has no real users.
# Instead, we select random users from those available in the database.
import random
from functools import wraps
from threading import Lock

from .models import UserModel

# global cache; normally fetching users is cached in memcached or similar
user_ids = None
def all_users():
    global user_ids
    if user_ids is None:
        with Lock():
            # re-check after acquiring the lock, as another thread could have
            # taken it between checking for None and requesting the lock.
            if user_ids is None:
                user_ids = [u.id for u in UserModel.objects.all()]
    return user_ids


def require_user(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user_id = random.choice(all_users())
        request.user = UserModel.objects.get(id=user_id)
        return view(request, *args, **kwargs)
    return wrapper


def suggested_users(user, count=5):
    """Suggest a number of users for this user to follow

    A random sample of users not already followed is included.
    """
    followed = set(user.following)
    return random.sample(
        [uuid for uuid in all_users() if uuid not in followed], count)
