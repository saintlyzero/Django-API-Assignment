import csv
import io
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from google.cloud import storage


class CSVSerializer:

   NUMBER_OF_COLS = 2

   COL1 = "video_name"
   COL2 = "video_size"
  
   bucket_name = 'b-ao-locale-19'
   
   local_file_path = ''
   local_file_name = ''
   gcs_file_path = ''
   

   def __init__(self):
      pass
   
   def get_local_file_details(self):
      local_file = {'path':self.local_file_path,'file_name':self.local_file_name}
      return local_file

   """ Store File Locally """
   def file_upload_local(self,reqest_file):
      
      fs = FileSystemStorage()
      filename = fs.save(reqest_file.name, reqest_file)
      uploaded_file_url = fs.url(filename)
      self.local_file_path = uploaded_file_url
      self.local_file_name = filename
      return uploaded_file_url

   def upload_file_to_bucket(self, file_details):
      
      resp = {}
      
      local_path = file_details['path']
      file_name = file_details['file_name']
      destination_blob_name = os.path.join('test',file_name)
      
      try:
         """ Upload file to the bucket """
         storage_client = storage.Client()
         bucket = storage_client.get_bucket(self.bucket_name)
         blob = bucket.blob(destination_blob_name)
         blob.upload_from_filename(local_path)
         gcs_url = 'https://storage.cloud.google.com/%(bucket)s/%(file)s' % {'bucket':self.bucket_name, 'file':destination_blob_name}
         resp['error'] = False
         resp['gcp_url'] = gcs_url
      except:
         resp['error'] = True
      finally:
         return resp

   def delete_local_file(self,file_path):
      os.system('rm -f '+file_path)
   
   def checkCSV(self,rawFile):

      RESPONSE = {
      'valid': False,
      'video_list': [],
      'local_file_path':'',
      'errors':[]
       }

      isValid = False
      data = []

      """ Check File Format """
      if rawFile.content_type != "text/csv":
         RESPONSE["errors"] ="CSV file required"
         return RESPONSE

      decoded_file = rawFile.read().decode('utf-8')
      io_string = io.StringIO(decoded_file)

      
      """ Check number of columns for each row """
      rawCSV = csv.reader(io_string, delimiter=',')
      for idx, line in enumerate(rawCSV):
   
         if len(line) != self.NUMBER_OF_COLS:
            RESPONSE["errors"] = "Columns expected: "+str(self.NUMBER_OF_COLS)+" on line "+str(idx+1)
            return RESPONSE
      
      """ Store file locally """
      local_path = self.file_upload_local(rawFile)
      RESPONSE['local_file_path'] = local_path
     

      """ Read the CSV File """
      df = pd.read_csv(local_path)
      
      
      """ Validate Column names """

      cols = df.keys()
      if cols[0] != self.COL1 or cols[1] != self.COL2:
         
         RESPONSE["errors"] = "Expected column names: "+self.COL1+", "+self.COL2
         return RESPONSE
      
      data = df.values
      for index in data:
         temp = {}
         temp["video_name"] = index[0]
         temp["video_size"] = index[1]
         RESPONSE["video_list"].append(temp)
         
      RESPONSE["valid"] = True

      return RESPONSE
   

  