from rest_framework import permissions

SAFE_METHODS = ('GET','HEAD','OPTIONS')

class CustomerReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and not request.user.groups.filter(name='Customers') or request.method in SAFE_METHODS)
           
        
			

