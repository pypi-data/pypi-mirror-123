from dataclasses import asdict, dataclass, field, fields
from typing import Union, List


@dataclass
class GeneralConfig:
    rootdir: str
    datafile: str
    matildadir: str = None
    problem: str = 'classification'
    target_col: str = None
    seed: int = 0

    def get_path_fields(self):
        return {'rootdir': self.rootdir, 'datafile': self.datafile, 'matildadir': self.matildadir}

    def set(self, name, value):
        setattr(self, name, value)


@dataclass(frozen=True)
class MeasuresConfig:
    list: List[str]


@dataclass(frozen=True)
class AlgorithmsConfig:
    pool: List[str]
    parameters: field(default_factory=dict)
    n_folds: int = 5
    n_iter: int = 1
    metric: str = 'logloss'


@dataclass(frozen=True)
class ISAConfig:
    engine: str = 'python'
    performance_threshold: Union[float, str] = 'auto'
    adjust_rotation: bool = True
    ih_threshold: float = 0.4
    ih_purity: float = 0.55


@dataclass(frozen=True)
class FSConfig:
    enabled: bool = True
    max_n_features: int = 10
    method: str = 'NCA'
    parameters: dict = field(default_factory=dict)
    variance_filter: bool = False
    variance_threshold: float = 0


@dataclass(frozen=True)
class HPOConfig:
    enabled: bool = True
    evals: int = 20
    timeout: int = 90


@dataclass(frozen=True)
class Configurations:
    general: GeneralConfig
    measures: MeasuresConfig
    algos: AlgorithmsConfig
    isa: ISAConfig
    fs: FSConfig
    hpo: HPOConfig

    def to_dict(self) -> dict:
        return asdict(self)


def from_dict(d: dict):
    config_sections = {f.name: f.type(**d[f.name]) for f in fields(Configurations)}
    return Configurations(**config_sections)


def from_old_format(d_old: dict):
    """
    Convenient method to map old configuration file fields into expected ones. It will be deprecated in future.
    """
    general = GeneralConfig(
        rootdir=d_old['rootdir'],
        matildadir=d_old.get('matildadir'),
        datafile=d_old['datafile'],
        problem=d_old.get('problem'),
        target_col=d_old.get('labels_col'),
        seed=d_old.get('seed'),
    )

    measures = MeasuresConfig(
        list=d_old.get('measures_list')
    )

    algos = AlgorithmsConfig(
        pool=d_old['algo_list'],
        parameters=d_old.get('parameters'),
        n_folds=d_old.get('n_folds'),
        n_iter=d_old.get('n_iter'),
        metric=d_old.get('metric')
    )

    isa = ISAConfig(
        engine=d_old.get('isa_engine'),
        performance_threshold=d_old.get('perf_threshold'),
        adjust_rotation=d_old.get('adjust_rotation'),
        ih_threshold=d_old.get('ih_threshold'),
        ih_purity=d_old.get('ih_purity')
    )

    fs = FSConfig(
        enabled=d_old.get('feat_select'),
        max_n_features=d_old.get('max_n_features'),
        method='IT',
        parameters=dict(criteria=d_old.get('method')),
        variance_filter=d_old.get('var_filter'),
        variance_threshold=d_old.get('var_threshold')
    )

    hpo = HPOConfig(
        enabled=d_old.get('hyper_param_optm'),
        evals=d_old.get('hpo_evals'),
        timeout=d_old.get('hpo_timeout')
    )

    return Configurations(
        general=general,
        measures=measures,
        algos=algos,
        isa=isa,
        fs=fs,
        hpo=hpo
    )
