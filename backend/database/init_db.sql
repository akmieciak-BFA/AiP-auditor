-- Database Initialization Script for BFA Audit App
-- ================================================

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_industry ON projects(industry);

-- Create calculation_results table
CREATE TABLE IF NOT EXISTS calculation_results (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    module_name VARCHAR(50) NOT NULL,
    scenario_type VARCHAR(50),
    inputs JSONB NOT NULL,
    outputs JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_calc_results_project ON calculation_results(project_id);
CREATE INDEX idx_calc_results_module ON calculation_results(module_name);
CREATE INDEX idx_calc_results_project_module ON calculation_results(project_id, module_name);
CREATE INDEX idx_calc_results_created ON calculation_results(created_at);

-- Create industry_benchmarks table
CREATE TABLE IF NOT EXISTS industry_benchmarks (
    id SERIAL PRIMARY KEY,
    industry VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(50),
    source VARCHAR(200),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    UNIQUE(industry, metric_name, date)
);

CREATE INDEX idx_benchmarks_industry ON industry_benchmarks(industry);
CREATE INDEX idx_benchmarks_metric ON industry_benchmarks(metric_name);
CREATE INDEX idx_benchmarks_industry_metric ON industry_benchmarks(industry, metric_name);

-- Create maturity_assessments table
CREATE TABLE IF NOT EXISTS maturity_assessments (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    overall_score FLOAT NOT NULL,
    maturity_level INTEGER NOT NULL,
    dimension_scores JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_maturity_project ON maturity_assessments(project_id);

-- Create scenario_analyses table
CREATE TABLE IF NOT EXISTS scenario_analyses (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    scenario_type VARCHAR(50) NOT NULL,
    financial_metrics JSONB NOT NULL,
    sensitivity_analysis JSONB,
    monte_carlo_results JSONB,
    recommendation JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scenarios_project ON scenario_analyses(project_id);

-- Create audit_step1_data table
CREATE TABLE IF NOT EXISTS audit_step1_data (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_step1_project ON audit_step1_data(project_id);

-- Create audit_step2_data table
CREATE TABLE IF NOT EXISTS audit_step2_data (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_step2_project ON audit_step2_data(project_id);

-- Insert sample industry benchmarks
INSERT INTO industry_benchmarks (industry, metric_name, value, unit, source) VALUES
('manufacturing', 'avg_roi', 25.0, 'percent', 'Industry Survey 2024'),
('manufacturing', 'avg_payback_months', 18.0, 'months', 'Industry Survey 2024'),
('manufacturing', 'automation_adoption_rate', 45.0, 'percent', 'Industry Survey 2024'),
('financial_services', 'avg_roi', 35.0, 'percent', 'Industry Survey 2024'),
('financial_services', 'avg_payback_months', 12.0, 'months', 'Industry Survey 2024'),
('financial_services', 'automation_adoption_rate', 60.0, 'percent', 'Industry Survey 2024'),
('healthcare', 'avg_roi', 30.0, 'percent', 'Industry Survey 2024'),
('healthcare', 'avg_payback_months', 15.0, 'months', 'Industry Survey 2024'),
('healthcare', 'automation_adoption_rate', 35.0, 'percent', 'Industry Survey 2024'),
('logistics', 'avg_roi', 28.0, 'percent', 'Industry Survey 2024'),
('logistics', 'avg_payback_months', 16.0, 'months', 'Industry Survey 2024'),
('logistics', 'automation_adoption_rate', 50.0, 'percent', 'Industry Survey 2024'),
('retail', 'avg_roi', 32.0, 'percent', 'Industry Survey 2024'),
('retail', 'avg_payback_months', 14.0, 'months', 'Industry Survey 2024'),
('retail', 'automation_adoption_rate', 55.0, 'percent', 'Industry Survey 2024')
ON CONFLICT (industry, metric_name, date) DO NOTHING;
