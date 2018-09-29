import os
from cryptography.fernet import Fernet

# since parms are already in the code , do they need to be written to files??
def setup():
    if not os.path.exists(os.path.expanduser('~\\etl\\')+'ketl_mysql.bin'):
        os.makedirs(os.path.dirname((os.path.expanduser('~\\etl\\')+'ketl_mysql.bin')))
        with open(os.path.expanduser('~\\etl\\')+'ketl_mysql.bin', 'wb') as file_objectk:
            file_objectk.write(b'esoLDNiVt_rFtRXF9a_R41Gv6bC4vbyvEHAAE9Mgvm4=')
        with open(os.path.expanduser('~\\etl\\')+'eetl_mysql.bin', 'wb') as file_objecte: file_objecte.write\
            (b'gAAAAABbYA00XHbUJeeRyAUb0sGiBqAUGwWC1k9I9IJ1xh0_gG2MjiVvNJnk42P5N85poBy0zPPbF8RFLJXCxboTstC2-Q2KuQ==')
        with open(os.path.expanduser('~\\etl\\')+'uetl_mysql.bin', 'wb') as file_objectu: file_objectu.write\
            (b'gAAAAABbYB9w_FMCMYK_FAEqoHo-zonQLXYBoziP8gyCdTG7bVobFxCTKz5_1S2ABeF8ocCopBR3aMFA1ruRvWDLgFTgmFeyAA==')


def ke():
    with open(os.path.expanduser('~\\etl\\')+'ketl_mysql.bin', 'rb') as obk:
        for l in obk:
            k = l
    with open(os.path.expanduser('~\\etl\\')+'eetl_mysql.bin', 'rb') as obe:
        for li in obe:
            e = li
    with open(os.path.expanduser('~\\etl\\')+'uetl_mysql.bin', 'rb') as obu:
        for lu in obu:
            u = lu
    return Fernet(k).decrypt(e), Fernet(k).decrypt(u)
