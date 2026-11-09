CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    segment TEXT,
    industry TEXT,
    annual_income REAL,
    existing_debt REAL,
    collateral_value REAL,
    credit_score INTEGER,
    prior_defaults INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS loan_products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    term_months INTEGER,
    rate REAL,
    product_type TEXT
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrower_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    risk_score REAL,
    recommendation TEXT,
    rationale TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id),
    FOREIGN KEY (product_id) REFERENCES loan_products (product_id)
);
