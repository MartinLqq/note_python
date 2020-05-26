class BaseConf:
    pass


class DevConf(BaseConf):

    DEBUG = True


class TestConf(BaseConf):

    DEBUG = True


class ProdConf(BaseConf):

    DEBUG = False


CONF = {
    'development': DevConf,
    'test': TestConf,
    'production': ProdConf
}
__all__ = ['CONF']
