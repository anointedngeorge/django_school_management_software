def check_permission(request, appname:str, crud:str, model:str):
    
    if appname and crud and model:
        try:
            command= f"{appname}.{crud}_{model}".lower()
            user = request.user
            if not user.is_superuser:
                result = user.has_perm(command)
                return result
            else:
                return True
        except Exception as e:
            return str(e)
    return False