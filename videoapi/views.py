import pdb
import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers.serializers import APIRequestSerializer, VideoSerializer, UserFilesSerializer
from .serializers.csvserializer import CSVSerializer
from .models import UserVideoMapping, UserFiles
from .services.user_video_service import UserVideoService
from .services.user_files_service import UserFilesService

class VideoAPI(APIView):
    
    def get(self, request):
        userFiles = UserFiles.objects.all()
        serializer = UserFilesSerializer(userFiles,many=True)
        return Response(serializer.data)
       

    def post(self, request):

        status = 200

        api_serializer = APIRequestSerializer(data=request.data)

        if api_serializer.is_valid():

            fileobj = request.data["video_file"]
            user_id = request.data["user_id"]
            csvChecker = CSVSerializer()
            csvCheckerResponse = csvChecker.checkCSV(fileobj)
            if csvCheckerResponse["valid"]:
                csvCheckerResponse["user_id"]= user_id
                # Save in DB
                add_video_response = UserVideoService.add_video(csvCheckerResponse)
                add_video_response['user_id'] = user_id 
                add_video_response['status'] = status

                if not add_video_response['errors_present']:     
                    add_video_response.pop('errors',None)
                    add_video_response.pop('errors_present',None)
                    fileDetails = csvChecker.get_local_file_details()
                    
                    gcs_url = csvChecker.upload_file_to_bucket(fileDetails)
                    csvChecker.delete_local_file(fileDetails['path'])
                    userFileService = UserFilesService()
                    userFileService.addUserVideoRecord(user_id,gcs_url)

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