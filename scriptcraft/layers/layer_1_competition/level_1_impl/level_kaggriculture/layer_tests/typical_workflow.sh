#!/bin/bash

#
# Kaggriculture: Typical Development Workflow
#
# This script automates the complete pipeline:
#
#   1. Validate project paths
#   2. Discover strategies from the strategy registry
#   3. Select strategy
#   4. Test selected strategy locally
#   5. Build submission for selected strategy
#   6. Inspect archive
#   7. Submit to Kaggle
#   8. Check submission status
#
# Strategy identity is owned by the Kaggriculture strategy registry.
#
# Usage:
#
#   bash typical_workflow.sh
#   bash typical_workflow.sh --no-submit
#   bash typical_workflow.sh --yes-all
#   bash typical_workflow.sh --strategy wheat
#   bash typical_workflow.sh --strategy melon_maxxer --no-submit
#

set -euo pipefail


# ============================================================================
# OUTPUT / COLOR CONFIGURATION
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'


# ============================================================================
# PATH CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

KAGGRICULTURE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LEVEL_1_IMPL_DIR="$(cd "$KAGGRICULTURE_DIR/.." && pwd)"
COMPETITION_DIR="$(cd "$LEVEL_1_IMPL_DIR/.." && pwd)"
LAYERS_DIR="$(cd "$COMPETITION_DIR/.." && pwd)"
SCRIPTCRAFT_DIR="$(cd "$LAYERS_DIR/.." && pwd)"
PYTHON_PACKAGE_DIR="$(cd "$SCRIPTCRAFT_DIR/.." && pwd)"
PYTHON_IMPLEMENTATIONS_DIR="$(cd "$PYTHON_PACKAGE_DIR/.." && pwd)"
IMPLEMENTATIONS_DIR="$(cd "$PYTHON_IMPLEMENTATIONS_DIR/.." && pwd)"
WORKSPACE_DIR="$(cd "$IMPLEMENTATIONS_DIR/.." && pwd)"


# ============================================================================
# KAGGRICULTURE TEST / BUILD FILES
# ============================================================================

LOCAL_TEST_MODULE="scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_tests.level_1.local_test"

BUILD_SCRIPT="$SCRIPT_DIR/level_0/build_submission.py"

REPLAY_FILE="$SCRIPT_DIR/replay.json"


# ============================================================================
# GENERATED OUTPUT
# ============================================================================

OUTPUT_ROOT="$WORKSPACE_DIR/workspace/output"
OUTPUT_DIR="$OUTPUT_ROOT/kaggriculture"

SUBMISSION_FILE="$OUTPUT_DIR/submission.tar.gz"


# ============================================================================
# FLAGS
# ============================================================================

INTERACTIVE=true
NO_SUBMIT=false
YES_ALL=false

STRATEGY_NAME=""


# ============================================================================
# ARGUMENT PARSING
# ============================================================================

while [[ $# -gt 0 ]]; do

    case "$1" in

        --strategy)
            if [[ $# -lt 2 ]]; then
                echo "Error: --strategy requires a strategy name."
                exit 1
            fi

            STRATEGY_NAME="$2"
            shift 2
            ;;

        --no-submit)
            NO_SUBMIT=true
            shift
            ;;

        --yes-all)
            YES_ALL=true
            INTERACTIVE=false
            shift
            ;;

        --help)
            echo "Usage: bash typical_workflow.sh [OPTIONS]"
            echo
            echo "Options:"
            echo "  --strategy NAME   Strategy registered in the Kaggriculture registry"
            echo "  --no-submit      Test & build but don't submit"
            echo "  --yes-all        Automate everything without prompts"
            echo "  --help           Show this help message"
            exit 0
            ;;

        *)
            echo "Unknown option: $1"
            echo "Use --help for usage."
            exit 1
            ;;

    esac

done


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}


success() {
    echo -e "${GREEN}[OK]${NC} $1"
}


warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}


error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}


prompt() {

    if [ "$YES_ALL" = true ]; then
        return 0
    fi

    local prompt_text="$1"
    local response

    read -p "$(echo -e ${YELLOW}[PROMPT]${NC} $prompt_text) (y/n) " -r response

    [[ "$response" =~ ^[Yy]$ ]]
}


# ============================================================================
# PATH VALIDATION
# ============================================================================

validate_paths() {

    info "Validating project paths..."

    if [ ! -d "$WORKSPACE_DIR" ]; then
        error "Workspace directory not found: $WORKSPACE_DIR"
    fi

    if [ ! -d "$PYTHON_PACKAGE_DIR" ]; then
        error "Python package directory not found: $PYTHON_PACKAGE_DIR"
    fi

    if [ ! -d "$SCRIPTCRAFT_DIR" ]; then
        error "ScriptCraft package directory not found: $SCRIPTCRAFT_DIR"
    fi

    if [ ! -d "$KAGGRICULTURE_DIR" ]; then
        error "Kaggriculture directory not found: $KAGGRICULTURE_DIR"
    fi

    if [ ! -f "$BUILD_SCRIPT" ]; then
        error "build_submission.py not found at $BUILD_SCRIPT"
    fi

    success "Project paths validated."
}


# ============================================================================
# STRATEGY REGISTRY
# ============================================================================

list_strategies() {

    cd "$SCRIPT_DIR"

    python -m "$LOCAL_TEST_MODULE" --list
}


validate_strategy() {

    local strategy="$1"

    cd "$SCRIPT_DIR"

    if ! python -m "$LOCAL_TEST_MODULE" "$strategy" \
        --opponent self \
        --steps 1 \
        --replay /dev/null \
        >/dev/null 2>&1; then

        error "Strategy '$strategy' is not registered."

    fi
}


# ============================================================================
# SELECT STRATEGY
# ============================================================================

select_strategy() {

    info "Available registered strategies..."
    echo

    list_strategies

    echo

    if [ -n "$STRATEGY_NAME" ]; then

        info "Strategy supplied by command line: $STRATEGY_NAME"

    elif [ "$YES_ALL" = true ]; then

        # Let the registry own the default.
        STRATEGY_NAME="$(python - <<'PY'
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    DEFAULT_STRATEGY,
)

print(DEFAULT_STRATEGY)
PY
)"

    else

        read -p "Enter strategy name (press Enter for registry default): " -r STRATEGY_NAME

        if [ -z "$STRATEGY_NAME" ]; then

            STRATEGY_NAME="$(python - <<'PY'
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    DEFAULT_STRATEGY,
)

print(DEFAULT_STRATEGY)
PY
)"

        fi

    fi

    info "Selected strategy: $STRATEGY_NAME"

    echo

    validate_strategy "$STRATEGY_NAME"

    success "Strategy '$STRATEGY_NAME' is registered."

    echo
}


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

main() {

    echo
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║      Kaggriculture: Development to Submission Workflow   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo

    # ========================================================================
    # STEP 1: PATH VALIDATION
    # ========================================================================

    info "STEP 1: Validating project paths..."
    echo

    validate_paths

    echo

    info "Workspace:       $WORKSPACE_DIR"
    info "Python package:  $PYTHON_PACKAGE_DIR"
    info "Kaggriculture:   $KAGGRICULTURE_DIR"
    info "Output:          $OUTPUT_DIR"

    echo


    # ========================================================================
    # STEP 2: STRATEGY REGISTRY / SELECTION
    # ========================================================================

    info "STEP 2: Discovering strategy registry..."
    echo

    select_strategy


    # ========================================================================
    # STEP 3: LOCAL TEST
    # ========================================================================

    info "STEP 3: Testing strategy '$STRATEGY_NAME' locally..."
    echo

    if prompt "Run local test against self?"; then

        cd "$SCRIPT_DIR"

        python -m "$LOCAL_TEST_MODULE" \
            "$STRATEGY_NAME" \
            --opponent self \
            --steps 720 \
            --replay "$REPLAY_FILE"

        success "Local test completed."
        success "Replay saved to: $REPLAY_FILE"

        echo

    else

        warn "Skipped local test."
        echo

    fi


    # ========================================================================
    # STEP 4: BUILD SUBMISSION
    # ========================================================================

    info "STEP 4: Building submission for strategy '$STRATEGY_NAME'..."
    echo

    mkdir -p "$OUTPUT_DIR"

    cd "$SCRIPT_DIR"

    python "$BUILD_SCRIPT" \
        --strategy "$STRATEGY_NAME"

    echo


    # ========================================================================
    # STEP 5: INSPECT ARCHIVE
    # ========================================================================

    if [ ! -f "$SUBMISSION_FILE" ]; then
        error "Submission archive not found: $SUBMISSION_FILE"
    fi

    success "Submission built: $SUBMISSION_FILE"

    echo

    info "STEP 5: Inspecting archive contents..."
    echo

    echo "Archive size: $(du -h "$SUBMISSION_FILE" | cut -f1)"
    echo "File count: $(tar -tzf "$SUBMISSION_FILE" | wc -l)"

    echo

    echo "Root files:"
    tar -tzf "$SUBMISSION_FILE" | grep -E '^[^/]+$' | head -10

    echo


    # ========================================================================
    # STEP 6: SUBMISSION DECISION
    # ========================================================================

    if [ "$NO_SUBMIT" = true ]; then

        success "Build complete. Skipping submission as requested."

        echo

        echo "Strategy:"
        echo "  $STRATEGY_NAME"

        echo

        echo "Submission archive:"
        echo "  $SUBMISSION_FILE"

        echo

        echo "To submit manually:"
        echo "  kaggle competitions submit kaggriculture \\"
        echo "    -f \"$SUBMISSION_FILE\" \\"
        echo "    -m \"${STRATEGY_NAME} submission\""

        echo

        exit 0

    fi


    echo

    if ! prompt "Submit strategy '$STRATEGY_NAME' to Kaggle?"; then

        warn "Submission cancelled by user."

        echo

        echo "To submit later:"
        echo "  kaggle competitions submit kaggriculture \\"
        echo "    -f \"$SUBMISSION_FILE\" \\"
        echo "    -m \"${STRATEGY_NAME} submission\""

        echo

        exit 0

    fi


    # ========================================================================
    # STEP 7: SUBMIT TO KAGGLE
    # ========================================================================

    info "STEP 7: Submitting strategy '$STRATEGY_NAME' to Kaggle..."
    echo

    if ! command -v kaggle &> /dev/null; then
        error "Kaggle CLI not found. Install with: pip install kaggle"
    fi

    TIMESTAMP="$(date +"%Y-%m-%d %H:%M:%S")"

    MESSAGE="$STRATEGY_NAME submission - $TIMESTAMP"

    kaggle competitions submit kaggriculture \
        -f "$SUBMISSION_FILE" \
        -m "$MESSAGE"

    success "Submission uploaded."

    echo


    # ========================================================================
    # STEP 8: CHECK SUBMISSION STATUS
    # ========================================================================

    info "STEP 8: Checking submission status..."
    echo

    if prompt "Check submission status?"; then

        kaggle competitions submissions kaggriculture | head -5

        echo

        success "Workflow complete!"

        echo

        echo "Strategy:"
        echo "  $STRATEGY_NAME"

        echo

        echo "Monitor your submission at:"
        echo "  https://www.kaggle.com/competitions/kaggriculture/submissions"

        echo

    fi
}


# ============================================================================
# RUN MAIN WORKFLOW
# ============================================================================

main