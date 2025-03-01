from website.models import Issue, Points, User, UserProfile, Domain
from rest_framework import  serializers
from django.db.models import Sum

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user model
    """
    def get_total_score(self,instance):
        score = Points.objects.filter(user=instance.user).aggregate(total_score=Sum('score')).get("total_score")
        if score==None: return 0
        return score
    
    def get_activities(self,instance):
        
        issues = Points.objects.filter(user=instance.user,score__gt=0).values("issue__id")
        return [ issue["issue__id"] for issue in issues ]


    user = UserSerializer(read_only=True)
    total_score = serializers.SerializerMethodField(method_name="get_total_score")
    activities = serializers.SerializerMethodField(method_name="get_activities")

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "title",
            "follows",
            "user",
            "user_avatar",
            "description",
            "winnings",
            "follows",
            "issue_upvoted",
            "issue_saved",
            "issue_flaged",
            "total_score",
            "activities"
        )


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue Model
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    """
    Serializer for Domain Model
    """

    class Meta:
        model = Domain
        fields = '__all__'

