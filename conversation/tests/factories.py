"""Factories for the ``conversation`` app."""
import factory

from django_libs.tests.factories import UserFactory

from ..models import Conversation, Message


class ConversationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Conversation

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        self.users.add(UserFactory())


class MessageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Message

    user = factory.SubFactory(UserFactory)
    conversation = factory.SubFactory(ConversationFactory)
    text = factory.Sequence(lambda n: 'This is a text {}'.format(n))
