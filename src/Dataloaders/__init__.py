# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from src.DBDefinitions import (
    EventModel,
    EventInvitationModel,
    PublicationModel,
    PublicationAuthorModel,
    PublicationTypeModel,
    PublicationCategoryModel
)

from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel

    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    PublicationModel: IDLoader[src.DBDefinitions.PublicationModel] = None
    PublicationAuthorModel: IDLoader[src.DBDefinitions.PublicationAuthorModel] = None
    PublicationTypeModel: IDLoader[src.DBDefinitions.PublicationTypeModel] = None
    PublicationCategoryModel: IDLoader[src.DBDefinitions.PublicationCategoryModel] = None

    def __init__(self, session):
        super().__init__(session)

        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.PublicationModel = self.get(PublicationModel)
        self.PublicationAuthorModel = self.get(PublicationAuthorModel)
        self.PublicationTypeModel = self.get(PublicationTypeModel)
        self.PublicationCategoryModel = self.get(PublicationCategoryModel)

        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
