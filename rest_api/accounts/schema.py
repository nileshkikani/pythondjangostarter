from typing_extensions import Required
from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError, error

from .models import User, Profile
from crud_operations.models import SpaceFeatureList, SpaceList, SpaceFeature
import time
from .jwtToken import EncodeData, DecodeData
from .decorators import *
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter
from graphene.utils.str_converters import to_snake_case
from graphene_django_pagination import DjangoPaginationConnectionField
from graphene_file_upload.scalars import Upload

class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        order = args.get('orderBy', None)
        if order:
            if type(order) is str:
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs

class SpaceListType(DjangoObjectType):
    class Meta:
        model = SpaceList
        fields = ('spaceName','x','y',)
        
class SpaceFeatureType(DjangoObjectType):
    class Meta:
        model = SpaceFeature

# class SpaceFeatureListFilter(FilterSet):
#     class Meta:
#         model = SpaceFeatureList

#     order_by = OrderingFilter(
#         fields=(
#             ('id'),
#         )
#     )


class SpaceFeatureListType(DjangoObjectType):
    # spaceFeatures = graphene.List(SpaceFeatureType)
    # print("---in")
    
    # @graphene.resolve_only_args
    # def resolve_spaceFeatures(self):
    #     return self.spaceFeatures.all()

    name = graphene.String(required=True)
    
    class Meta:
        model = SpaceFeatureList        
        filter_fields = {
            "spaceFeatures__feature" : ["in", "iexact"],
        }
        order_by = OrderingFilter(
        fields=(
            ('id'),
            )
        )
        interfaces = (graphene.relay.Node, )

class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "email": ["icontains", "exact"]
        }
        # order_by = OrderingFilter(
        # fields=(
        #     ('id'),
        #     )
        # )

# class DomainName(graphene.Interface):
#     message = graphene.String()
#     m = ''

# class RegistrarInfo(graphene.ObjectType):
#     class Meta:
#         interfaces = (DomainName,)

#     def resolve_message(self, args, context, info):
#         # Code to get the registrar
#         return self.message

# class UserLoginCustomMessages(graphene.ObjectType):

#     message = graphene.String()

#     def resolve_message(self, args, context, info):
#         return self.message

# class FeatureInputs(graphene.InputObjectType):
#     feature = graphene.String()

class Query(graphene.ObjectType):
    all_space_list = graphene.Field(SpaceListType, name=graphene.String(required=True))
    all_space_feature_id = graphene.List(SpaceFeatureListType)
    get_feature_name = graphene.Field(SpaceFeatureType, name=graphene.String(required=True) )
    # List as input
    # get_features_name = graphene.Field(lambda: graphene.List(SpaceFeatureType), name=graphene.List(graphene.String))
    # get_space_names = graphene.List(SpaceFeatureListType)
    feature = graphene.relay.Node.Field(SpaceFeatureListType)
    all_features = OrderedDjangoFilterConnectionField(SpaceFeatureListType, orderBy=graphene.List(of_type=graphene.String))
    get_users = DjangoPaginationConnectionField(UserType)
    # sort_all_features = DjangoFilterConnectionField(SpaceFeatureListType)

    def resolve_all_space_list(root, info, name):
        try:
            return SpaceList.objects.get(spaceName=name)
        except SpaceList.DoesNotExist:
            return None
    
    def resolve_all_space_feature_id(root, info):
        # We can easily optimize query count in the resolve method
        return SpaceFeatureList.objects.select_related("x").all()

    def resolve_get_feature_name(root, info, name):
        try:
            print(type(SpaceFeature.objects.get(feature=name)))
            return SpaceFeature.objects.get(feature=name)
        except SpaceFeature.DoesNotExist:
            return None
    
    def resolve_get_users(self, info, **kwargs):
        return User.objects.all()
    
    # def resolve_all_features(root, info, name):
    #     return None
    
    # def resolve_get_features_name(root, info, feature1, feature2):        
    #     # print(type(SpaceFeature.objects.filter(feature__in=name)))
    #     # try:
    #     #     return SpaceFeature.objects.filter(feature__in=name)
    #     # except SpaceFeature.DoesNotExist:
    #     #     return None
    #     try:
    #         return SpaceFeature.objects.filter(feature__in=[feature1, feature2])
    #     except SpaceFeature.DoesNotExist:
    #         return None

    
    # def resolve_get_space_names(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return SpaceFeatureList.objects.select_related("y").all()

class SpaceMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        new_space = graphene.String(required=True)        

    # The class attributes define the response of the mutation
    edges = graphene.Field(SpaceListType)

    @classmethod
    def mutate(cls, root, info, new_space):
        space = SpaceList(spaceName=new_space)
        space.save()
        # Notice we return an instance of this mutation
        return SpaceMutation(edges=space)


class UserRegisterMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)        
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    edges = graphene.Field(UserType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, email, password):
        message = None
        user = None
        try:
            User.objects.get(email=email)
            raise Exception("Email already registered!")
        except User.DoesNotExist:
            print("in")
            splitValues = email.split('@')
            user = User(email=email, username=splitValues[0] + "_" + str(round(time.time() * 1000)))
            user.set_password(password)
            user.save()
            return UserRegisterMutation(edges=user,message="Registered successfully!")

class UserLoginMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String()        
        password = graphene.String()
        socialId = graphene.String()
        loginType = graphene.String()

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()

    @classmethod
    def mutate(cls, root, info, email=None, password=None, socialId=None, loginType=None):
        user = None
        token=None
        if (loginType == "email") and (email and password is not None):
            try:
                user = User.objects.get(email=email)
                print("user",user)
                if user.isLogin == True:
                    raise Exception("You are already logged-in!")
                if user.check_password(password):
                    encoded_jwt = EncodeData({"id": user.id})
                    user, created = User.objects.update_or_create(email=user.email, defaults={'isLogin': True, 'loginType': loginType})                               
                    return UserLoginMutation(user=user,token=encoded_jwt,message="Logged-in successfully!")
                else:
                    raise Exception("Either email or password is incorrect!")
            except User.DoesNotExist:
                # message="Hi!"
                # message = resolver_message(root, info, message)
                raise Exception("Please sign-up first!")
        
        elif (loginType == "facebook") and (socialId is not None):
            try:
                user = User.objects.get(facebookId=socialId, loginType=loginType)
                if user.isLogin == True:
                    raise Exception("You are already logged-in!")
                encoded_jwt = EncodeData({"id": user.id})
                return UserLoginMutation(user=user,token=encoded_jwt,message="Logged-in successfully!")
            except User.DoesNotExist:
                user = User.objects.create(username=loginType + "_" + str(round(time.time() * 1000)), facebookId=socialId, loginType=loginType, isLogin=True)
                user.set_unusable_password()
                user.save()
                encoded_jwt = EncodeData({"id": user.id})
                return UserLoginMutation(user=user,token=encoded_jwt,message="Logged-in successfully!")
        
        elif (loginType == "google") and (socialId is not None):
            try:
                user = User.objects.get(facebookId=socialId, loginType=loginType)
                if user.isLogin == True:
                    raise Exception("You are already logged-in!")
                encoded_jwt = EncodeData({"id": user.id})
                return UserLoginMutation(user=user,token=encoded_jwt,message="Logged-in successfully!")
            except User.DoesNotExist:
                user = User.objects.create(username=loginType + "_" + str(round(time.time() * 1000)), googleId=socialId, loginType=loginType, isLogin=True)
                user.set_unusable_password()
                user.save()
                encoded_jwt = EncodeData({"id": user.id})
                return UserLoginMutation(user=user,token=encoded_jwt,message="Logged-in successfully!")
        else:
            raise Exception("Input parameter combination is incorrect!")


class UserLogoutMutation(graphene.Mutation):

    # The class attributes define the response of the mutation
    message = graphene.String()

    # @classmethod
    @isUserAuthenticatedGraphQL
    def mutate(root, info, userId):
        if type(userId) is dict:
            userName = User.objects.get(pk=userId['id'])                        
            User.objects.update_or_create(email=userName.email, defaults={'isLogin': False})  
            return UserLogoutMutation(message="Logged-out successfully!")
        else:
            return Exception(userId)


class UserUploadPicMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file
        print(file)
        return UserUploadPicMutation(success=True)

class Mutation(graphene.ObjectType):
    create_space = SpaceMutation.Field()
    user_register = UserRegisterMutation.Field()
    user_login = UserLoginMutation.Field()
    user_logout = UserLogoutMutation.Field()
    upload_pic = UserUploadPicMutation.Field()
   


schema = graphene.Schema(query=Query, mutation=Mutation)

# {
#   allSpaceFeatures(name:"feature1") {
    # y {
    #   spaceNames {
    #     spaceName
    #   }
    #   spaceFeatures {
    #     feature
    #   }
    # }
#   }
# }

# mutation firstmutation {
#   createSpace(newSpace:"Raiya circle") {
#     edges {
#       spaceName
#     }
#   }
# }
