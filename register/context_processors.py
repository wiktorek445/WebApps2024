from register.models import Accounts


def user_account(request):
    if request.user.is_authenticated:
        user_account = Accounts.objects.get(username=request.user)
        return {'user_account': user_account}
    return {}
