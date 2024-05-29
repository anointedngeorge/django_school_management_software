from products.models import ProductCartLogs

def contextProcessor(request):
    try:
        user = request.user.pk
        return {
            "cart_logs": ProductCartLogs.objects.all().filter(user_id=user)
        }
    except:
        pass