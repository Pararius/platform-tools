import io
import paramiko
import sshtunnel
from google.cloud import secretmanager


def get_secret(secret_name: str, project_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
    )

    return response.payload.data.decode("UTF-8")


def create_ssh_tunnel(
    host: str,
    username: str,
    private_key: str,
    private_key_password: str,
    remote_bind_address: str,
    remote_bind_port: int,
) -> sshtunnel.SSHTunnelForwarder:
    private_key_rsa = paramiko.RSAKey.from_private_key(
        io.StringIO(private_key),
        private_key_password,
    )

    return sshtunnel.SSHTunnelForwarder(
        (host, 22),
        ssh_username=username,
        ssh_pkey=private_key_rsa,
        remote_bind_address=(remote_bind_address, remote_bind_port),
    )
