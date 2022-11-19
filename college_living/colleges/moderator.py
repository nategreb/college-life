from moderation import moderation
from moderation.moderator import GenericModerator
from colleges.models import Dorms, ResidentialArea

class DormsModeration(GenericModerator):
    auto_approve_for_groups = ['Admin', 'Mods']
    
    
class ResidentialAreaModeration(GenericModerator):
    auto_approve_for_groups = ['Admin', 'Mods']
    
  
#TODO: moderation for college related models  
# moderation.register(Dorms, DormsModeration)
# moderation.register(ResidentialArea, ResidentialAreaModeration)