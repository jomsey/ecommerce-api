from rest_framework import permissions

SAFE_METHODS = ('GET','HEAD','OPTIONS')

class CustomerReadOnly(permissions.BasePermission):
    message = 'Only GET method is allowed with a customer account'
    
    def has_permission(self,request,view):
        
        if request.user.is_authenticated and  request.user.groups.filter(name='Customers'):
            return False
        if request.method in SAFE_METHODS:
            return True

			

