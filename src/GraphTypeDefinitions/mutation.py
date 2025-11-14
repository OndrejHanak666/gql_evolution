import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .PublicationGQLModel import PublicationMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, PublicationMutation):
    pass

