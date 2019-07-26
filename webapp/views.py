import pdb

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employees
from .serializers import EmployeesSerializers
from .services.employee_service import EmployeeService


""" This APP is a Demo app. 
    Go to Videoapi App      """
    
class EmployeeList(APIView):

    def get(self, request):
        employees = Employees.objects.all()
        serializer = EmployeesSerializers(employees,many=True)
        return Response(serializer.data)

    def post(self, request):
    
        # import pdb; pdb.set_trace()
        serializer = EmployeesSerializers(data=request.data)
        if serializer.is_valid():
            print('Request is valid')
            print('Sending data to service')
            EmployeeService.add_employee(request.data)
            return Response({"success":"true"}) 
        else:
            return Response({"success":"false"}) 