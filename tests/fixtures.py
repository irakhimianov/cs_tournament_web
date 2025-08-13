from pytest_factoryboy import register

import core.factories

register(core.factories.User, _name='user_factory')
