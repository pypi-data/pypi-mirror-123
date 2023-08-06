import quixote.build.shell as shell
import quixote.build.apt as apt


def _add_docker_repository():
    apt.update()
    apt.install(
        "apt-transport-https",
        "ca-certificates",
        "curl",
        "gnupg-agent",
        "software-properties-common"
    )
    shell.command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -")
    shell.command("apt-key fingerprint 0EBFCD88")
    # TODO: find a way not to hardcode this:
    apt.add_repository("deb https://download.docker.com/linux/debian buster stable")
    apt.update()


_DOCKER_PACKAGE = "docker-ce"
_DOCKER_CLI_PACKAGE = "docker-ce-cli"


def install_docker_cli():
    """
    Install the docker CLI
    """

    _add_docker_repository()
    apt.install(_DOCKER_CLI_PACKAGE)


def install_docker(with_cli: bool = True):
    """
    Install docker

    :param with_cli:            whether or not the docker CLI should be installed (default is True)
    """

    _add_docker_repository()
    if with_cli:
        apt.install(_DOCKER_PACKAGE, _DOCKER_CLI_PACKAGE)
    else:
        apt.install(_DOCKER_PACKAGE)
