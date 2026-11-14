https://einternational-beige-hornet.fastmcp.app/mcp


# Expense Tracker MCP Server

An MCP (Model Context Protocol) server built with **FastMCP** that helps manage and summarize personal expenses using a PostgreSQL database.

## Features

- **Add expenses** with date, amount, category, subcategory, and note.
- **List expenses** within an inclusive date range.
- **Summarize expenses** by category within a date range, with an optional category filter.
- **Read expense categories** from a `categories.json` resource.

## Tech Stack

- Python
- FastMCP
- PostgreSQL
- Psycopg 3

## MCP Tools

| Tool | Description |
|---|---|
| `add_expense` | Adds a new expense record. |
| `list_expenses` | Lists expenses between `start_date` and `end_date` (inclusive). |
| `summarize` | Returns total expenses grouped by category for a date range. An optional `category` can filter the result. |

### Tool Parameters

**`add_expense`**
- `date`: Expense date, preferably `YYYY-MM-DD`.
- `amount`: Expense amount.
- `category`: Expense category.
- `subcategory`: Optional subcategory (default: empty string).
- `note`: Optional note (default: empty string).

**`list_expenses`**
- `start_date`: Start date in `YYYY-MM-DD` format.
- `end_date`: End date in `YYYY-MM-DD` format.

**`summarize`**
- `start_date`: Start date in `YYYY-MM-DD` format.
- `end_date`: End date in `YYYY-MM-DD` format.
- `category`: Optional category filter.

## MCP Resource

| Resource URI | Description |
|---|---|
| `expense://categories` | Returns the contents of `categories.json` as JSON. |

## Project Structure

```text
Expense-Tracker-MCP-Server/
├── main.py
├── categories.json
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Requirements

- Python version supported by the project's `.python-version` file.
- [uv](https://docs.astral.sh/uv/)
- A PostgreSQL database (for example, [Neon](https://neon.tech/)).

## Setup and Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Expense-Tracker-MCP-Server.git
cd Expense-Tracker-MCP-Server
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
uv sync
```

If the PostgreSQL driver is not already listed in `pyproject.toml`, add it with:

```bash
uv add "psycopg[binary]"
```

### 3. Configure the Database Connection

The server reads the PostgreSQL connection string from the `DATABASE_URL` environment variable. Do not hard-code database credentials in `main.py` or commit them to GitHub.

**PowerShell:**

```powershell
$env:DATABASE_URL = "postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require"
```

**macOS/Linux:**

```bash
export DATABASE_URL="postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require"
```

Replace the example value with your own PostgreSQL connection string.

### 4. Run the MCP Server

```bash
uv run python main.py
```

The server initializes the `expenses` table if it does not already exist, then starts the FastMCP server.

## Deployment

This project can be deployed through FastMCP Gateway / Prefect Horizon using a GitHub repository.

1. Push the project to GitHub.
2. Create or select a deployment connected to the repository and the `main` branch.
3. Set the deployment environment variable:
   - **Name:** `DATABASE_URL`
   - **Value:** Your PostgreSQL connection string.
4. Use `main.py:mcp` as the server entrypoint if the deployment setup asks for an entrypoint.
5. Deploy and inspect the deployment logs.

The deployment environment must have access to the PostgreSQL database. Keep the connection string private.

## Security

- Never commit `.env` files, database passwords, or secret connection strings.
- Keep `.env` in `.gitignore` if you use one for local development.
- Do not commit local SQLite database files such as `expenses.db`.
- If a database password is accidentally exposed, reset/rotate it in your database provider and update the deployment secret.

## Notes

- The `expenses` table is created automatically when the server starts, if it does not exist.
- The `categories.json` file must be present in the deployed project for the `expense://categories` resource to work.
- Existing data in a local SQLite database is not automatically copied to PostgreSQL. Migrate it separately if you need to preserve it.

## License

Add a license file and update this section if you choose to distribute the project under an open-source license.
