import qtl_ctp_api as m


def test_basic():
    print(m)


def test_consts():
    print(m.consts)
    print(f'THOST_TERT_QUICK: {m.consts.THOST_TERT_QUICK}')


if __name__ == '__main__':
    test_basic()
    test_consts()
