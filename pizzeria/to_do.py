class Vote(models.Model):
	user = user
	vote = vote
	chooice = choice

class VoteSerializer(serializers.ModelSeriliazer):
	class Meta:
		model = Vote
		fields = ['user', 'vote', 'chooice']

class VoteViewSet(viesets.GenericModelVieset):
	serializer_class = VoteSerializer



# urls
router = SimpleRouter()
router.register('/votes', VoteViewSet, 'votes')



# tests.py
def test_vote_create(self):
	response = self.client.post(reverse('votes'), date={'vote': 4, 'chooice': 3})
	# 127.0.0.1:8000/votes
	self.assertEqual(response.status_code, 201)
