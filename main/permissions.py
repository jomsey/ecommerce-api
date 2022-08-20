from rest_framework import permissions

class CustomerReadOnly(permissions.BasePermission):
    SAFE_METHODS = ['GET','HEAD','OPTIONS']
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and \
                    not request.user.groups.filter(name='Customers') or\
                    request.method in self.SAFE_METHODS
                )
           
        
			

