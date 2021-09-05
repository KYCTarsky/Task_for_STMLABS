import pytest
import sys
from main import check_mistake_argv,make_address_list_ipv4


@pytest.mark.parametrize("fail_data_cma",([['notmain.py', 'add_list.docx', 'IPv6'],
                                           ['мэйн.пай','список','Ipv3']]))
def test_check_mistake_argv(fail_data_cma):
    with pytest.raises(SystemExit):
        check_mistake_argv(fail_data_cma)


