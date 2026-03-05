# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from src.DBDefinitions import (
    PublicationModel,
    PublicationAuthorModel,
    PublicationTypeModel,
    PublicationCategoryModel,
    PublicationSubjectModel

)

from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel
    PublicationModel: IDLoader[src.DBDefinitions.PublicationModel] = None
    PublicationAuthorModel: IDLoader[src.DBDefinitions.PublicationAuthorModel] = None
    PublicationTypeModel: IDLoader[src.DBDefinitions.PublicationTypeModel] = None
    PublicationCategoryModel: IDLoader[src.DBDefinitions.PublicationCategoryModel] = None
    PublicationSubjectModel: IDLoader[src.DBDefinitions.PublicationSubjectModel] = None

    def __init__(self, session):
        super().__init__(session)
        self.PublicationModel = self.get(PublicationModel)
        self.PublicationAuthorModel = self.get(PublicationAuthorModel)
        self.PublicationTypeModel = self.get(PublicationTypeModel)
        self.PublicationCategoryModel = self.get(PublicationCategoryModel)
        self.PublicationSubjectModel = self.get(PublicationSubjectModel)

        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
