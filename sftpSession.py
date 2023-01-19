import dataclasses
import os
import paramiko
import logging
logging.basicConfig(format='%(asctime)s - %(filename)s -> %(message)s')
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)

@dataclasses.dataclass(init=True, repr=True, eq=True)
class SftpSession:
    host_conn: paramiko.Transport = None
    host_sess: paramiko.SFTPClient = None
    host: str = os.environ.get('HOST')
    username: str = os.environ.get('USERNAME')
    password: str = os.environ.get('PASSWORD')
    port: int = os.environ.get('PORT')
    address: str = f"{host}:{port}"
    addkey: str = f"[{host}]:{port}"

    def isValid(self):
        if (self.host != None and
            self.username != None and
            self.password != None and
            self.port != None):
            return True
        else: return False
    def open(self):
        if (self.isValid()):
            try:
                ssh_client = paramiko.SSHClient()
                transport = paramiko.Transport(self.address)
                transport.connect()
                ssh_client.get_host_keys().add(hostname=self.addkey,
                                               keytype=transport.get_remote_server_key(),
                                               key=transport.get_remote_server_key())
                ssh_client.connect(self.host, self.port, self.username, self.password)
                sftp_sess: object = ssh_client.open_sftp()
                self.host_conn = transport
                self.host_sess = sftp_sess
                LOG.error('Init ok: Session open')
                return sftp_sess
            except Exception as exception:
                print(exception)
                return None
        else:
            LOG.error('Init error: Env variables not set')
            return None
    def close(self):
        self.host_conn.close()
        self.host_sess.close()

def main():
    sftp_client = SftpSession()
    sftp_session = sftp_client.open()
    if sftp_session != None:
        files = sftp_session.listdir()
        sftp_client.close()
        LOG.debug(f"DIR = {files}")
    else:
        LOG.error('Init error: Sftp client not created')


if __name__ == '__main__':
    main()
