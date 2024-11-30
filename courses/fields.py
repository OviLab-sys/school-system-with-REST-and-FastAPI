from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Orderfield(models.PositiveIntegerField):
    def __init__(self, for_fields = None, *args, **kargs):
        self.for_fields = for_fields
        super().__init__(*args,**kargs)
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            #no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    #filter by objects with the same field value
                    #for the fields in "for_fields"
                    query = {field: getattr(model_instance,field) for field in self.fields}
                    qs = qs.filter(**query)
                #get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.oder + 1
            except ObjectDoesNotExist:
                value = 0
                setattr(model_instance,self.attname, value)
                return value
            else:
                return super().pre_save(model_instance,add)