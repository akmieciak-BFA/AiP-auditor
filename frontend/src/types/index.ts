// Project types
export interface Project {
  id: number;
  name: string;
  client_name: string;
  status: 'step1' | 'step2' | 'step3' | 'step4' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  client_name: string;
}

// Step 1 types
export interface Step1Input {
  organization_data: any;  // Comprehensive initial assessment data
  questionnaire_answers: Record<string, any>;
  processes_list: string[];
}

export interface DigitalMaturity {
  process_maturity: number;
  digital_infrastructure: number;
  data_quality: number;
  organizational_readiness: number;
  financial_capacity: number;
  strategic_alignment: number;
  overall_score: number;
  interpretation: string;
}

export interface ProcessScoring {
  process_name: string;
  score: number;
  tier: number;
  rationale: string;
}

export interface QualityMetrics {
  is_valid: boolean;
  word_counts: Record<string, number>;
  warnings: string[];
}

export interface Step1Result {
  digital_maturity: DigitalMaturity;
  processes_scoring: ProcessScoring[];
  top_processes: string[];
  legal_analysis: string;
  system_dependencies: {
    systems: string[];
    matrix: number[][];
  };
  recommendations: string;
  bfa_scoring?: {
    automation_potential: number;
    business_impact: number;
    technical_feasibility: number;
    roi_potential: number;
    strategic_alignment: number;
    risk_level: number;
  };
  _quality_metrics?: QualityMetrics;
}

// Step 2 types
export interface ProcessStep {
  name: string;
  description: string;
  executor: string;
  system_used: string;
  duration_minutes: number;
  frequency: string;
  action_type: string;
}

export interface Step2ProcessData {
  basic_info: {
    name: string;
    department: string;
    process_owner: string;
    objective: string;
    scope: string;
  };
  as_is: {
    steps: ProcessStep[];
    total_cycle_time_hours: number;
    execution_frequency: string;
    annual_volume: number;
    fte_count: number;
  };
  costs: {
    labor_costs: number;
    operational_costs: number;
    error_costs: number;
    delay_costs: number;
  };
  problems: {
    problems: Array<{
      description: string;
      impact: string;
      annual_cost: number;
    }>;
  };
  systems: {
    systems_used: string[];
    integrations: string[];
    data_quality: string;
    technical_bottlenecks: string[];
  };
}

export interface Step2Result {
  muda_analysis: {
    defects: { description: string; cost_per_year: number };
    overproduction: { description: string; cost_per_year: number };
    waiting: { description: string; cost_per_year: number };
    non_utilized_talent: { description: string; cost_per_year: number };
    transportation: { description: string; cost_per_year: number };
    inventory: { description: string; cost_per_year: number };
    motion: { description: string; cost_per_year: number };
    extra_processing: { description: string; cost_per_year: number };
    total_waste_cost: number;
  };
  process_costs: {
    labor_costs: number;
    operational_costs: number;
    error_costs: number;
    delay_costs: number;
    total_cost: number;
  };
  bottlenecks: Array<{
    name: string;
    description: string;
    impact: string;
    cost_per_year: number;
  }>;
  automation_potential: {
    percentage: number;
    automatable_steps: string[];
    rationale: string;
  };
  bpmn_description: string;
  _quality_metrics?: QualityMetrics;
}

// Step 3 types
export interface Step3Input {
  budget_level: 'low' | 'medium' | 'high';
  tech_preferences?: Record<string, any>;
}

// Step 4 types
export interface Step4GenerateRequest {
  client_name: string;
  author_name: string;
  logo_url?: string;
  selected_processes: string[];
  budget_scenario: string;
  include_reports?: boolean;
}
