#!/bin/bash
# Master SDK Generation Script (XML + JSON + HTML)
# This script should be run from the ROOT of the project.
# Usage: ./scripts/generate_models.sh [version]

VERSION=${1:-"1.27"}
BASE_DIR="metadata/$VERSION"

if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Metadata directory '$BASE_DIR' not found."
    echo "Please create it and add: metadata_document.xml, service_document.json, service_layer_api_reference.html"
    exit 1
fi

# 0. Detect Real vs Vanilla Metadata
METADATA_XML="$BASE_DIR/metadata_document.xml"
SERVICE_JSON="$BASE_DIR/service_document.json"

if [ -f "$BASE_DIR/metadata_document.real.xml" ]; then
    echo "  - Using REAL metadata (detected .real.xml)"
    METADATA_XML="$BASE_DIR/metadata_document.real.xml"
fi

if [ -f "$BASE_DIR/service_document.real.json" ]; then
    echo "  - Using REAL service document (detected .real.json)"
    SERVICE_JSON="$BASE_DIR/service_document.real.json"
fi

echo "🚀 Starting Generation Pipeline for SAP B1 Version $VERSION..."

# 1. Generate/Refresh HTML Reference Cache
echo "  - Refreshing Reference Cache..."
uv run scripts/b1sl_metadata_generator/reference_parser.py \
    "$BASE_DIR/service_layer_api_reference.html" \
    "$BASE_DIR/reference_cache.json"

# 2. Run Main Generator with Triple-Source
echo "  - Running Core Generator..."
uv run -m scripts.b1sl_metadata_generator.generator \
    "$METADATA_XML" \
    src/b1sl/b1sl/models/_generated \
    --service-doc "$SERVICE_JSON" \
    --ref-cache "$BASE_DIR/reference_cache.json"

echo "✨ Done! SDK models and resources have been updated using SAP $VERSION metadata."