import argparse
import logging
import os
import shutil
import sys
import time
from pathlib import Path

import pandas as pd
from pyispace.example import save_opts
from pyispace.trace import trace_build_wrapper, make_summary, _empty_footprint  # noqa
from pyispace.utils import save_footprint, scriptcsv

from . import integrator, formatter
from .context import Configuration, Workspace
from .feature_selection import filtfeat
from .metrics import loss_threshold
from .visualization import Demo, AppClassification


_conf_file = 'config.yaml'


def main(args):
    start = time.time()
    logger = logging.getLogger(__name__)
    _my_path = Path().absolute()

    if args.other is None:
        config_path = _my_path / _conf_file
    else:
        config_path = args.other

    conf = Configuration(config_path).load()

    logger.info(f"Configuration file: '{str(config_path)}'")
    for name, path_str in conf.general.get_path_fields().items():
        if path_str is None:
            continue
        path = Path(path_str)
        if not path.is_absolute():
            abs_path = _my_path / path
            abs_path = abs_path.resolve()
            if abs_path.exists():
                conf.general.set(name, str(abs_path))
            else:
                logger.error("Invalid '{0}': '{1}'.".format(name, abs_path))
                sys.exit(1)

    file_path = Path(conf.general.datafile)
    if file_path.is_file():
        logger.info("Reading input dataset: '{0}'".format(file_path))
        df_dataset = pd.read_csv(file_path)
    else:
        logger.error("Invalid datafile '{0}'.".format(file_path))
        sys.exit(1)

    seed = conf.general.seed
    if isinstance(seed, int):
        os.environ["PYHARD_SEED"] = repr(seed)
        logger.info(f"Seed={seed}")
    else:
        os.environ["PYHARD_SEED"] = ""
        logger.info(f"Using random seed")

    rootdir_path = Path(conf.general.rootdir)
    problem = str.lower(conf.general.problem)
    if problem in {'classification', 'regression'}:
        logger.info(f"Type of problem: '{problem}'")
    else:
        logger.error(f"Unknown problem type '{problem}'.")
        sys.exit(1)

    if args.meta:
        logger.info("Building metadata.")

        df_metadata, df_ih = integrator.build_metadata(data=df_dataset,
                                                       config=conf,
                                                       return_ih=True,
                                                       verbose=args.verbose)
        df_metadata.to_csv(rootdir_path / 'metadata.csv')
        df_ih.to_csv(rootdir_path / 'ih.csv')
    else:
        df_metadata = pd.read_csv(rootdir_path / 'metadata.csv', index_col='instances')
        df_ih = pd.read_csv(rootdir_path / 'ih.csv', index_col='instances')

    if args.isa:
        if conf.fs.enabled:
            n_feat_cols = len(df_metadata.filter(regex='^feature_').columns)
            if n_feat_cols > conf.fs.max_n_features:
                logger.info("Feature selection on")
                logger.info(f"Chosen method: {conf.fs.method}")

                df_metadata.to_csv(rootdir_path / 'metadata_full.csv')

                df_features = df_metadata.filter(regex='^feature_')
                df_algo = df_metadata.filter(regex='^algo_')
                features = df_features.columns.to_list()

                fs_params = {**conf.fs.parameters, **{'standardize': False}}
                selected = filtfeat(
                    X=df_features.values,
                    Y=df_algo.values,
                    method=conf.fs.method,
                    max_n_features=conf.fs.max_n_features,
                    names=features,
                    **fs_params
                )

                if len(selected) < 3:
                    logger.warning(f"An insufficient number of features has been selected ({len(selected) < 3}). "
                                   f"An attempt with a pre-fixed number (10) of features to be selected will be made")
                    fs_params = {**fs_params, **{'n_features_to_select': 10}}
                    selected = filtfeat(
                        X=df_features.values,
                        Y=df_algo.values,
                        method=conf.fs.method,
                        max_n_features=conf.fs.max_n_features,
                        names=features,
                        **fs_params
                    )

                logger.info(f"Selected features: {selected}")

                df_metadata = pd.concat([df_features[selected], df_algo], axis=1)
                df_metadata.to_csv(rootdir_path / 'metadata.csv')
            else:
                logger.info("Skipping feature selection: "
                            "number of features already satisfied "
                            f"({n_feat_cols} <= max_n_features ({conf.fs.max_n_features}))")
        else:
            logger.info("Feature selection off")

        isa_engine = str.lower(conf.isa.engine)
        logger.info(f"Running Instance Space Analysis with {repr(isa_engine)} engine.")
        if isa_engine == 'python':
            # changes ISA 'perf':'epsilon' option
            epsilon = conf.isa.performance_threshold
            if epsilon == 'auto':
                n_classes = df_dataset.iloc[:, -1].nunique()
                epsilon = loss_threshold(n_classes, metric=conf.algos.metric)
            other = {'perf': {'epsilon': epsilon}}

            model = integrator.run_isa(rootdir=rootdir_path, metadata=df_metadata, settings=other,
                                       rotation_adjust=conf.isa.adjust_rotation, save_output=False)

            threshold = conf.isa.ih_threshold
            pi = conf.isa.ih_purity
            logger.info("Calculating instance hardness footprint area")
            logger.info(f"An instance is easy if its IH-value <= {threshold}")
            Ybin = df_ih.values[:, 0] <= threshold
            ih_fp = trace_build_wrapper(model.pilot.Z, Ybin, pi)

            # Calculate IH summary
            ih_summary = make_summary(space=model.trace.space, good=[ih_fp], best=[_empty_footprint()],
                                      algolabels=['instance_hardness'])
            model.trace.summary = model.trace.summary.append(ih_summary)

            # Save footprints and models
            save_footprint(ih_fp, rootdir_path, 'instance_hardness')
            scriptcsv(model, rootdir_path)
        elif isa_engine == 'matlab':
            _ = integrator.run_matilda(metadata=df_metadata, rootdir=conf.general.rootdir,
                                       matildadir=conf.general.matildadir)
        elif isa_engine == 'matlab_compiled':
            integrator.run_matilda_module(rootdir=rootdir_path)
        else:
            logger.error(f"Unknown ISA engine '{repr(isa_engine)}'.")
            sys.exit(1)

    if args.app:
        logging.getLogger().setLevel(logging.WARNING)

        workspace = Workspace(rootdir_path, file_path)
        workspace.load()

        if problem == 'classification':
            app = AppClassification(workspace)
        elif problem == 'regression':
            # app = AppRegression(workspace)
            raise NotImplementedError("Regression problems not yet supported. Coming soon!")
        app.show(port=5001, show=args.browser)  # noqa

    end = time.time()
    elapsed_time = end - start
    if elapsed_time < 60:
        logger.info(f"Total elapsed time: {elapsed_time:.1f}s")
    else:
        logger.info(
            f"Total elapsed time: {int(elapsed_time // 60)}m{int((elapsed_time / 60 - elapsed_time // 60) * 60)}s")
    logger.info("Instance Hardness analysis finished.")
    sys.exit(0)


def cli():
    parser = argparse.ArgumentParser(description="PyHard - Python Instance Hardness Framework. \n"
                                                 "If you find a bug, please open an issue in our repo: "
                                                 "https://gitlab.com/ita-ml/pyhard/-/issues")
    parser.add_argument('-F', '--files', dest='generate', action='store_true', default=False,
                        help="generate configuration files locally")
    parser.add_argument('--app', dest='app', action='store_true', default=False,
                        help="run app to visualize data")
    parser.add_argument('--demo', dest='demo', action='store_true', default=False,
                        help="run demo for toy datasets")
    parser.add_argument('--no-meta', dest='meta', action='store_false',
                        help="does not generate a new metadata file; uses previously saved instead")
    parser.add_argument('--no-isa', dest='isa', action='store_false',
                        help="does not execute the instance space analysis")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help="verbose mode")
    parser.add_argument('--no-browser', dest='browser', action='store_false', default=True,
                        help="run app without opening browser")
    parser.add_argument('-c', '--config', dest='other', default=None, required=False,
                        metavar='FILE', help="specifies a path to a config file other than default")

    args = parser.parse_args()
    print("run 'pyhard --help' to see all options.")

    sh = logging.StreamHandler()
    if args.verbose:
        sh.setLevel(logging.DEBUG)
    else:
        sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logging.getLogger().addHandler(sh)

    if args.demo:
        print("Press ^C to exit demo")
        demo = Demo()
        pane = demo.display()
        pane.servable()
        pane.show(title="Demo", port=5001, websocket_origin=['127.0.0.1:5001', 'localhost:5001'])  # threaded=True
    elif args.app:
        print("Press ^C to exit app")
        args.isa = False
        args.meta = False
        main(args)
    elif args.generate:
        src = Path(__file__).parent
        dest = Path().absolute()
        shutil.copy(src / f'conf/{_conf_file}', dest)
        save_opts(dest)
        print("Default config files generated!")
    else:
        logging.getLogger().setLevel(logging.INFO)
        main(args)
