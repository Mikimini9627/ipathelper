import configparser
import os
import subprocess
import sys

def publish(section):
    rc = os.path.expanduser('~/.pypirc')
    if not os.path.exists(rc):
        print('ERROR: ~/.pypirc が見つかりません')
        sys.exit(1)

    cfg = configparser.ConfigParser()
    cfg.read(rc)

    if not cfg.has_section(section):
        print(f'ERROR: ~/.pypirc に [{section}] セクションがありません')
        sys.exit(1)

    url      = cfg.get(section, 'repository', fallback='https://upload.pypi.org/legacy/')
    username = cfg.get(section, 'username',   fallback='')
    password = cfg.get(section, 'password',   fallback='')

    env = os.environ.copy()
    env['UV_PUBLISH_USERNAME'] = username
    env['UV_PUBLISH_PASSWORD'] = password

    result = subprocess.run(
        ['uv', 'publish', '--publish-url', url],
        env=env
    )
    sys.exit(result.returncode)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python publish.py <section>')
        sys.exit(1)
    publish(sys.argv[1])