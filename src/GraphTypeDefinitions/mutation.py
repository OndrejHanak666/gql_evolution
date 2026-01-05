import strawberry

from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .PublicationGQLModel import PublicationMutation
from .PublicationAuthorGQLModel import PublicationAuthorMutation
from .PublicationTypeGQLModel import PublicationTypeMutation
from .PublicationCategoryGQLModel import PublicationCategoryMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(
    EventMutation, 
    EventInvitationMutation,
    PublicationMutation,
    PublicationAuthorMutation,
    PublicationTypeMutation,
    PublicationCategoryMutation
):
    pass

