from os import makedirs
from os.path import exists

import click
import click_spinner

from energinetml.core.model import TrainedModel
from energinetml.backend import default_backend as backend
from energinetml.settings import PACKAGE_VERSION, PACKAGE_NAME
from energinetml.settings import DEFAULT_RELATIV_LOG_FILENAME
from energinetml.settings import DEFAULT_RELATIV_ARTIFACT_PATH
from energinetml.cli.utils import discover_model

from energinetml.azure.logger import echo_logger

# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_model()
@click.argument('parameters', nargs=-1)
@click.option('--cloud-mode', '-c', 'cloud_mode',
              default=False, is_flag=True,
              help='Run training in cloud mode (do not use locally)')
@click.option('--force-download', '-f', 'force_download',
              default=False, is_flag=True,
              help='Force download of datasets (ignore locally cached files)')
@click.option('--seed', '-s',
              required=False, default=None, type=str,
              help='Seed value')
def train(parameters, cloud_mode, force_download, seed, model):
    """
    Train a model locally.
    \f

    :param list[str] parameters:
    :param bool cloud_mode:
    :param bool force_download:
    :param str seed:
    :param energinetml.Model model:
    """

    # -- init output log -----------------------------------------------------
    # TODO: How to make sure the folder exist before running the cmd?
    makedirs(DEFAULT_RELATIV_ARTIFACT_PATH, exist_ok=True)

    # wipe log file if it already exsists
    if exists(DEFAULT_RELATIV_LOG_FILENAME):
        open(DEFAULT_RELATIV_LOG_FILENAME, 'w').close()

    # -- Training context ----------------------------------------------------

    if cloud_mode:
        # Training is running in the cloud
        context = backend.get_cloud_training_context()
    else:
        # Training is running locally
        context = backend.get_local_training_context(force_download)

    # -- Train Parameters ----------------------------------------------------

    params = {}
    params.update(context.get_parameters(model))
    params.update(dict(param.split(':') for param in parameters))
    params['seed'] = seed \
        if seed is not None \
        else model.generate_seed()

    # -- Tags ----------------------------------------------------------------

    tags = {PACKAGE_NAME: str(PACKAGE_VERSION)}
    tags.update(params)
    tags.update(context.get_tags(model))
    tags.update(model.extra_tags())

    # -- Training ------------------------------------------------------------
    echo_logger('Training model...')

    try:
        trained_model = context.train_model(model=model, tags=tags, **params)
    except NotImplementedError:
        echo_logger('Training script needs an implementation!')
        echo_logger((
            'The train() method of your model raised a NotImplementedError '
            'which indicates that you have not yet implemented it.'
        ))
        echo_logger('Stacktrace follows:')
        echo_logger('-' * 79)
        raise

    # -- Verify returned object ----------------------------------------------

    echo_logger('-' * 79)
    echo_logger('Training complete')
    echo_logger('Verifying trained model...')

    # Must be of type TrainedModel
    if not isinstance(trained_model, TrainedModel):
        echo_logger('-' * 79)
        echo_logger((
            'The object returned by your train()-method must be of type '
            'TrainedModel (or inherited classes). You gave me something '
            'of type %s instead.'
        ) % str(type(trained_model)))
        raise click.Abort()

    # Verify object properties
    try:
        trained_model.verify()
    except trained_model.Invalid as e:
        echo_logger('-' * 79)
        echo_logger('%s does not validate: %s' % (
            trained_model.__class__.__name__, str(e)))
        raise click.Abort()

    # -- Dump output to disk -------------------------------------------------

    echo_logger('Dumping trained model to: %s' % model.trained_model_path)

    trained_model.params.update(params)
    trained_model.dump(model.trained_model_path)

    # -- Upload output files -------------------------------------------------

    echo_logger('Uploading output files...')

    with click_spinner.spinner():
        context.save_local_log()
        context.save_output_files(model)
    # -- Print portal link ---------------------------------------------------

    echo_logger('Portal link: %s' % context.get_portal_url())
