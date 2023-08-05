# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tideploy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1.2,<6.0.0', 'fabric>=2.5.0,<3.0.0', 'paramiko>=2.7.0,<3.0.0']

entry_points = \
{'console_scripts': ['tideploy = tideploy.cli:run']}

setup_kwargs = {
    'name': 'tideploy',
    'version': '0.1.1',
    'description': 'Remote deployment using Fabric',
    'long_description': "# tideploy: remote deployment simplified\n\n`tideploy` is a simple tool to simplify remote deployment using SSH. While it has been specifically designed for deploying Docker containers, it can be easily configured for other deployment pipelines.\n\n`tideploy` is a Python CLI script that depends on [Fabric](https://www.fabfile.org/), a library for executing shell commands remotely over SSH.\n\n### What `tideploy` can do\n\n`tideploy` performs the following steps:\n\n1. Connects to a remote host via SSH\n2. Transfers files to a remote host\n3. Runs a script contained in the files called `deploy.sh`\n\nThese are all very simple, but due to the versatile nature of steps 2 and 3 you can perform nearly any task. An example deployment can be found in `/example_deployments`. There, the deploy script as well as a docker-compose file and .env file are transferred, after which Docker Compose is executed from the script.\n\n### Installation and basic usage\n\n```shell\npip install tideploy\n```\n\n`tideploy` is a CLI script that requires a number of arguments to function. To easily employ `tideploy` in a virtualenv, [Poetry](https://python-poetry.org) is recommended. Once installed, you can view the `tideploy` help by running:\n\n```shell\npoetry run tideploy --help\n```\n\n`tideploy` does not support password-authenticated SSH connections for security reasons. Use an SSH keyfile instead. If the keyfile is protected by a passphrase, you will be prompted to enter it.\n\nBy default, `tideploy` will look for a `/deployment` folder in the working directory and transfer its contents to a `/deployment` folder in the remote server's home directory. Subsequently, the `deploy.sh` script (which is assumed to be part of the files that are transferred) is executed.\n\nThe 'hostname' and 'user' arguments are required.\n\n```shell\ntideploy -n bar.com -u foo\n```\nwill connect to user foo at host bar.com, with the SSH key located at `./keys/ssh.key`.\n\n### Usage guide\n\n```\nusage: tideploy [-h] [-y YAML] -n HOST -u USER [-p PORT] [-k KEY] [-svn SVN_URL] [-s SOURCE] \n[-t TARGET]\n\nDeploy app remotely using Python Fabric.\n\nExamples:\ntideploy -n bar.com -u foo -s bar_deployment -t bar_target\ntideploy --yaml deployments/foo_deployment.yml\ntideploy -n bar.com -u foo -svn https://github.com/foo/bar/trunk/baz\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -y YAML, --yaml YAML  YAML configuration file location. Optional and can be used only \n  instead of CLI arguments. (default: ./deployments/deployment.yml)\n\narguments:\n  -n HOST, --host HOST  Remote server hostname\n  -u USER, --user USER  Remote server user\n  -p PORT, --port PORT  Remote SSH port (default: 22)\n  -k KEY, --key KEY     SSH key location for remote access (default: ./keys/ssh.key)\n  -svn SVN_URL, --svn-url SVN_URL\n                        If files are not stored locally, you can use an SVN (Subversion) \n                        URL to check out a specific directory that will be transferred. \n                        Specify the local download location using the --source argument. \n                        SVN must be installed for this to work.\n  -s SOURCE, --source SOURCE\n                        Directory (relative to the script or absolute path) that contains \n                        the deployment files (.env, docker-compose.yml and tideploy.sh). \n                        'tideploy.sh' is required! Every file in the directory (including \n                        in subdirectories) will be\n                        transferred. Note that this is the directory download destination \n                        for SVN checkout if an SVN link was provided for '--svn-url'. \n                        (default: ./deployments/deployment)\n  -t TARGET, --target TARGET\n                        Target directory in the remote server where all files from the \n                        subdirectory will be loaded into. This must be an absolute path or \n                        relative to the target server home directory. (default: ./deployment)\n```\n\n#### YAML configuration file\n\nIf you do not want to specify all arguments from the command line, you can supply it with a YAML file instead by denoting the file name after the `--yaml` flag. All other flags are then ignored and only the YAML file is read. See the `example_deployments/deploynent.yml` file for the syntax.\n\n#### SVN link\n\nIf you want to be sure you are sending the most recent deployment files or you do not want to download them first, you can use a SVN (Subversion) link to check them out locally before sending them. Use the `--svn-url` option. You can check out a single directory from all GitHub repositories this way ([GitHub Docs](https://docs.github.com/en/github/importing-your-projects-to-github/working-with-subversion-on-github/support-for-subversion-clients)). \n\nFor example, if you want to transfer the contents of the `/baz` directory from the HEAD branch of the `foo/bar` GitHub repository, you can use `https://github.com/foo/bar/trunk/baz`. If you want it from some other branch, replace `trunk` with `branches/<branch>`.\n\n### Supported platforms\n\n`tideploy` depends on Fabric, which itself depends on [Paramiko](https://www.paramiko.org/installing.html), which relies on a number of non-pure Python packages (bcrypt, cryptography and PyNaCl, the latter of which relies on cffi). This requirement means only platforms for which these packages have binary releases are supported, but that should include almost all.\n\n`tideploy` is primarily targeted at Linux → Linux deployment pipelines. Windows and macOS are untested. ",
    'author': 'Tip ten Brink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tiptenbrink/deploy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
