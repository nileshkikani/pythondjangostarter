from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.http import QueryDict
from model_utils import Choices
from django.db.models import Q

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'name'),
    ('2', 'email'),

)


class Admin(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin"

    def makePassword(self):
        return make_password(self.password)

    def checkPassword(self, password):
        return check_password(password, self.password)

    def datatableQuery(inputs):
        # print(inputs['order[0][column]'])
        # input=QueryDict.dict(inputs)

        draw = int(inputs["draw"])
        length = int(inputs['length'])
        start = int(inputs['start'])
        search_value = inputs['search[value]']
        order_column = inputs['order[0][column]']
        order = inputs['order[0][dir]']

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # print(order_column)
        if order == 'desc':
            order_column = '-' + order_column

        result = Admin.objects.all()
        total = result.count()
        iTotalRecords = total

        if search_value:
            result = result.filter(Q(id__icontains=search_value) |
                                   Q(name__icontains=search_value) |
                                   Q(email__icontains=search_value)
                                   )

        count = result.count()
        iTotalDisplayRecords = count

        if length == -1:
            result = result.order_by(order_column)
        else:
            result = result.order_by(order_column)[start:start + length]

        return {
            'data': result,
            'recordsFiltered': count,
            'recordsTotal': total,
            'draw': str(draw),
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords
        }
