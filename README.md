# Keygen CLI

A command-line interface (CLI) application for interacting with the Keygen.sh API.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/keygen-cli.git
   cd keygen-cli
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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

## Usage

The CLI provides commands for managing licenses. Here are some examples:

### Creating a License

Basic usage:
```
kgsh licenses create
```
This will prompt you for the necessary information interactively.

You can also provide information via command-line options:
```
kgsh licenses create --name "My License" --policy "Standard Policy" --group "Test Group" --email "user@example.com" --user-name "John Doe" --company-name "ACME Inc."
```

Adding custom metadata fields:
```
kgsh licenses create --name "Custom License" --custom-field "department=Sales" --custom-field "role=Manager"
```

### Listing Licenses

```
kgsh licenses list
```

### Deleting a License

To delete a license:
```
kgsh licenses delete
```