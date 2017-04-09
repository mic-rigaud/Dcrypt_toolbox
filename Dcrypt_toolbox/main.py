import os
import sys
import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix='DCRYPT_TOOLBOX')


class Context(object):

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'plugins'))


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('algo_'):
                rv.append(filename[5:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            print(name)
            mod = __import__('Dcrypt_toolbox.plugins.algo_' + name,
                             None, None, ['main'])
        except ImportError:
            return
        return mod.main





@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--fileIn', type=click.Path(exists=True, file_okay=False,
                                        resolve_path=True),
              help='Permet de choisir le fichier qui contient le texte chiffre.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def main(ctx, verbose, home):
    """
    Dcrypt_toolbox est une application qui permet de lancer des analyses cryptographique.
    Il est ainsi possible de faire du brute force sur des algorithmes simples tel que:
    Cesar, Vigenere, ...
    """
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home
