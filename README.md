# Keygen CLI

A command-line interface (CLI) application for interacting with the Keygen.sh API.

p.s. This application was developed in a hurry with help of Cursor AI for research purposes.

## Motivation

Keygen.sh is a powerful platform for managing software licenses and digital assets. While it offers a comprehensive API, there was a need for a more user-friendly tool to interact with this API, especially for non-technical users and for handling different operations.

Key motivations for creating this CLI tool:

1. Simplify License Management: Creating and managing licenses through a web interface can be time-consuming, especially when dealing with multiple licenses for demos and customers.

2. Reduce Human Error: Manual license creation is prone to mistakes. An automated CLI tool helps minimize these errors.

3. Improve Efficiency: Our development team needed a quick and reliable way to create trial licenses. The existing solutions were not flexible or convenient enough.

4. User-Friendly Interface: This CLI is designed with interactivity in mind, making it accessible for both technical and non-technical users.

5. Flexibility and Customization: Unlike our previous solution, this CLI is easy to modify and extend, allowing us to adapt it to our changing needs.

6. Ability to quickly take a glance at the licenses, groups, packages, releases, and more.

By addressing these needs, this CLI tool streamlines our license management process, making it more efficient, reliable, and user-friendly for our entire team.

p.s. This tool is not perfect and is not intended to replace the web interface. It is a simple tool to help with common tasks.

## Installation

1. Clone this repository and navigate to it (it is `python-keygen-cli` directory by default):
   ```
   cd python-keygen-cli
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the package:
   ```
   pip install -e ".[dev]"
   ```

## Configuration

Create a `.env` file in the root directory of the project with the following content:

```
KEYGEN_ACCOUNT_ID=your_account_id
KEYGEN_PRODUCT_TOKEN=your_product_token
```

Replace `your_account_id` and `your_product_token` with your actual Keygen.sh account ID and product token.

# Usage

The CLI provides commands for managing licenses. Here are some examples:

## Licenses

### Creating a License

This will prompt you for the necessary information interactively. Use the arrow keys to select options and press Enter to confirm.
```
❯ kgsh licenses create

Enter license name: asdasd

Select a policy:
▸ policy1
  policy2
  (Press 'q' to abort)

Select a group (or 'No group' to proceed without a group):
  group1
  group2
  group3
▸ No group
  (Press 'q' to abort)

Proceeding without a group.
Enter email (optional, press Enter to leave blank): 
Enter user name (optional, press Enter to leave blank): 
Enter company name (optional, press Enter to leave blank): 
License created successfully:
  Name: asdasd
  Key: <here will be the license key>
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: None
    userName: None
    companyName: None
```

You can also provide information via command-line options (policy `--policy` and group `--group` are mandatory and must exist in your Keygen account):
```
❯ kgsh licenses create --name "My-License-1" --policy "Standard-Policy" --group "Test-Group" --email "user@example.com" --user-name "John Doe" --company-name "ACME Inc."

License created successfully:
  Name: My-License-1
  Key: <here will be the license key>
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: user@example.com
    userName: John Doe
    companyName: ACME Inc.
```
Or even shorter (policy `-p` and group `-g` are mandatory and must exist in your Keygen account):
```
❯ kgsh licenses create -n "My-License-2" -p "Standard-Policy" -g "Test-Group" -e "user@example.com" -u "John Doe" -c "ACME Inc."

License created successfully:
  Name: My-License-2
  Key: <here will be the license key>
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: user@example.com
    userName: John Doe
    companyName: ACME Inc.
```
Metadata fields can be added or can be skipped. If skipped, all values in metadata will be set to `None`.


If you try to create a license with the same name, you will get an error:
```
❯ kgsh licenses create --name asdasd

Error: A license with the name 'asdasd' already exists.
Please choose a different name or use a unique identifier.
```

You can even add additional custom metadata fields (not tested yet):
```
❯ kgsh licenses create --name "Custom-License" --custom-field "department=Sales" --custom-field "role=Manager"
```

### Listing Licenses

```
❯ kgsh licenses list

+------------+---------------+---------------------+---------------+----------------+
| Name       | Key           | Email               | User Name     | Company Name   |
+============+===============+=====================+===============+================+
| license1   | ABCD-ABCD-... | user1@example.com   | Service User  | CompanyName1   |
+------------+---------------+---------------------+---------------+----------------+
| license2   | DBCD-DBCD-... | user2@example.com   |               | CompanyName2   |
+------------+---------------+---------------------+---------------+----------------+
| license3   | EFGH-EFGH-... |                     | Service User  | CompanyName3   |
+------------+---------------+---------------------+---------------+----------------+
```
It will list all licenses in your account in a table view, including metadata fields for better understanding of the licenses.

If the value is `None`, it will be displayed as empty.

### Deleting a License

To delete a license:
```
❯ kgsh licenses delete

Select a license to delete:
▸ license1 (abcdabcd-abdc-abdc-abdc-abdcabdcabdc)
  license2 (abcdabcd-abdc-abdc-abdc-abdcabdcabdc)

Selected license:
  Name: license1
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: user1@example.com
    userName: Service User
    companyName: CompanyName

Are you sure you want to delete this license? [y/N]: y
```

Delete specific license by name:
```
❯ kgsh licenses delete --name "license1"

Selected license:
  Name: license1
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: user1@example.com
    userName: Service User
    companyName: CompanyName

Are you sure you want to delete this license? [y/N]: y
```

It will list all the licenses in your account, you will need to select the license you want to delete.

After selecting the license, it will ask you to confirm the deletion.

Warning: This will actually delete the license from your account.

Or you can delete license without configmation by setting `-f` or `--force` flag:
```
❯ kgsh licenses delete --name asdasd -f                                                     

Selected license:
  Name: asdasd
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email: None
    userName: None
    companyName: None
License 'asdasd' (ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc) has been successfully deleted.
```

## Groups

### Listing Groups

```
❯ kgsh groups list

+---------+--------------------------------------+
| Name    | ID                                   |
+=========+======================================+
| group1  | abcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+---------+--------------------------------------+
| group2  | abcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+---------+--------------------------------------+
```

## Packages

### Listing Packages

```
❯ kgsh packages list

+-----------+--------------------------------------+----------+------------+
| Name      | ID                                   | Engine   | Platform   |
+===========+======================================+==========+============+
| package1  | abcdabcd-abdc-abdc-abdc-abdcabdcabdc | pypi     | N/A        |
+-----------+--------------------------------------+----------+------------+
| package2  | bbcdabcd-abdc-abdc-abdc-abdcabdcabdc | pypi     | N/A        |
+-----------+--------------------------------------+----------+------------+
| package3  | cbcdabcd-abdc-abdc-abdc-abdcabdcabdc | pypi     | N/A        |
+-----------+--------------------------------------+----------+------------+
```

## Releases

### Listing Releases

List all releases:
```
❯ kgsh releases list

+------------------+------------+--------------------------------------+
| Name             | Version    | Id                                   |
+==================+============+======================================+
| cool-release1    | 1.2.13     | 1bcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+------------------+------------+--------------------------------------+
| awesome-release2 | 2.4.8      | 2bcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+------------------+------------+--------------------------------------+
```

List releases by full release name:
```
❯ kgsh releases list -n cool-release1

+------------------+------------+--------------------------------------+
| Name             | Version    | Id                                   |
+==================+============+======================================+
| cool-release1    | 1.2.13     | 1bcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+------------------+------------+--------------------------------------+
```

List releases by part of release name:
```
❯ kgsh releases list -n cool

+------------------+------------+--------------------------------------+
| Name             | Version    | Id                                   |
+==================+============+======================================+
| cool-release1    | 1.2.13     | 1bcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+------------------+------------+--------------------------------------+

❯ kgsh releases list -n awesome

+------------------+------------+--------------------------------------+
| Name             | Version    | Id                                   |
+==================+============+======================================+
| awesome-release2 | 2.4.8      | 2bcdabcd-abdc-abdc-abdc-abdcabdcabdc |
+------------------+------------+--------------------------------------+
```
