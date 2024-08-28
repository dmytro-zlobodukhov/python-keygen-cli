import click
import requests
import json

from prompt_toolkit import prompt
from tabulate import tabulate

from .utils import create_selection_dialog
from .api.licenses import create_license, get_licenses, delete_license
from .api.groups import get_groups
from .api.policies import get_policies
from .api.releases import get_releases, get_releases_by_name
from .api.packages import get_packages


# MARK: CLI - main
@click.group()
def cli():
    pass


# MARK: Licenses commands
@cli.group()
def licenses():
    pass


# MARK: Licenses commands - create
@licenses.command()
@click.option('-n', '--name', help='Name of the license')
@click.option('-p', '--policy', help='Name of the policy for the license')
@click.option('-g', '--group', help='Name of the group for the license')
@click.option('-e', '--email', help='Email for the license metadata')
@click.option('-u', '--user-name', help='User name for the license metadata')
@click.option('-c', '--company-name', help='Company name for the license metadata')
@click.option('--custom-field', help='Custom field for the license metadata (format: key=value)', multiple=True)
def create(name, policy, group, email, user_name, company_name, custom_field):
    if not name:
        name = prompt("Enter license name: ")

    # Check if a license with the same name already exists
    existing_licenses = get_licenses()
    if any(license['attributes']['name'] == name for license in existing_licenses):
        click.echo(f"Error: A license with the name '{name}' already exists.")
        click.echo("Please choose a different name or use a unique identifier.")
        return

    if not policy:
        policies = get_policies()
        policy = create_selection_dialog(
            "Select a policy:",
            [(p['id'], p['attributes']['name']) for p in policies],
            allow_abort=True
        )
        
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
        group_options = [(g['id'], g['attributes']['name']) for g in groups]
        group_options.append((None, "No group"))
        group = create_selection_dialog(
            "Select a group (or 'No group' to proceed without a group):",
            group_options,
            allow_abort=True
        )
        
        if group is None:
            click.echo("Proceeding without a group.")
    else:
        # Find group ID by name
        groups = get_groups()
        group_id = next((g['id'] for g in groups if g['attributes']['name'] == group), None)
        if not group_id:
            click.echo(f"Warning: Group '{group}' not found. Proceeding without a group.")
            group = None
        else:
            group = group_id

    # Metadata collection
    metadata = {}
    
    if not email:
        email = prompt("Enter email (optional, press Enter to leave blank): ") or None
    if email:
        metadata['email'] = email

    if not user_name:
        user_name = prompt("Enter user name (optional, press Enter to leave blank): ") or None
    if user_name:
        metadata['userName'] = user_name

    if not company_name:
        company_name = prompt("Enter company name (optional, press Enter to leave blank): ") or None
    if company_name:
        metadata['companyName'] = company_name

    # Process custom fields
    for field in custom_field:
        try:
            key, value = field.split('=', 1)
            metadata[key.strip()] = value.strip()
        except ValueError:
            click.echo(f"Warning: Ignoring invalid custom field format: {field}")

    try:
        result = create_license(name, group, policy, metadata)
        click.echo("License created successfully:")
        click.echo(f"  Name: {result['attributes']['name']}")
        click.echo(f"  Key: {result['attributes']['key']}")
        click.echo(f"  ID: {result['id']}")
        click.echo("  Metadata:")
        for key, value in result['attributes'].get('metadata', {}).items():
            click.echo(f"    {key}: {value}")
    except requests.exceptions.HTTPError as e:
        click.echo(f"Failed to create license: {e}")
        click.echo("Please check the error details above.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")


# MARK: Licenses commands - list
@licenses.command()
def list():
    licenses = get_licenses()
    if not licenses:
        click.echo("No licenses found.")
    else:
        table_data = []
        headers = ["Name", "Key", "Email", "User Name", "Company Name"]
        
        for license in licenses:
            name = license['attributes']['name']
            key = license['attributes']['key'][:10] + "..."  # First 10 chars + ...
            metadata = license['attributes'].get('metadata', {})
            email = metadata.get('email', '')
            user_name = metadata.get('userName', '')
            company_name = metadata.get('companyName', '')
            
            table_data.append([name, key, email, user_name, company_name])
        
        # Sort the table data by license name (first column)
        table_data.sort(key=lambda x: x[0].lower())
        
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


# MARK: Licenses commands - delete
@licenses.command()
@click.option('--name', help='Name of the license to delete')
@click.option('-f', '--force', is_flag=True, help='Force deletion without confirmation')
def delete(name, force):
    licenses = get_licenses()
    if not licenses:
        click.echo("No licenses found.")
        return

    if name:
        # Find the license by name
        selected_license_data = next((license for license in licenses if license['attributes']['name'] == name), None)
        if not selected_license_data:
            click.echo(f"No license found with the name '{name}'.")
            return
    else:
        # If no name provided, use the selection dialog
        license_options = [(license['id'], f"{license['attributes']['name']} ({license['id']})") for license in licenses]
        selected_license = create_selection_dialog(
            "Select a license to delete:",
            license_options,
            allow_abort=True
        )

        if selected_license is None:
            click.echo("License deletion aborted.")
            return

        selected_license_data = next(license for license in licenses if license['id'] == selected_license)

    license_name = selected_license_data['attributes']['name']
    license_id = selected_license_data['id']
    metadata = selected_license_data['attributes'].get('metadata', {})

    click.echo(f"\nSelected license:")
    click.echo(f"  Name: {license_name}")
    click.echo(f"  ID: {license_id}")
    click.echo("  Metadata:")
    for key, value in metadata.items():
        click.echo(f"    {key}: {value}")

    if not force:
        confirm = click.confirm("\nAre you sure you want to delete this license?", default=False)
    else:
        confirm = True

    if confirm:
        try:
            if delete_license(license_id):
                click.echo(f"License '{license_name}' (ID: {license_id}) has been successfully deleted.")
            else:
                click.echo(f"Failed to delete license '{license_name}' (ID: {license_id}). The API request was successful, but the license may not have been deleted.")
        except requests.exceptions.HTTPError as e:
            click.echo(f"Failed to delete license: {e}")
            click.echo("Please check the error details above.")
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}")
    else:
        click.echo("License deletion cancelled.")


# MARK: Groups commands
@cli.group()
def groups():
    pass


# MARK: Groups commands - list
@groups.command()
def list():
    groups = get_groups()
    if not groups:
        click.echo("No groups found.")
        return  # Exit early if no groups found
    else:
        # Format the groups data for tabulation
        formatted_groups = [[group['attributes']['name'], group['id']] for group in groups]
        click.echo(tabulate(formatted_groups, headers=["Name", "ID"], tablefmt="grid"))


# MARK: Releases commands
@cli.group()
def releases():
    pass


# MARK: Releases commands - list
@releases.command()
@click.option('-n', '--name', help='Name of the release (partial match)')
def list(name=None):
    releases = get_releases()
    
    if not releases:
        click.echo("No releases found.")
        return

    if name:
        filtered_releases = [
            release for release in releases
            if name.lower() in release['attributes']['name'].lower()
        ]
        if not filtered_releases:
            click.echo(f"No releases found containing '{name}'.")
            return
        releases = filtered_releases

    table_data = []
    headers = ["Name", "Version", "Id"]

    for release in releases:
        release_name = release['attributes']['name']
        version = release['attributes']['version']
        id = release['id']

        table_data.append([release_name, version, id])

    # Sort the table data by release version (second column)
    table_data.sort(key=lambda x: x[1].lower())

    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


# MARK: Packages commands
@cli.group()
def packages():
    pass

# MARK: Packages commands - list
@packages.command()
def list():
    packages = get_packages()
    if not packages:
        click.echo("No packages found.")
        return

    table_data = []
    headers = ["Name", "ID", "Engine", "Platform"]

    for package in packages:
        name = package['attributes'].get('name', 'N/A')
        id = package['id']
        engine = package['attributes'].get('engine', 'N/A')
        platform = package['attributes'].get('platform', 'N/A')

        table_data.append([name, id, engine, platform])

    # Sort the table data by package name (first column)
    table_data.sort(key=lambda x: x[0].lower())

    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


# MARK: Main
def main():
    cli()


if __name__ == '__main__':
    main()