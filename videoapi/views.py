import pdb
import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers.serializers import APIRequestSerializer, VideoSerializer
from .serializers.csvserializer import CSVSerializer
from .models import UserVideoMapping
from .services.user_video_service import UserVideoService

class VideoAPI(APIView):
    
    def get(self, request):
        return Response({"success":"Hit API"}) 

    def post(self, request):

        status = 201

        api_serializer = APIRequestSerializer(data=request.data)

        if api_serializer.is_valid():

            fileobj = request.data["video_file"]
            print('file obj > ',type(fileobj))
            user_id = request.data["user_id"]
            csvChecker = CSVSerializer()
            csvCheckerResponse = csvChecker.checkCSV(fileobj)
            if csvCheckerResponse["valid"]:
                csvCheckerResponse["user_id"]= user_id
                # Save in DB
                add_video_response = UserVideoService.add_video(csvCheckerResponse)
                add_video_response['user_id'] = user_id 
                add_video_response['status'] = 201
                print(add_video_response)

                if not add_video_response['errors_present']:     
                    add_video_response.pop('errors',None)
                    add_video_response.pop('errors_present',None)

                add_video_response.pop('errors_present',None)            
                return Response(add_video_response)
            
            else:
                error_details={}
                error_details["errors"] = csvCheckerResponse["errors"]
                error_details["status"] = status
                return Response(error_details)

        else:
            error_details={}
            error_details["errors"] = api_serializer.errors.keys()
            error_details["status"] = status
            return Response(error_details) 