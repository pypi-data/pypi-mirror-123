import datetime
import hashlib
import json
import os
import subprocess
import time
from collections import namedtuple

from string import Template
from tempfile import NamedTemporaryFile

import psycopg2
import pytest


Formation = namedtuple('Formation', ['id', 'namespace', 'connection_string'])


def write_formation(version, branch):
    test_root = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(test_root, 'formation_template.yaml')
    formation_id = hashlib.sha1('{}-{}'.format(version, branch).encode('utf-8')).hexdigest()
    namespace = 'ns-{}'.format(formation_id)

    binding = {
        'formation_id': formation_id,
        'namespace': namespace,
        'pg_version': version,
        'admin_password': 'test',
        'replication_password': 'test',
        'compose_password': 'test'
    }

    with open(template_path) as template_file:
        template_body = template_file.read()

    template = Template(template_body)

    with NamedTemporaryFile('w', delete=False) as spec_file:
        spec_file.write(template.substitute(binding))

    return spec_file.name, namespace, formation_id


def create_formation(version, branch):
    yaml_file, namespace, formation_id = write_formation(version, branch)

    try:
        subprocess.check_call(['kubectl', 'get', 'namespace', namespace])
    except subprocess.CalledProcessError:
        subprocess.call(['kubectl', 'create', 'namespace', namespace])

    subprocess.check_call(['kubectl', 'apply', '-f', yaml_file])
    os.remove(yaml_file)

    give_up_time = datetime.datetime.now() + datetime.timedelta(minutes=120)

    while True:
        print("Waiting for formation to complete...")
        output = subprocess.check_output(['kubectl', 'get', 'formation', formation_id,
                                          '--namespace', namespace, '-o', 'json'])
        data = json.loads(output.decode('utf-8'))
        if data['status']['state'] == 'OK':
            break
        elif datetime.datetime.now() >= give_up_time:
            pytest.fail("Timed out creating formation. [{}]".format(version, formation_id))
        time.sleep(20)

    return namespace, formation_id


def build_connection_string(environment, namespace):
    if '-db' not in environment:
        environment = '{}-db01'.format(environment)

    try:
        workers = subprocess.check_output(['bx', 'cs', 'workers', environment, '--json'],
                                          stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("Error getting workers: {} {}".format(e.returncode, e.output))
        workers = None

    if workers is None:
        # Sometimes this doesn't work immediately...
        time.sleep(20)
        workers = subprocess.check_output(
            ['bx', 'cs', 'workers', environment, '--json']
        )

    worker_ip = json.loads(workers.decode('utf-8'))[0]['publicIP']
    services = subprocess.check_output(['kubectl', 'get', 'services', '-n', namespace,
                                        '-o', 'json'])

    for service in json.loads(services.decode('utf-8'))['items']:
        if service['spec']['type'] == 'NodePort':
            node_port = service['spec']['ports'][0]['nodePort']
            return "postgres://admin:test@{}:{}/ibmclouddb?sslmode=require".format(worker_ip, node_port) # pragma: whitelist secret


def can_connect(connection_string):
    try:
        connection = psycopg2.connect(connection_string)
        c = connection.cursor()
        c.execute('SELECT 1')
    except psycopg2.OperationalError:
        return False
    return True


def set_admin_password(namespace, formation_id, connection_string):
    output = subprocess.check_output([
        'kubectl', 'exec', '-n', namespace, 'c-{}-m-0'.format(formation_id),
        '-c', 'db', '--', 'patronictl', '--config-file', '/conf/postgresql/patroni.yml',
        'list', '--format', 'json'
    ])
    leader = [member for member in json.loads(output.decode('utf-8'))
              if member['Role'] == 'Leader'][0]['Member']
    data = json.dumps({
        'username': 'admin',
        'password': 'test'
    })
    subprocess.check_call(['kubectl', 'exec', '-n', namespace, leader, '-c', 'mgmt', '--',
                           'cdb', 'execute', 'postgresql', 'change_password', data])

    give_up_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

    while True:
        print("Waiting for password to change...")
        time.sleep(20)

        if can_connect(connection_string):
            return
        elif datetime.datetime.now() >= give_up_time:
            pytest.fail('Timed out waiting for password to change. [{}]'.format(formation_id))


def setup_formation(version, environment, branch):
    namespace, formation_id = create_formation(version, branch)
    connection_string = build_connection_string(environment, namespace)

    if not can_connect(connection_string):
        set_admin_password(namespace, formation_id, connection_string)

    return Formation(formation_id, namespace, connection_string)


def make_formation_fixture(version):
    @pytest.fixture(scope="module")
    def formation(request):
        branch = request.config.getoption("--branch")
        environment = request.config.getoption("--environment")
        formation_id = request.config.getoption("--formation")
        namespace = request.config.getoption("--namespace")

        if (formation_id and not namespace) or (namespace and not formation_id):
            pytest.exit("Both namespace and formation must be provided if either are given")
            return

        formation_id_provided = formation_id and namespace

        if formation_id_provided:
            connection_string = build_connection_string(environment, namespace)
            if not can_connect(connection_string):
                set_admin_password(namespace, formation_id, connection_string)
            formation = Formation(formation_id, namespace, connection_string)
        else:
            formation = setup_formation(version, environment, branch)

        def fin():
            """Delete the namespace and formation when tests pass."""
            for test in request.node.items:
                if test.rep_call.outcome == 'passed' and not formation_id_provided:
                    subprocess.call(['kubectl', 'delete', 'namespace', test.formation.namespace])
        request.addfinalizer(fin)

        return formation

    return formation
