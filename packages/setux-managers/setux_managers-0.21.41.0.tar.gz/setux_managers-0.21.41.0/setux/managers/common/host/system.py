from pybrary.net import get_ip_adr
from pybrary.func import memo

from setux.core.manage import Manager


class Distro(Manager):
    '''System Infos
    '''
    manager = 'system'

    @property
    def hostname(self):
        attr = '_hostname_'
        try:
            val = getattr(self, attr)
        except AttributeError:
            ret, out, err = self.run('hostname')
            val = out[0]
            setattr(self, attr,  val)
        return val

    @hostname.setter
    def hostname(self, val):
        attr = '_hostname_'
        delattr(self, attr)
        new_val = val.replace('_', '-')

        new_hostname = self.target.read('/etc/hostname')
        current = new_hostname.strip()
        new_hostname = new_hostname.replace(current, new_val)
        self.target.write('/etc/hostname', new_hostname)

        new_hosts = self.target.read('/etc/hosts')
        new_hosts = new_hosts.replace(current, new_val)
        self.target.write('/etc/hosts', new_hosts)

        ret, out, err = self.run(f'hostname {new_val}')
        return ret

    @memo
    def fqdn(self):
        ret, out, err = self.run('hostname -f')
        return out[0]
