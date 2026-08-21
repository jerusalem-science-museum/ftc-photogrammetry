#!/bin/bash

# Define the parent folder path
PARENT_FOLDER="/mnt/shared_in/photogrammetry_data"
IMAGES_FOLDER="/mnt/shared_in/photogrammetry_images"

# Define the cleanup limits
AGE_THRESHOLD=14  # days
MIN_MODELS=30     # highest priority: never delete below this number
MAX_MODELS=60     # second priority: keep only this many newest models

# Define the log file path
LOG_FILE="/home/mada/delete_old_models_log.txt"

# Initialize the counter for deleted models
DELETED_COUNT=0

# Get the current date and time for logging
CURRENT_DATE=$(date "+%Y-%m-%d %H:%M:%S")

delete_model() {
    local model="$1"
    local folder_name
    local image_to_delete

    echo "Deleting model: $model"
    rm -rf "$model"
    ((DELETED_COUNT++))

    # Delete the matching gallery image if it exists.
    folder_name=$(basename "$model")
    image_to_delete="$IMAGES_FOLDER/$folder_name.png"
    if [ -f "$image_to_delete" ]; then
        echo "Deleting file: $image_to_delete"
        rm -f "$image_to_delete"
    fi
}

log_result() {
    if [ "$DELETED_COUNT" -gt 0 ]; then
        echo "$CURRENT_DATE - Deleted $DELETED_COUNT models" >> "$LOG_FILE"
    else
        echo "$CURRENT_DATE - No models deleted" >> "$LOG_FILE"
    fi
}

# Get models sorted by folder name. Timestamp names sort from oldest to newest.
mapfile -t MODELS < <(find "$PARENT_FOLDER" -mindepth 1 -maxdepth 1 -type d | sort)
TOTAL_MODELS=${#MODELS[@]}

# min_models has the highest priority: do not delete anything at or below it.
if [ "$TOTAL_MODELS" -le "$MIN_MODELS" ]; then
    echo "$CURRENT_DATE - $TOTAL_MODELS models found, minimum is $MIN_MODELS, skipping deletion" >> "$LOG_FILE"
    exit 0
fi

# max_models has second priority: delete oldest models until only MAX_MODELS remain.
if [ "$TOTAL_MODELS" -gt "$MAX_MODELS" ]; then
    MODELS_TO_DELETE=$((TOTAL_MODELS - MAX_MODELS))
    MAX_SAFE_DELETIONS=$((TOTAL_MODELS - MIN_MODELS))

    if [ "$MODELS_TO_DELETE" -gt "$MAX_SAFE_DELETIONS" ]; then
        MODELS_TO_DELETE="$MAX_SAFE_DELETIONS"
    fi

    for ((i = 0; i < MODELS_TO_DELETE; i++)); do
        delete_model "${MODELS[$i]}"
    done
fi

# Refresh the list after max-model cleanup before applying age cleanup.
mapfile -t MODELS < <(find "$PARENT_FOLDER" -mindepth 1 -maxdepth 1 -type d | sort)
TOTAL_MODELS=${#MODELS[@]}

# age_threshold has third priority: delete old models only while above MIN_MODELS.
if [ "$TOTAL_MODELS" -gt "$MIN_MODELS" ]; then
    for MODEL in "${MODELS[@]}"; do
        if [ "$TOTAL_MODELS" -le "$MIN_MODELS" ]; then
            break
        fi

        if [ -n "$(find "$MODEL" -maxdepth 0 -mtime +"$AGE_THRESHOLD")" ]; then
            delete_model "$MODEL"
            ((TOTAL_MODELS--))
        fi
    done
fi

log_result
