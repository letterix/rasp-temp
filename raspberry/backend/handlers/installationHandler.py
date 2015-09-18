from dao import InstallationDao
from uuid import getnode as get_mac


def get_installation():

    installation = InstallationDao.get()
    if installation and installation['serial_number'] == str(get_py_mac()):
        return installation
    print("Setting correct serial_number")
    serial_number = get_py_mac()
    model = 'pi'
    print("real serial_number is: ", serial_number)
    InstallationDao.create(serial_number, model)
    installation = InstallationDao.get()
    print("serial_number now set to: ", installation.get('serial_number'))
    return installation

def get_py_mac():
    mac = get_mac()
    if (mac >> 40)%2:
        raise OSError("The system could not find the mac address of the pi")
    return mac