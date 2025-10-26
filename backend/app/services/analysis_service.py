from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import Project, Step1Data, Step2Process, Step3Data


class AnalysisService:
    """Service for aggregating and analyzing audit data."""
    
    @staticmethod
    def get_project_summary(db: Session, project_id: int) -> Dict[str, Any]:
        """Get complete project summary for presentation generation."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        # Get Step 1 results
        step1_data = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
        step1_results = step1_data.analysis_results if step1_data else {}
        
        # Get Step 2 results
        step2_processes = db.query(Step2Process).filter(Step2Process.project_id == project_id).all()
        step2_results = [
            {
                "process_name": p.process_name,
                "process_data": p.process_data,
                "analysis_results": p.analysis_results
            }
            for p in step2_processes
        ]
        
        # Get Step 3 results
        step3_data = db.query(Step3Data).filter(Step3Data.project_id == project_id).first()
        step3_results = step3_data.analysis_results if step3_data else {}
        
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "client_name": project.client_name,
                "status": project.status
            },
            "step1_results": step1_results,
            "step2_results": step2_results,
            "step3_results": step3_results
        }
    
    @staticmethod
    def calculate_total_savings(step2_results: List[Dict[str, Any]], step3_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate total potential savings across all processes."""
        total_current_cost = 0
        total_waste_cost = 0
        total_savings_potential = 0
        
        for process in step2_results:
            analysis = process.get("analysis_results", {})
            costs = analysis.get("process_costs", {})
            muda = analysis.get("muda_analysis", {})
            
            total_current_cost += costs.get("total_cost", 0)
            total_waste_cost += muda.get("total_waste_cost", 0)
        
        # Calculate savings from Step 3 scenarios
        scenarios = step3_results.get("scenarios", [])
        for scenario in scenarios:
            benefits = scenario.get("benefits_year1", {})
            total_savings_potential = max(total_savings_potential, benefits.get("total", 0))
        
        return {
            "total_current_cost": total_current_cost,
            "total_waste_cost": total_waste_cost,
            "total_savings_potential": total_savings_potential,
            "roi_potential": (total_savings_potential / total_current_cost * 100) if total_current_cost > 0 else 0
        }
