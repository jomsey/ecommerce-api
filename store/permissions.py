from rest_framework import permissions


class CustomerReadOnly(permissions.BasePermission):
    SAFE_METHODS = ['GET','HEAD','OPTIONS']
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and \
                    not request.user.groups.prefetch_related("customuser","auth").filter(name='Customers') or\
                    request.method in self.SAFE_METHODS
                )
        
class UserPermission(permissions.BasePermission):
    
    SAFE_METHODS = ['POST','HEAD','OPTIONS']
    
    def has_permission(self,request,view):
        #Allow  unauthenticated users to register, else they should be authenticated
        if request.method in self.SAFE_METHODS:
            return permissions.AllowAny
        return permissions.IsAuthenticated
           
        
			

