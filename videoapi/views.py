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

    STATUS = 200
    
    def get(self, request):
        req_userid = request.query_params['user_id']
        userFilesSerializer = UserFilesSerializer(data = request.query_params)
        if userFilesSerializer.is_valid(): 
            userFiles = UserFiles.objects.filter(user_id = req_userid)
            serializer = UserFilesSerializer(userFiles,many=True)
            return Response(serializer.data)
        else: 
            return Response({'error':'user_id does not exist','status':self.STATUS})
       

    def post(self, request):

        api_serializer = APIRequestSerializer(data=request.data)

        if api_serializer.is_valid():

            fileobj = request.data["video_file"]
            user_id = request.data["user_id"]
            csvChecker = CSVSerializer()
            csvCheckerResponse = csvChecker.checkCSV(fileobj)
            if csvCheckerResponse["valid"]:
                csvCheckerResponse["user_id"]= user_id
                
                """ Save in user_video_mapping table """
                
                add_video_response = UserVideoService.add_video(csvCheckerResponse)
                add_video_response['user_id'] = user_id 
                add_video_response['status'] = self.STATUS

                if not add_video_response['errors_present']:     
                    add_video_response.pop('errors',None)
                    add_video_response.pop('errors_present',None)
                    fileDetails = csvChecker.get_local_file_details()
                    
                    """ Upload File to GSC """
                    gcs_service_resp = csvChecker.upload_file_to_bucket(fileDetails)
                    if gcs_service_resp['error']:
                        return Response({'error':'Error while uploading to GCS Bucket','status':self.STATUS})
                    
                    gcs_url = gcs_service_resp['gcp_url']
                    csvChecker.delete_local_file(fileDetails['path'])

                    """ Add Record of user_id and File URL """
                    userFileService = UserFilesService()
                    userFileService.addUserVideoRecord(user_id,gcs_url)

                add_video_response.pop('errors_present',None)            
                return Response(add_video_response)
            
            else:
                error_details={}
                error_details["errors"] = csvCheckerResponse["errors"]
                error_details["status"] = self.STATUS
                return Response(error_details)

        else:
            error_details={}
            error_details["errors"] = api_serializer.errors.keys()
            error_details["status"] = self.STATUS
            return Response(error_details) 