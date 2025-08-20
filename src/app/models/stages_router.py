# src\app\models\stages_router.py
from typing import Dict, List
from app.models import ModuleEnum


def derive_stage_for_module(module: str, context: dict) -> str:
    if module == ModuleEnum.HOME.value:
        return derive_home_stage(context)
    if module == ModuleEnum.SOCIAL.value:
        return derive_social_stage(context)
    if module == ModuleEnum.ANALYTICS.value:
        return derive_analytics_stage(context)
    return "onboarding"


HOME_STAGE_STEPS: Dict[str, List[str]] = {
    "onboarding_company": ["fill_basic_info", "fill_brand_data"],
    "onboarding_products": [
        "add_product_basic_data",
        "add_target_customers",
        "add_competitors",
    ],
    "onboarding_integrations": ["connect_social_platforms"],
    "onboarding_completed": [],
}


def derive_home_stage(context: dict) -> str:
    if not context.get("stage_initialized"):
        return "onboarding"
    if context.get("integrations", {}).get("connected"):
        return "onboarding_completed"
    if context.get("product", {}).get("completed"):
        return "onboarding_integrations"
    if context.get("company", {}).get("completed"):
        return "onboarding_products"
    return "onboarding_company"  # default for fresh signups


def get_home_steps(stage: str) -> List[str]:
    return HOME_STAGE_STEPS.get(stage, [])


ANALYTICS_STAGE_STEPS: Dict[str, List[str]] = {
    "analytics_ready": ["verify_connection", "pull_summary"],
    "analytics_active": ["select_dashboard", "fetch_metrics", "answer_questions"],
}


def derive_analytics_stage(context: dict) -> str:
    # dumb rule: connection -> active, else ready
    if context.get("analytics", {}).get("connected"):
        return "analytics_active"
    return "analytics_ready"


def get_analytics_steps(stage: str) -> List[str]:
    return ANALYTICS_STAGE_STEPS.get(stage, [])


SOCIAL_STAGE_STEPS: Dict[str, List[str]] = {
    "social_ready": ["verify_tokens", "fetch_pages"],
    "social_active": ["sync_or_publish"],
}


def derive_social_stage(context: dict) -> str:
    # dumb rule: tokens -> active, else ready
    if context.get("social", {}).get("tokens_ok"):
        return "social_active"
    return "social_ready"


def get_social_steps(stage: str) -> List[str]:
    return SOCIAL_STAGE_STEPS.get(stage, [])
