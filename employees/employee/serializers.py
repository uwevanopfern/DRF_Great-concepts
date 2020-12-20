from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions

from . import models


class TaskSerializer(serializers.ModelSerializer):
    """ HyperlinkedModelSerializer gives url of specific user"""

    class Meta:
        """ Meta class tells django which fields to take in model """
        model = models.Tasks
        # fields = '__all__'
        fields = ('id', 'user', 'name', 'description')
        # extra_kwargs = {'user': {'read_only': True}}  # read only means user field will nt be shown while posting data
        depth = 1  # this will give the details of user

        """
        >>> task = TaskSerializer(data={'user': 1, 'name' :'Clean', 'description': 'Clean this before noon'})
        >>> task.is_valid()
        True
        >>> task.errors
        {}
        """
        #
        # def create(self, validated_data):
        #     """ Create and return new user"""
        #
        #     tasks = models.Tasks(
        #         user=self.request.user,
        #         name=validated_data['name'],
        #         description=validated_data['description']
        #     )
        #
        #     tasks.save()
        #
        #     return tasks+" Created successfully"

        """
        >>> task = Tasks.objects.get(id=2)
        >>> oops = TaskSerializer(task, many=True)
        >>> oops = TaskSerializer(task)
        >>> oops.data
        {'id': 2, 'user': 2, 'name': 'Cook', 'description': 'Cook well bro'}
        >>> data = oops.data
        >>> data
        {'id': 2, 'user': 2, 'name': 'Cook', 'description': 'Cook well bro'}
        >>> data["user"]
        >>> 2
        """

        """
        GET USER DATA AND ACCESS ON EACH AND EVERY FIELD IN TABLE
        >>> user = UserProfile.objects.get(id=1)
        >>> user
        <UserProfile: admin@gmail.com>
        >>> user.name
        'Uwe Van Admin'
        >>> user.is_active
        True
        >>>
        """

        """UPDATE SPECIFIC DATA
        >>> task = Tasks.objects.get(id=2)
        >>> task
        >>> update_task = TaskSerializer(task, data={"description": 'Cook well bro'}, partial=True)
        >>> update_task.is_valid()
        True
        >>> update_task.save()
        <Tasks: Cook>
        >>> update_task.data
        {'id': 2, 'user': 2, 'name': 'Cook', 'description': 'Cook well bro'}
        """

        """WHEN PARSING MANY OBJECT IN SERIALIZER YOU NEED TO PROVIDE many=True coz of many data, when it is single 
        data there is not need to parse in serializer 
        >>> tasks = Tasks.objects.all()
        >>> serialized = TaskSerializer(tasks, many=True)
        >>> serialized.data
        [OrderedDict([('id', 1), ('user', 1), ('name', 'Clean'),
        ('description', 'Clean this before noon')]),
        OrderedDict([('id', 2), ('user', 2), ('name', 'Cook'), 
        ('description', 'Cook well bro')
        ])]
        >>>
        """


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """ HyperlinkedModelSerializer gives url of specific user"""

    tasks = TaskSerializer(many=True, read_only=True)
    # tasks = TaskSerializer(many=True)

    class Meta:
        """ Meta class tells django which fields to take in model """
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password', 'url', 'tasks')
        extra_kwargs = {'password': {'write_only': True}}  # write only means pwd will not be return in json result

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            # instance.set_password(make_password(password, salt=None, hasher='pbkdf2_sha1'))
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    message = "User is not activated"
                    raise exceptions.ValidationError(message)
            else:
                message = "Unable to login with given credentials"
                raise exceptions.ValidationError(message)
        else:
            message = "Provide username or password"
            raise exceptions.ValidationError(message)
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

