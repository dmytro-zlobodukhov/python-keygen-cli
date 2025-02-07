# Keygen CLI

A command-line interface (CLI) application for interacting with the Keygen.sh API.

## Table of Contents
  - [Motivation](#motivation)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Licenses](#licenses)
      - [Creating a License](#creating-a-license)
      - [Listing Licenses](#listing-licenses)
      - [Showing License Details](#showing-license-details)
      - [Checkout a License](#checkout-a-license)
      - [Deleting a License](#deleting-a-license)
    - [Groups](#groups)
      - [Listing Groups](#listing-groups)
    - [Packages](#packages)
      - [Listing Packages](#listing-packages)
    - [Releases](#releases)
      - [Listing Releases](#listing-releases)
    - [Artifacts](#artifacts)
      - [Listing Artifacts](#listing-artifacts)

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

Create a `.env` file in the root directory of the project with the following content (you can copy and edit the `.env.example` file):

```
KEYGEN_ACCOUNT_ID=your_account_id
KEYGEN_PRODUCT_TOKEN=your_product_token
```

Alternatively, you can set these environment variables directly in your shell:

```
# On Linux/macOS
export KEYGEN_ACCOUNT_ID=your_account_id
export KEYGEN_PRODUCT_TOKEN=your_product_token

# On Windows
$env:KEYGEN_ACCOUNT_ID="your_account_id"
$env:KEYGEN_PRODUCT_TOKEN="your_product_token"
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

Listing as a detailed table:
```
❯ kgsh licenses list -o wide

+------------+---------------+---------------+---------------------+---------------+----------------+
| Name       | Key           | License       | Email               | User Name     | Company Name   |
+============+===============+===============+=====================+===============+================+
| license1   | ABCD-ABCD-... | Trial         | user1@example.com   | Service User  | CompanyName1   |
+------------+---------------+---------------+---------------------+---------------+----------------+
| license2   | DBCD-DBCD-... | Trial         | user2@example.com   |               | CompanyName2   |
+------------+---------------+---------------+---------------------+---------------+----------------+
| license3   | EFGH-EFGH-... | Trial         |                     | Service User  | CompanyName3   |
+------------+---------------+---------------+---------------------+---------------+----------------+
```

Listing as a default table:
```
❯ kgsh licenses list

+------------+---------------+---------------+
| Name       | Key           | License       |
+============+===============+===============+
| license1   | ABCD-ABCD-... | Trial         |
+------------+---------------+---------------+
| license2   | DBCD-DBCD-... | Trial         |
+------------+---------------+---------------+
| license3   | EFGH-EFGH-... | Trial         |
+------------+---------------+---------------+
```

Listing as a text list:
```
❯ kgsh licenses list -o text

license1
license2
license3
```

Listing as a JSON:
```
❯ kgsh licenses list -o json

[
    {
        "name": "license1",
        "key": "ABCD-ABCD-ABCD-ABCD",
        "metadata": {
            "email": "email",
            "userName": "Service User",
            "companyName": "CompanyName1"
        }
    },
    {
        "name": "license2",
        "key": "DBCD-DBCD-DBCD-DBCD",
        "metadata": {
            "email": "email",
            "userName": "",
            "companyName": "CompanyName2"
        }
    },
    {
        "name": "license3",
        "key": "EFGH-EFGH-EFGH-EFGH",
        "metadata": {
            "email": "",
            "userName": "Service User",
            "companyName": "CompanyName3"
        }
    }
]
```

Listing as a CSV:
```
❯ kgsh licenses list -o csv

Name,Key,Email,User Name,Company Name
license1,ABCD-ABCD-ABCD-ABCD,email,Service User,CompanyName1
license2,DBCD-DBCD-DBCD-DBCD,email,,CompanyName2
license3,EFGH-EFGH-EFGH-EFGH,,Service User,CompanyName3
```

It will list all licenses in your account in a table/json/csv/text view, including metadata fields for better understanding of the licenses.

If the value is `None`, it will be displayed as empty.

### Showing License Details

To show details of a specific license (or you can set `-o text` explicitly):
```
❯ kgsh licenses show --name "license1"

Selected license:
  Name: license1
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email:
    userName: Service User
    companyName: CompanyName
    licenseType: Trial
```

Show details of a specific license in JSON:
```
❯ kgsh licenses show --name "license1" -o json

{
    "name": "license1",
    "id": "abcdabcd-abdc-abdc-abdc-abdcabdcabdc",
    "metadata": {
        "email": "",
        "userName": "Service User",
        "companyName": "CompanyName",
        "licenseType": "Trial"
    }
}
```

Or you can combine `show` and `list` commands:
```
❯ kgsh licenses show --name "$(kgsh licenses list -o text | grep license1)"

Selected license:
  Name: license1
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email:
    userName: Service User
    companyName: CompanyName
    licenseType: Trial
```

### Checkout a License

Action to check-out a license. This will generate a snapshot of the license at time of checkout, encoded into a license file certificate that can be decoded and used for licensing offline and air-gapped environments. 

To checkout a license:
```
❯ kgsh licenses checkout --name "license1"

Selected license:
  Name: license1
  ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc
  Metadata:
    email:
    userName: Service User
    companyName: CompanyName
    licenseType: Trial
License 'license1' (ID: abcdabcd-abdc-abdc-abdc-abdcabdcabdc) has been successfully checked out.
Certificate saved to: /home/user/python-keygen-cli/license1.lic
```

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

## Artifacts

### Listing Artifacts

List all artifacts:
```
❯ kgsh artifacts list

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package1-0.3.0-py3-none-any.whl  | 1bcdabcd-abdc-abdc-abdc-abdcabdcabdc | any          | linux      |        0.16 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package1-0.3.1-py3-none-any.whl  | 2bcdabcd-abdc-abdc-abdc-abdcabdcabdc | any          | linux      |        0.16 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package2-0.2.1-py3-none-any.whl  | 3bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package2-0.2.2-py3-none-any.whl  | 4bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.2-py3-none-any.whl  | 5bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | darwin     |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.3-py3-none-any.whl  | 6bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | darwin     |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.2-py3-none-any.whl  | 7bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | linux      |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.3-py3-none-any.whl  | 8bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | linux      |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.2-py3-none-any.whl  | 7bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | windows    |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.3-py3-none-any.whl  | 8bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | windows    |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
```

List artifacts by full or partial artifact name:
```
❯ kgsh artifacts list -n package1

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package1-0.3.0-py3-none-any.whl  | 1bcdabcd-abdc-abdc-abdc-abdcabdcabdc | any          | linux      |        0.16 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package1-0.3.1-py3-none-any.whl  | 2bcdabcd-abdc-abdc-abdc-abdcabdcabdc | any          | linux      |        0.16 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
```
List artifacts by full or partial version:
```
❯ kgsh artifacts list -v 0.2

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package2-0.2.1-py3-none-any.whl  | 3bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package2-0.2.2-py3-none-any.whl  | 4bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
```

List artifacts by full or partial platform:
```
❯ kgsh artifacts list -p windows

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package2-0.2.1-py3-none-any.whl  | 3bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package2-0.2.2-py3-none-any.whl  | 4bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.2-py3-none-any.whl  | 7bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | windows    |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package3-1.1.3-py3-none-any.whl  | 8bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | windows    |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+

```
List artifacts by full or partial architecture:
```
❯ kgsh artifacts list -a x86

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package2-0.2.1-py3-none-any.whl  | 3bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
| package2-0.2.2-py3-none-any.whl  | 4bcdabcd-abdc-abdc-abdc-abdcabdcabdc | x86_64       | windows    |        0.19 |
+----------------------------------+--------------------------------------+--------------+------------+-------------+

```
Or you can combine all these filters at once:
```
❯ kgsh artifacts list -n package3 -v 1.1.3 -p linux -a arm

+----------------------------------+--------------------------------------+--------------+------------+-------------+
| Name                             | ID                                   | Architecture | Platform   |   Size (MB) |
+==================================+======================================+==============+============+=============+
| package3-1.1.3-py3-none-any.whl  | 8bcdabcd-abdc-abdc-abdc-abdcabdcabdc | arm64        | linux      |        0.2  |
+----------------------------------+--------------------------------------+--------------+------------+-------------+
```
