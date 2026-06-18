-- ==========================================
-- AI Website Audit Tool Database
-- MySQL 8+
-- ==========================================

CREATE DATABASE IF NOT EXISTS website_audit_tool;

USE website_audit_tool;

-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE users
ADD COLUMN role VARCHAR(20) DEFAULT 'client';

ALTER TABLE users
ADD COLUMN is_active INTEGER DEFAULT 1;


-- =====================================
-- USER SETTINGS TABLE
-- =====================================

CREATE TABLE user_settings (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    theme VARCHAR(20) DEFAULT 'light',

    report_format VARCHAR(20) DEFAULT 'pdf',

    default_url VARCHAR(500),

    email_notifications BOOLEAN DEFAULT TRUE,

    weekly_summary BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ==========================================
-- AUDITS TABLE
-- ==========================================

CREATE TABLE audits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    website_url VARCHAR(500) NOT NULL,

    seo_score INT DEFAULT 0,
    performance_score INT DEFAULT 0,
    accessibility_score INT DEFAULT 0,
    security_score INT DEFAULT 0,
    mobile_score INT DEFAULT 0,

    overall_score INT DEFAULT 0,

    audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

ALTER TABLE audits
ADD COLUMN summary TEXT NULL;

ALTER TABLE audits
ADD COLUMN grade VARCHAR(10) NULL;


ALTER TABLE audits
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE audits
ADD COLUMN accessibility_metrics JSON;

ALTER TABLE audits
ADD COLUMN security_metrics JSON;

ALTER TABLE audits
ADD COLUMN mobile_metrics JSON;

ALTER TABLE audits
ADD COLUMN screenshot_path TEXT;

ALTER TABLE audits
ADD COLUMN recommendations JSON;

-- ==========================================
-- FINDINGS TABLE
-- ==========================================

CREATE TABLE findings (
    id INT AUTO_INCREMENT PRIMARY KEY,

    audit_id INT NOT NULL,

    category VARCHAR(100) NOT NULL,
    severity ENUM(
        'Critical',
        'High',
        'Medium',
        'Low'
    ) NOT NULL,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    recommendation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (audit_id)
        REFERENCES audits(id)
        ON DELETE CASCADE
);

ALTER TABLE findings
ADD COLUMN issue TEXT;

ALTER TABLE findings
ADD COLUMN priority VARCHAR(20);

ALTER TABLE findings
ADD COLUMN benefit TEXT;

-- ==========================================
-- REPORTS TABLE
-- ==========================================

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,

    audit_id INT NOT NULL,

    report_type VARCHAR(50) DEFAULT 'PDF',

    file_path VARCHAR(500),

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (audit_id)
        REFERENCES audits(id)
        ON DELETE CASCADE
);

-- ==========================================
-- INDEXES
-- ==========================================

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_audits_user
ON audits(user_id);

CREATE INDEX idx_findings_audit
ON findings(audit_id);

CREATE INDEX idx_reports_audit
ON reports(audit_id);