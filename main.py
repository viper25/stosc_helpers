import sys

import click
import subprocess
import tomllib


@click.command()
@click.option('--program',
              type=click.Choice(['1', 'Create Harvest Invoices', '3', '4']),
              prompt='Choose a program to run',
              help='Select a program to run.')
def main(program):
    secrets = load_secrets()

    python_executable = sys.executable  # Get the path to the current Python interpreter

    if program == '1':
        run_program1(python_executable, secrets['database'])
    elif program == '2':
        export_members(python_executable)
    elif program == '3':
        generate_contacts(python_executable)
    elif program == '4':
        compare_contacts(python_executable)
    else:
        click.echo('Invalid program selection.')


def load_secrets():
    # Create path to file with BASE_PATH and file name
    file = "config.toml"
    with open(file, "rb") as f:
        config = tomllib.load(f)
    return config


def run_program1(executable, secrets):
    arg1 = click.prompt('Enter argument 1', type=int)
    arg2 = click.prompt('Enter argument 2', type=str)
    # Call program 1 with the provided arguments and secrets
    subprocess.run(
        [executable, 'invoice_creation/hello.py', str(arg1), arg2, secrets['USER'], secrets['STOSC_DB_HOST']])


@click.command()
@click.argument('out', type=click.File('w'), default='-', required=False)
def export_members(out):
    click.echo("member List", file=out)


def generate_contacts(executable):
    subprocess.run([executable, 'utils\\generate_xero_contacts.py'])

def compare_contacts(executable):
    subprocess.run([executable, 'utils\\compare_email_and_address_xero_crm.py'])


if __name__ == '__main__':
    main()
