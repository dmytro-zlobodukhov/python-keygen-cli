# Keygen CLI

A command-line interface (CLI) application for interacting with the Keygen.sh API.

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
   pip install -e .
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