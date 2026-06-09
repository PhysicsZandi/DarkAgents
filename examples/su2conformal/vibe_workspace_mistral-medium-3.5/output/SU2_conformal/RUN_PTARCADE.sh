#!/bin/bash
# PTArcade execution script for SU2_conformal model
# Run this from the vibe_workspace directory

echo "=== PTArcade Campaign for SU2_conformal ==="
echo "Starting at: $(date)"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/spectrum.py" ]; then
    echo "ERROR: Not in vibe_workspace directory"
    exit 1
fi

# Create output directory if needed
mkdir -p output/SU2_conformal/chains

# Run PTArcade
echo "Running PTArcade with N_samples = 100,000..."
echo "This may take 1-2 hours depending on hardware."
echo ""

ptarcade -m output/SU2_conformal/ptarcade_model.py \
         -c output/SU2_conformal/ptarcade_config.py

# Check if PTArcade succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "PTArcade completed successfully!"
    echo ""
    
    # Generate plots
    echo "Generating posterior plots..."
    python output/SU2_conformal/ptarcade_plot.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=== PTArcade Campaign Complete ==="
        echo "Output files:"
        echo "  - output/SU2_conformal/chains/ (MCMC chains)"
        echo "  - output/SU2_conformal/ptarcade_bayes.json (Bayesian estimates)"
        echo "  - output/SU2_conformal/ptarcade_summary.txt (text summary)"
        echo "  - output/SU2_conformal/SU2_conformal_posteriors.pdf (posterior plots)"
        echo ""
        echo "Next steps:"
        echo "  1. Update handoff_pta.json with ptarcade_analysis results"
        echo "  2. Proceed to constraint-agent and prior-agent"
    else
        echo "ERROR: Plot generation failed"
        exit 1
    fi
else
    echo "ERROR: PTArcade failed"
    exit 1
fi

echo "Finished at: $(date)"
