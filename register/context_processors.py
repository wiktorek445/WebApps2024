from register.models import Accounts


def user_account(request):
    if request.user.is_authenticated:
        user_account1 = Accounts.objects.get(username=request.user)
        return {'user_account': user_account1}
    return {}
