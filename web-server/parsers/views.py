from rest_framework.decorators import api_view
from rest_framework.response import Response

from parsers.core import FACTORY
from parsers.core.media_parser import MediaParser
from parsers.core.services.response_service import create_response
from parsers.core.video_parser import VideoParserBuilder
from parsers.core.image_parser import ImgParserBuilder
from parsers.serializers import ParseContentReqSerializer, ParseContentRespSerializer


@api_view(["GET"])
def parse_content(request):
    serializer_req = ParseContentReqSerializer(data=request.query_params)
    serializer_req.is_valid(raise_exception=True)
    url = serializer_req.validated_data["url"]
    parse_type = serializer_req.validated_data["parse_type"]

    parsed_args = {
        "url": url,
        "directory": "",
        "max_videos": 0,
    }

    parser = FACTORY.create(parse_type, **parsed_args)
    parsed_objects = parser.parse()
    response_data = [{"obj_type": parse_type, "data": MediaParser.to_data(obj)} for obj in parsed_objects]
    return create_response(data=response_data, serializer_class=ParseContentRespSerializer)
