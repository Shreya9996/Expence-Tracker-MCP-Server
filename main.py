from fastmcp import FastMCP
import os
import psycopg
from psycopg.rows import dict_row

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

# Read the connection string from the cloud environment
DATABASE_URL = os.environ["DATABASE_URL"]

mcp = FastMCP("ExpenseTracker")


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id BIGSERIAL PRIMARY KEY,
                date TEXT NOT NULL,
                amount DOUBLE PRECISION NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)


init_db()


@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """Add a new expense entry to the database."""

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO expenses
            (date, amount, category, subcategory, note)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (date, amount, category, subcategory, note),
        )

        expense_id = cur.fetchone()["id"]

        return {"status": "ok", "id": expense_id}


@mcp.tool()
def list_expenses(start_date, end_date):
    """List expense entries within an inclusive date range."""

    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN %s AND %s
            ORDER BY id ASC
            """,
            (start_date, end_date),
        )

        return cur.fetchall()


@mcp.tool()
def summarize(start_date, end_date, category=None):
    """Summarize expenses by category within an inclusive date range."""

    query = """
        SELECT category, SUM(amount) AS total_amount
        FROM expenses
        WHERE date BETWEEN %s AND %s
    """

    params = [start_date, end_date]

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " GROUP BY category ORDER BY category ASC"

    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()


@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """Return expense categories from categories.json."""

    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
