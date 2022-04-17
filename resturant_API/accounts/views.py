from reservations.views import AdminRoleMixin
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer


class UserAPIView(AdminRoleMixin, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def post(self, request):
        '''
        Creates a new user
        '''
        serializer = self.serializer_class(data=request.data)
        employee_number = request.data.get('employee_number')

        # checks if user with employee number already exists
        is_user_exists = CustomUser.objects.filter(employee_number=employee_number).exists()
        if is_user_exists:
            return Response(
                {"res": "User with " + employee_number + " already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "result": "user created successfully", "data": serializer.validated_data['employee_number']},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
