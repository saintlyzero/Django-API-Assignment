from ..models import UserFiles

class UserFilesService:

    def __init__(self):
      pass

    def addUserVideoRecord(self, uid, gcs_file_url):
        userFiles = UserFiles(user_id = uid, file_path = gcs_file_url)
        userFiles.save()