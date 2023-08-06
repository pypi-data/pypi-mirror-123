# -*- coding: utf-8 -*-

from os import makedirs, stat_result
from pathlib import Path
from sys import stdout
from enum import Enum
import PrintTags as pt

from typing import Optional, Union, List, Tuple, Type, overload, Sequence


class JobNotAvailableError(Exception):
    ...


class RunMode(Enum):
    TRAIN = 'Train'
    INFERENCE = 'Inference'

    @classmethod
    def list_values(cls) -> Tuple[str, ...]:
        # noinspection PyTypeChecker
        return tuple(map(lambda c: c.value, cls))

    @classmethod
    def list_members(cls) -> Tuple['RunMode', ...]:
        # noinspection PyTypeChecker
        return tuple(map(lambda c: c, cls))


def _query_yes_no(question: str, default: Optional[str] = None) -> bool:
    """
    Queries the user for a yes/no answer to a given question

    args:
        question: The question the user is answering
        default: The default answer if none is provided
    """

    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt: str = ' [y/n] '
    elif default == 'yes':
        prompt: str = ' [Y/n] '
    elif default == 'no':
        prompt: str = ' [y/N] '
    else:
        raise ValueError(f'Invalid default answer: {default}')

    while True:
        stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            stdout.write('Please respond with "yes", '
                         '"no", "y", or "n"\n')


def _query_job_name() -> str:
    while True:
        name = input('Please enter a name for the current job: ')
        if _validate_job_name(name):
            return name
        else:
            pt.notice('The job name provided is invalid. '
                      'Please remove any spaces or special '
                      'characters other than "_" and try again.',
                      tag=False)


def _query_mode(allowed_modes: Optional[Sequence[RunMode]] = None) -> RunMode:
    stdout.write('Which operation mode would you like?\n')
    mode_members: Tuple[RunMode, ...]
    if allowed_modes is None:
        mode_members = RunMode.list_members()
    else:
        mode_members = tuple(allowed_modes)
    for i, mode in enumerate(mode_members):
        value: str = mode.value
        pt.green(f'{i + 1}: {value}')
    while True:
        input_value: str = input('Please enter the number of the mode you would like to use: ')
        try:
            mode_number: int = int(input_value)
        except ValueError:
            pt.notice(f'"{input_value}" is not a valid response', tag=False)
            continue
        if mode_number and mode_number <= len(mode_members):
            return mode_members[mode_number - 1]
        else:
            pt.notice(f'Please enter a valid mode number', tag=False)


def _validate_job_name(name: str) -> bool:
    """
    Checks if the given name is acceptable as a job name

    args:
        job_name: A string containing the name
        to be used for the current training job
    """

    acceptable_chars = ['_', '-']
    acceptable_chars += [str(i) for i in range(10)]
    if not name:
        return False
    for char in name:
        if char in acceptable_chars:
            continue
        elif not char.isalpha():
            return False
    return True


class FSItemBase(object):
    __slots__ = ['_path', '_name', '_id']

    def __init__(self, path: Union[str, Path]):
        path = path if isinstance(path, Path) else Path(path)
        self._path: Path = path.resolve()
        if not self._path.exists():
            raise RuntimeError(f'{self._path} does not exist.')
        self._name: str = self._path.name
        file_stat: stat_result = self._path.stat()
        self._id: int = hash(str(file_stat.st_ino) + str(file_stat.st_dev) + str(self._path))

    @property
    def name(self) -> str:
        return self._name

    @property
    def seconds_since_created(self) -> float:
        return self._path.stat().st_mtime

    @property
    def id(self) -> int:
        return self._id


class Checkpoint(FSItemBase):
    def __init__(self, path: Union[str, Path]):
        super(Checkpoint, self).__init__(path)
        if self._path.is_dir():
            raise IsADirectoryError(f'{self._path} is a directory.')

    @property
    def path(self) -> Path:
        return self._path


class Network(FSItemBase):
    def __init__(self, path: Union[str, Path]):
        super(Network, self).__init__(path)
        if self._path.is_dir():
            raise IsADirectoryError(f'{self._path} is a directory.')

    @property
    def path(self) -> Path:
        return self._path


class Job(FSItemBase):
    __slots__ = [
        '_checkpoint_dir',
        '_samples_dir',
        '_logs_dir',
        '_network_dir',
        '_inference_dir',
        '_input_data_path',
        '_selected_checkpoint',
        '_selected_network'
    ]
    _checkpoint_dir: Path
    _samples_dir: Path
    _logs_dir: Path
    _network_dir: Path
    _inference_dir: Path

    _input_data_path: Optional[Path]
    _selected_checkpoint: Optional[Checkpoint]
    _selected_network: Optional[Network]

    def __init__(self, path: Union[str, Path]):
        super(Job, self).__init__(path)
        if not self._path.is_dir():
            raise NotADirectoryError(f'{self._path} is not a directory.')
        self._checkpoint_dir = self._path.joinpath('checkpoints')
        self._samples_dir = self._path.joinpath('samples')
        self._logs_dir = self._path.joinpath('logs')
        self._network_dir = self._path.joinpath('networks')
        self._inference_dir = self._path.joinpath('inference')

        self._make_sub_dirs()
        self._input_data_path = None
        self._selected_checkpoint = None
        self._selected_network = None

    def _make_sub_dirs(self) -> None:
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self._samples_dir.mkdir(parents=True, exist_ok=True)
        self._logs_dir.mkdir(parents=True, exist_ok=True)
        self._network_dir.mkdir(parents=True, exist_ok=True)
        self._inference_dir.mkdir(parents=True, exist_ok=True)

    @property
    def dir(self) -> Path:
        return self._path

    @property
    def checkpoint_dir(self) -> Path:
        return self._checkpoint_dir

    @property
    def samples_dir(self) -> Path:
        return self._samples_dir

    @property
    def logs_dir(self) -> Path:
        return self._logs_dir

    @property
    def network_dir(self) -> Path:
        return self._network_dir

    @property
    def inference_dir(self) -> Path:
        return self._inference_dir

    @property
    def input_data_path(self) -> Path:
        return self._input_data_path

    @property
    def checkpoints(self) -> List[Checkpoint]:
        _checkpoints: List[Checkpoint] = []
        for checkpoint_dir in self._checkpoint_dir.iterdir():
            if not checkpoint_dir.stem.startswith('.'):
                checkpoint: Checkpoint = Checkpoint(checkpoint_dir)
                _checkpoints.append(checkpoint)
        # Sort by most recently modified using using timestamp
        return sorted(_checkpoints, key=lambda x: x.seconds_since_created, reverse=True)

    @property
    def networks(self) -> List[Network]:
        _networks: List[Network] = []
        for network_dir in self._network_dir.iterdir():
            if not network_dir.stem.startswith('.'):
                network: Network = Network(network_dir)
                _networks.append(network)
        # Sort by most recently modified using using timestamp
        return sorted(_networks, key=lambda x: x.seconds_since_created, reverse=True)

    @property
    def selected_checkpoint(self) -> Optional[Checkpoint]:
        return self._selected_checkpoint

    @selected_checkpoint.setter
    def selected_checkpoint(self, value: Checkpoint) -> None:
        did_match: bool = False
        for checkpoint in self.checkpoints:
            if value.id == checkpoint.id:
                did_match = True
        if not did_match:
            raise ValueError('Attempting to select checkpoint that is '
                             'not associated with this job. This is not'
                             'allowed.')
        self._selected_checkpoint = value

    @property
    def selected_network(self) -> Optional[Network]:
        return self._selected_network

    @selected_network.setter
    def selected_network(self, value: Network) -> None:
        did_match: bool = False
        for network in self.networks:
            if value.id == network.id:
                did_match = True
        if not did_match:
            raise ValueError('Attempting to select network that is '
                             'not associated with this job. This is not'
                             'allowed.')
        self._selected_network = value


def _list_jobs(jobs_dir: Path) -> Optional[List[Job]]:

    """
    Searches the jobs directory for existing jobs
    and returns them sorted by most recently used.
    """

    if not jobs_dir.exists():
        return

    jobs: List[Job] = []
    for job_dir in jobs_dir.iterdir():
        if not job_dir.stem.startswith('.'):
            job: Job = Job(job_dir)
            jobs.append(job)
    # Sort by most recently modified using timestamp
    if not jobs:
        return
    return sorted(jobs, key=lambda x: x.seconds_since_created, reverse=True)


def _create_job(name: str, jobs_dir: Path) -> Job:
    job_dir: Path = jobs_dir.joinpath(name)
    try:
        job_dir.mkdir()
    except FileExistsError:
        raise FileExistsError(f'A job titled {name} already exists, '
                              f'please try again')
    job = Job(job_dir)
    return job


class JobManager(object):
    """
    Handles the directory and file state of a training job.
    """

    __slots__ = [
        '_jobs_dir',
        '_active_job',
        '_run_mode',
        '_jobs',
    ]

    _jobs_dir: Path
    _active_job: Optional[Job]
    _run_mode: RunMode
    _jobs: List[Job]

    RunMode: Type[RunMode] = RunMode

    def __init__(self,
                 jobs_dir: Optional[Union[str, Path]] = None,
                 job_name: Optional[str] = None,
                 run_mode: Optional[RunMode] = None,
                 ignore_checkpoints: bool = False):
        if jobs_dir is None:
            self._jobs_dir = Path('./jobs/').resolve()
        else:
            self._jobs_dir = jobs_dir if isinstance(jobs_dir, Path) else Path(jobs_dir)
        if not self._jobs_dir.exists():
            makedirs(str(self._jobs_dir))
        elif not self._jobs_dir.is_dir():
            raise NotADirectoryError(f'{self._jobs_dir} is not a directory.')

        self._run_mode = run_mode if run_mode is not None else _query_mode()
        self._jobs = _list_jobs(self._jobs_dir)
        self._active_job = None
        if job_name is not None:
            self._setup_with_name(job_name, ignore_checkpoints)
        else:
            self._setup_with_prompt(ignore_checkpoints)

    def _setup_with_name(self, job_name: str, ignore_checkpoints: bool) -> None:
        # See if this job exists. If so, load it up.
        self._active_job = self.get_job(job_name)
        # Job doesn't exist. Try to create it. This will
        # raise if it's not a valid job name.
        if self._active_job is None:
            self._active_job = _create_job(job_name, self._jobs_dir)
        if not ignore_checkpoints:
            self._query_load_checkpoint()

    def _setup_with_prompt(self, ignore_checkpoints: bool) -> None:

        """
        Query user regarding the course of action they wish
        to take. They can choose to load an existing
        job, or create a new one.
        """

        if self._run_mode == RunMode.TRAIN:
            if self._jobs:
                # Query load existing job if jobs exist
                if _query_yes_no('Would you like to load an existing job?', default='no'):
                    self._query_load_job(message='Available jobs:', must_have_checkpoints=False)
                    if not ignore_checkpoints:
                        self._query_load_checkpoint()
                else:
                    self._query_create_job()
            else:
                self._query_create_job()
        elif self._run_mode == RunMode.INFERENCE:
            try:
                self._query_load_job('Available jobs:', must_have_networks=True)
            except JobNotAvailableError:
                pt.notice('There are no jobs available for performing inference')
                return
            self._query_load_network()
        else:
            raise ValueError(f'"{self._run_mode}" is not a valid run mode.')

    def _query_create_job(self) -> None:

        while True:
            job_name: str = _query_job_name()
            try:
                self._active_job = _create_job(job_name, self._jobs_dir)
                pt.success(f'Created new job titled: {job_name}')
                break
            except FileExistsError as e:
                pt.warn(e)

    def get_job(self, name: str) -> Optional[Job]:
        if self._jobs is not None:
            for job in self._jobs:
                if name == job.name:
                    return job

    @overload
    def _query_load_job(self, message: str):
        ...

    @overload
    def _query_load_job(self, message: str, must_have_checkpoints: bool = False):
        ...

    @overload
    def _query_load_job(self, message: str, must_have_networks: bool = False):
        ...

    def _query_load_job(self,
                        message: str,
                        must_have_checkpoints: bool = False,
                        must_have_networks: bool = False) -> None:

        """
        Queries the user to determine if they would
        like to load an existing job.
        """

        jobs: List[Job] = self._jobs
        # These two arguments should be given simultaneously. The
        # above overloads for this method should be followed.
        if must_have_checkpoints:
            jobs = [x for x in jobs if x.checkpoints]
        if must_have_networks:
            jobs = [x for x in jobs if x.networks]
        if not jobs:
            raise JobNotAvailableError
        stdout.write(message + '\n')
        for i, job in enumerate(jobs):
            pt.green(f'{i + 1}: {job.name}')
        while True:
            try:
                job_number: int = int(input('Please enter the number of the '
                                            'job you would like to load: '))
            except ValueError:
                continue
            if job_number and job_number <= len(jobs):
                job: Job = jobs[job_number - 1]
                self.active_job = job
                break
            else:
                pt.notice(f'Please enter a valid job number', tag=False)

    def _query_load_checkpoint(self) -> None:

        """
        Queries the user to determine if they would
        like to load an existing checkpoint.
        """

        if self.active_job is None:
            return
        checkpoints: List[Checkpoint] = self.active_job.checkpoints
        if not checkpoints:
            return
        stdout.write(f'Checkpoints for "{self.active_job.name}":\n')
        for i, checkpoint in enumerate(checkpoints):
            pt.green(f'{i + 1}: {checkpoint.name}')
        while True:
            try:
                checkpoint_number: int = int(input('Please enter the number of the '
                                                   'checkpoint you would like to load: '))
            except ValueError:
                continue
            if checkpoint_number and checkpoint_number <= len(checkpoints):
                checkpoint: Checkpoint = checkpoints[checkpoint_number - 1]
                self.active_job.selected_checkpoint = checkpoint
                break
            else:
                pt.notice(f'Please enter a valid checkpoint number')

    def _query_load_network(self) -> None:

        """
        Queries the user to determine if they would
        like to load an exported network.
        """

        if self.active_job is None:
            return
        networks: List[Network] = self.active_job.networks
        if not networks:
            return
        stdout.write(f'Networks for "{self.active_job.name}":\n')
        for i, network in enumerate(networks):
            pt.green(f'{i + 1}: {network.name}')
        while True:
            try:
                network_number: int = int(input('Please enter the number of the '
                                                'network you would like to load: '))
            except ValueError:
                continue
            if network_number and network_number <= len(networks):
                network: Network = networks[network_number - 1]
                self.active_job.selected_network = network
                break
            else:
                pt.notice(f'Please enter a valid network number')

    @property
    def jobs_dir(self) -> Path:
        return self._jobs_dir

    @property
    def active_job(self) -> Job:
        if self._active_job is None:
            raise ValueError('Found `None` when accessing active job.')
        return self._active_job

    @active_job.setter
    def active_job(self, value: Job) -> None:
        did_match: bool = False
        for job in self._jobs:
            if value.id == job.id:
                did_match = True
        if not did_match:
            raise ValueError('Attempting to select a job that is not associated '
                             'with this project. This is not allowed')
        self._active_job = value

    @property
    def run_mode(self) -> RunMode:
        return self._run_mode

    @property
    def jobs(self):
        return self._jobs
