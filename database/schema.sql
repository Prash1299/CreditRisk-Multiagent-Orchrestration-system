-- Logical schema (SQLAlchemy also creates these tables at startup).
-- PostgreSQL and SQLite are both supported via DATABASE_URL.

CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    segment VARCHAR(64),
    industry VARCHAR(64),
    monthly_income DOUBLE PRECISION,
    existing_emi DOUBLE PRECISION,
    collateral_value DOUBLE PRECISION,
    credit_score INTEGER,
    prior_defaults INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS loan_products (
    product_id VARCHAR(32) PRIMARY KEY,
    lender VARCHAR(120),
    name VARCHAR(160),
    product_type VARCHAR(32),
    min_amount DOUBLE PRECISION,
    max_amount DOUBLE PRECISION,
    min_tenure_months INTEGER,
    max_tenure_months INTEGER,
    rate_from DOUBLE PRECISION,
    rate_to DOUBLE PRECISION,
    min_credit_score INTEGER,
    max_foir DOUBLE PRECISION,
    processing_fee_pct DOUBLE PRECISION,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(64),
    request TEXT,
    disposition VARCHAR(32),
    risk_score DOUBLE PRECISION,
    rationale TEXT,
    payload_json TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interaction_memory (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(64),
    kind VARCHAR(32),
    content TEXT,
    created_at TIMESTAMP
);
