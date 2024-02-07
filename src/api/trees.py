from fastapi import Form
from fastapi import APIRouter, UploadFile

from apps.trees.services.decoder import XmlDecoder, JsonDecoder
from apps.trees.services.tree import TreeService

router = APIRouter(prefix='/trees', tags=['Trees'])


@router.post(
    path='',
    name='get legal information',
    description='get legal information'
)
async def post_processing(
        two_tree: UploadFile,
        one_tree: str = Form(...),
):
    xml_decoded = XmlDecoder().decode(two_tree.file)
    json_decoded = JsonDecoder().decode(one_tree)

    return TreeService().process(json_decoded, xml_decoded)
