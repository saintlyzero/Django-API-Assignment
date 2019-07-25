from ..models import UserVideoMapping
from ..serializers.serializers import VideoSerializer


class UserVideoService:

    def __del__(self):
        print('##__UserVideoService Dectructor__##')

    def add_video(data):

        RESPONSE = {'errors_present': False, 'errors':[], 'saved_videos':[]}    
       
        for indx, video in enumerate(data["video_list"]):

            uid = data["user_id"]
            vname = video["video_name"]
            vsize = video["video_size"]
            tmp = {'user_id':uid,'video_name':vname,'video_size':vsize}
            video_serializer = VideoSerializer(data = tmp)

            if video_serializer.is_valid():
                user_video_mapping = UserVideoMapping(user_id=uid,video_name=vname,video_size=vsize)
                user_video_mapping.save()
                RESPONSE['saved_videos'].append(vname)
                
            else:
                RESPONSE["errors_present"] = True
                errors = video_serializer.errors.keys()

                for err in errors:
                    RESPONSE['errors'].append(err+" on line "+str(indx+1))

        return RESPONSE    
                
                