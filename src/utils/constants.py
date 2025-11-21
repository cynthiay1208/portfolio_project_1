"""
Central constants used across the data pipeline.
"""

# -------------------------------------------------------------------
# Project Metadata
# -------------------------------------------------------------------

PROJECT_NAME = "Sales Reporting Data Pipeline"
PROJECT_VERSION = "0.1.0"

# -------------------------------------------------------------------
# File Handling Defaults
# -------------------------------------------------------------------

DEFAULT_ENCODING = "utf-8"
DEFAULT_SHEET = "Sheet1"

# -------------------------------------------------------------------
# YAML / JSON Config Locations
# -------------------------------------------------------------------

PATH_CONNECTIONS = "config/connections.yaml"
PATH_MODEL_MAP = "config/mappings/model_map.json"
PATH_DATE_RULES = "config/mappings/date_rules.json"
PATH_RETAILERS = "config/mappings/retailers.json"
PATH_INGESTION_LIST = "config/ingestion_list.yaml"

# (Phase 3 will add schema + validation constants)
