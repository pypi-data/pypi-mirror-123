import json
import sys
import yaml
from .rabbitmq_fmu import create_fmu_with_outputs
import subprocess
import tempfile
from pathlib import Path
from abc import ABC, abstractmethod
import shutil
import uuid
import os
import glob
import psutil
import copy
import stat
from jsonschema import validate as yml_validate


class TaskLauncher(ABC):
    @abstractmethod
    def launch(self, job_dir, task_conf) -> int:
        pass

    def launch_redirect_to_log(self, job_dir, name, cmds):
        wrap_file_path = job_dir / (name + '.sh')
        with open(wrap_file_path, 'w') as wrapper:
            wrapper.write('#!/bin/bash\n')
            wrapper.write(" ".join(cmds))
            wrapper.write(" > " + name + ".log 2>&1\n")
            wrapper.flush()

        st = os.stat(str(wrap_file_path))
        os.chmod(str(wrap_file_path), st.st_mode | stat.S_IEXEC)

        p = subprocess.Popen(str(wrap_file_path), cwd=job_dir)
        print("Process started with pid: %d" % p.pid)
        return p.pid


class MaestroProcessLauncher(TaskLauncher):

    def __init__(self, jar_path) -> None:
        self.maestro_jar = jar_path

    def launch(self, job_dir, task_conf) -> int:
        java_path = shutil.which('java')
        # maestro_args = 'interpret -runtime {0} -output {1} --no-expand {2}'.format(
        #     task_conf['spec_runtime'], ".", task_conf['spec'])

        cmd = [str(java_path), '-jar', str(self.maestro_jar), 'interpret', '-runtime',
               str(job_dir / task_conf['spec_runtime']),
               '-output', ".",
               '--no-expand', str(job_dir / task_conf['spec'])]

        if 'execution' in task_conf and 'capture_output' in task_conf['execution'] and \
                task_conf['execution']['capture_output']:
            return self.launch_redirect_to_log(job_dir, "maestro_launcher", cmd)

        p = subprocess.Popen(cmd, cwd=job_dir)
        print("Process started with pid: %d" % p.pid)
        return p.pid
        # try:
        #     outs, errs = p.communicate(timeout=15)
        #     print(outs)
        #     print(errs)
        # except subprocess.TimeoutExpired:
        #     p.kill()
        #     outs, errs = p.communicate()
        #     print(outs)
        #     print(errs)


class AmqpProviderProcessLauncher(TaskLauncher):
    def launch(self, job_dir, task_conf) -> int:
        print(sys.executable)
        path = job_dir / "amqp-launch.yml"
        with open(path, 'w') as f:
            f.write(yaml.dump(task_conf))

        script = Path(__file__).parent.resolve() / 'amqp_data_repeater.py'
        cmd = [sys.executable, str(script), '--config', str(path), '--log=DEBUG']
        print(cmd)

        if 'execution' in task_conf and 'capture_output' in task_conf['execution'] and \
                task_conf['execution']['capture_output']:
            return self.launch_redirect_to_log(job_dir, "qmqp_repeater_launcher", cmd)

        p = subprocess.Popen(cmd, cwd=job_dir)
        print("Process started with pid: %d" % p.pid)
        try:
            outs, errs = p.communicate(timeout=15)
            print(outs)
            print(errs)
        except subprocess.TimeoutExpired:
            p.kill()
            outs, errs = p.communicate()
            print(outs)
            print(errs)
        return p.pid


def validate(conf):
    with open(Path(__file__).parent / 'schema.yml', 'r') as sf:
        schema = yaml.load(sf, Loader=yaml.FullLoader)
        yml_validate(conf, schema)


def show(conf):
    if 'servers' in conf:
        print('## Servers ##')
        for s in conf['servers']:
            print("Server:\n\tid: %s\n\ttype:%s\n\tembedded: %s" % (s['id'], s['type'], 'embedded' in s))


def run(conf, run_index, job_dir):
    validate(conf)
    print('''###############################################################
    
    Running from ''' + str(job_dir) + '''
    
###############################################################''')

    task_providers = {'simulation_maestro': MaestroProcessLauncher(conf['tools']['maestro']['path']),
                      'data-repeater_AMQP-AMQP': AmqpProviderProcessLauncher()}

    if 'configurations' in conf:
        config = conf['configurations'][run_index]
        print("Running: '%s'" % config['name'])
        for idx, task in enumerate(config['tasks']):

            print("State %d: %s" % (idx, task['type']))

            if 'execution' in task and 'skip' in task['execution'] and task['execution']['skip']:
                print('Skipping launch of %d: %s' % (idx, task['type']))
                continue

            identifier = "{0}_{1}".format(task['type'], task['implementation'])
            if identifier not in task_providers:
                raise "No launcher for task id: %s" % identifier

            task_launcher = task_providers[identifier]
            pid = task_launcher.launch(job_dir, task)
            with open(job_dir / (identifier + '.pid'), 'w') as f:
                f.write(str(pid))


def flatten(t):
    return [item for sublist in t for item in sublist]


def prepare(conf, run_index, job_id, job_dir, fmu_dir):
    # validate sections
    validate(conf)

    # start all one at the time
    if 'configurations' in conf:
        config = conf['configurations'][run_index]
        print("Running: '%s'" % config['name'])

        current_job_id = job_id
        # check if the job has a fixed job id
        if 'fixed_job_id' in config:
            current_job_id = config['fixed_job_id']

        for idx, task in enumerate(config['tasks']):

            print("State %d: %s" % (idx, task['type']))

            if 'simulation' in task['type']:
                # we need to generate rabbitmq fmu with the right signals
                if 'spec' in task and 'spec_runtime' in task:
                    # already processed
                    del task['config']
                    continue
                signals = flatten([([(s, t['signals'][s]['target']['datatype']) for s in (t['signals'].keys()) if
                                     'target' in t['signals'][s] and 'datatype' in t['signals'][s]['target']]) for
                                   t in config['tasks'] if t['type'] == 'data-repeater'])
                # flatten([list(t['signals'].keys()) for t in config['tasks'] if t['type'] == 'data-repeater'])
                dest = task['config']['fmus']['{amqp}']
                print("\tCreating AMQP instance with the required signals")
                create_fmu_with_outputs(
                    conf['tools']['rabbitmq']['path'], Path(fmu_dir) / Path(dest).name,
                    signals)
                # configure AMQP exchange
                task['config']['parameters']['{amqp}.ext.config.routingkey'] = current_job_id
                task['config']['parameters']['{amqp}.ext.config.exchangename'] = 'fmi_digital_twin'
                task['config']['parameters']['{amqp}.ext.config.exchangetype'] = 'direct'
                for server in conf['servers']:
                    if 'embedded' in server and server['embedded'] and server['type'] == 'AMQP':
                        task['config']['parameters']['{amqp}.ext.config.hostname'] = server['host']
                        task['config']['parameters']['{amqp}.ext.config.port'] = int(server['port'])
                        task['config']['parameters']['{amqp}.ext.config.username'] = server['user']
                        task['config']['parameters']['{amqp}.ext.config.password'] = server['password']
                        break

                print("\tImporting into Maestro for spec generating")
                with tempfile.NamedTemporaryFile(suffix='.json') as fp:
                    fp.write(json.dumps(task['config']).encode('utf-8'))
                    fp.flush()
                    cmd = "java -jar {0} import -vi FMI2   sg1 {1} -output {2} --fmu-base-dir {3}".format(
                        conf['tools']['maestro']['path'],
                        fp.name,
                        "specs", fmu_dir)
                    print(cmd)
                    subprocess.run(cmd, shell=True, check=True, cwd=job_dir)
                    task['spec'] = str(Path('specs') / 'spec.mabl')
                    task['spec_runtime'] = str(Path('specs') / 'spec.runtime.json')
                    del task['config']
            if 'data-repeater' in task['type'] and 'AMQP-AMQP' in task['implementation']:
                for signal in task['signals'].keys():
                    # including HACK for wired naming implicit to the rabbitmq fmu
                    task['signals'][signal]['target']['exchange'] = 'fmi_digital_twin'  # + '_cd'
                    task['signals'][signal]['target']['routing_key'] = current_job_id  # + '.data.to_cosim'
                for server in task['servers']:
                    task['servers'][server] = copy.deepcopy(
                        [s for s in conf['servers'] if s['id'] == task['servers'][server]][0])
                    del task['servers'][server]['id']
                    del task['servers'][server]['name']
                    del task['servers'][server]['type']


def check_launcher_status(scan_directory):
    pid_files = glob.glob(str(scan_directory) + '/*.pid')
    # print(pid_files)
    for path in pid_files:
        try:
            with open(path, 'r') as file:
                pid = int(file.read())
            if not psutil.pid_exists(pid):
                Path(path).unlink()
            else:
                print(Path(path).name + ' -- RUNNING')
        except ValueError:
            Path(path).unlink()


def check_launcher_pid_status(path):
    try:
        with open(path, 'r') as file:
            pid = int(file.read())
        if not psutil.pid_exists(pid):
            Path(path).unlink()
        else:
            return True
    except ValueError:
        Path(path).unlink()
    return False


def main():
    configuration_file = '/Users/kgl/data/au/into-cps-association/digital-twin-platform/src/dtpt/basic.yml'

    # rabbitmq_fmu_path = '/Users/kgl/data/au/into-cps-association/digital-twin-platform/src/dtpt/rabbitmq.fmu'
    # maestro_jar = '/Users/kgl/data/au/into-cps-association/maestro/maestro/target/maestro-2.1.6-SNAPSHOT-jar-with-dependencies.jar'

    project_dir = Path(__file__).parent.resolve()

    # bookkeeping
    pid_files = glob.glob(str(project_dir / 'jobs') + '/**/*.pid')
    print(pid_files)
    for path in pid_files:
        try:
            with open(path, 'r') as file:
                pid = int(file.read())
            if not psutil.pid_exists(pid):
                Path(path).unlink()
        except ValueError:
            Path(path).unlink()

    with open(configuration_file, 'r') as f:
        try:
            conf = yaml.load(f, Loader=yaml.FullLoader)
            show(conf)
            job_id = str(uuid.uuid4())
            print("Starting new job with id: %s" % job_id)

            job_dir = project_dir / 'jobs' / job_id
            os.makedirs(job_dir, exist_ok=True)

            prepare(conf, 1, job_id, job_dir=job_dir,
                    fmu_dir='/Users/kgl/data/au/into-cps-association/digital-twin-platform/src/dtpt/fmus')

            with open(job_dir / 'job.yml', 'w') as f:
                f.write(yaml.dump(conf))
            print(yaml.dump(conf))
            run(conf, 1, job_dir)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc


if __name__ == '__main__':
    main()
