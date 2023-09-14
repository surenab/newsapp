from django.test import TestCase
from .models import Team, NewsComment, Message, News
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model
# Create your tests here.
class TeamTestCase(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(team_member="only a test", position="yes, this is only a test", description ="description")

    def test_team_str(self):
        self.assertEqual(str(self.team), self.team.team_member)

    def test_team_description(self):
        self.assertEqual("description", self.team.description)

    def tearDown(self) -> None:
        del self.team


class NewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username = "Info", email = "infopulse@gmail.com", password = "1234567")
        self.first_news = News.objects.create(date = datetime.now(), title = "test", description = "desc", news_type = "1", user = self.user)

    def test_news_str(self):
        pass

    def test_news_description(self):
        pass

    def tearDown(self) -> None:
        del self.user
        del self.first_news


# class NewsTestCase(TestCase):
#     def setUp(self) -> None:
#         self.first_news = News.objects.create(title="only a test", description="yes, this is only a test", news_type ="testing")

#     def test_news_str(self):
#         self.assertEqual(str(self.first_news), self.first_news.title)

#     # def test_news_title(self):
#     #     pass

#     def tearDown(self) -> None:
#         pass


# class NewsTest(TestCase):
    
#     def create_news(self, title="only a test", description="yes, this is only a test", news_type ="testing", view_count=0):
#         return News.objects.create(title=title, description=description, news_type=news_type, view_count=view_count, date=timezone.now())
    
#     def test_news_creation(self):
#         n = self.create_news()
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.assertTrue(isinstance(n, News))
#         self.assertEqual(n.__unicode__(), n.title)


# class NewsCommentTestCase(TestCase):
#     def setUp(self) -> None:
#         self.comment = NewsComment.objects.create(text="only a test")

#     def test_comm_str(self):
#         self.assertEqual(str(self.comment), self.comment.owner.username)

#     def tearDown(self) -> None:
#         pass



# class MessageTestCase(TestCase):
#     def setUp(self) -> None:
#         self.msg = Message.objects.create(full_name="only a test", subject="yes, this is only a test", message ="testing")
#         self.date = Message.objects.create(date = timezone.now())

#     def test_msg_str(self):
#         self.assertFalse(str(self.msg), self.msg.full_name)
#         # self.assertEqual(int(self.date), self.date.date)

#     def tearDown(self) -> None:
#         pass