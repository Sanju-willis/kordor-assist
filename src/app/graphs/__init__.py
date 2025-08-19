# src\app\graphs\__init__.py
from app.graphs.home_graph import build_home_workflow
from app.graphs.analytics_graph import build_analytics_workflow
from app.graphs.social_graph import build_social_workflow


__all__ = [
    "build_home_workflow",
    "build_analytics_workflow",
    "build_social_workflow",
    
   
]
