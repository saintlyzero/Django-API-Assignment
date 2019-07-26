from ..models import UserFiles

""" Adds Record of User_Id and GCS URL """
class UserFilesService:

    def __init__(self):
      pass

    def addUserVideoRecord(self, uid, gcs_file_url):
        userFiles = UserFiles(user_id = uid, file_path = gcs_file_url)
        userFiles.save()