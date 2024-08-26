import click
import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog

from .api import get_groups, get_policies, create_license, get_licenses

@click.group()
def cli():
    pass

@cli.group()
def licenses():
    pass

@licenses.command()
@click.option('--name', help='Name of the license')
@click.option('--policy', help='Name of the policy for the license')
@click.option('--group', help='Name of the group for the license')
def create(name, policy, group):
    if not name:
        name = prompt("Enter license name: ")

    if not policy:
        policies = get_policies()
        policy = radiolist_dialog(
            title="Select a policy",
            text="Choose a policy for the license (mandatory):",
            values=[(p['id'], p['attributes']['name']) for p in policies]
        ).run()
        
        if not policy:
            click.echo("Error: Policy selection is mandatory. Aborting license creation.")
            return
    else:
        # Find policy ID by name
        policies = get_policies()
        policy_id = next((p['id'] for p in policies if p['attributes']['name'] == policy), None)
        if not policy_id:
            click.echo(f"Error: Policy '{policy}' not found. Aborting license creation.")
            return
        policy = policy_id

    if not group:
        groups = get_groups()
        group = radiolist_dialog(
            title="Select a group",
            text="Choose a group for the license (optional, press Ctrl+C to skip):",
            values=[(g['id'], g['attributes']['name']) for g in groups]
        ).run()
        
        if not group:
            click.echo("Warning: No group selected. Proceeding without a group.")
    else:
        # Find group ID by name
        groups = get_groups()
        group_id = next((g['id'] for g in groups if g['attributes']['name'] == group), None)
        if not group_id:
            click.echo(f"Warning: Group '{group}' not found. Proceeding without a group.")
            group = None
        else:
            group = group_id

    # Ask for additional metadata
    email = prompt("Enter email (optional, press Enter to leave blank): ") or None
    user_name = prompt("Enter user name (optional, press Enter to leave blank): ") or None
    company_name = prompt("Enter company name (optional, press Enter to leave blank): ") or None

    metadata = {
        "email": email,
        "userName": user_name,
        "companyName": company_name
    }

    try:
        result = create_license(name, group, policy, metadata)
        click.echo("License created successfully:")
        click.echo(f"  Name: {result['attributes']['name']}")
        click.echo(f"  Key: {result['attributes']['key']}")
        click.echo(f"  ID: {result['id']}")
    except requests.exceptions.HTTPError as e:
        click.echo(f"Failed to create license: {e}")
        click.echo("Please check the error details above.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")

@licenses.command()
def list():
    licenses = get_licenses()
    if not licenses:
        click.echo("No licenses found.")
    else:
        click.echo("Licenses:")
        for license in licenses:
            click.echo(f"- ID: {license['id']}, Name: {license['attributes']['name']}")

def main():
    cli()

if __name__ == '__main__':
    main()