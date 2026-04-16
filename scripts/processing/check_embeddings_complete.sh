#!/bin/bash
# Check if embeddings generation is complete and send reminder

DB_COUNT=$(psql -U cbwinslow -d epstein -t -c "SELECT COUNT(*) FROM pages WHERE rtx3060_embedding IS NOT NULL;" 2>/dev/null | xargs)
TOTAL_COUNT=$(psql -U cbwinslow -d epstein -t -c "SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL;" 2>/dev/null | xargs)

if [ -z "$DB_COUNT" ] || [ -z "$TOTAL_COUNT" ]; then
    echo "Cannot connect to database"
    exit 1
fi

REMAINING=$((TOTAL_COUNT - DB_COUNT))
PERCENT=$(echo "scale=1; $DB_COUNT * 100 / $TOTAL_COUNT" | bc -l 2>/dev/null || echo "0")

echo "Embeddings Progress: $DB_COUNT / $TOTAL_COUNT ($PERCENT%) - $REMAINING remaining"

if [ "$REMAINING" -lt 100 ]; then
    echo ""
    echo "=========================================="
    echo "EMBEDDINGS GENERATION ESSENTIALLY COMPLETE!"
    echo "=========================================="
    echo "Time: $(date)"
    echo ""
    echo "ACTIONS REQUIRED:"
    echo "1. Stop the service: sudo systemctl stop epstein-embeddings"
    echo "2. Disable auto-start: sudo systemctl disable epstein-embeddings"
    echo "3. Create vector index for performance"
    echo ""
    echo "Check status: sudo systemctl status epstein-embeddings"
    echo "View logs: tail /tmp/rtx3060_embeddings.log"
    echo "=========================================="
    
    # Write completion files
    echo "Complete: $DB_COUNT embeddings generated at $(date)" > /tmp/EMBEDDINGS_COMPLETE_MARKER
    echo "Complete: $DB_COUNT embeddings generated at $(date)" > /home/cbwinslow/workspace/epstein/EMBEDDINGS_COMPLETE_MARKER
    
    exit 0
else
    echo "Still processing... $REMAINING pages remaining"
    exit 1
fi
