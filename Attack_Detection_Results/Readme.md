# Attack Detection Results Dataset

## Overview

This dataset contains the results of an Interest Flooding Attack (IFA) detection system analysis performed on network traffic data. The dataset provides interval-based analysis of network metrics and their corresponding attack classification results using statistical probability distributions and Hellinger distance measurements.

## Dataset Description

The analysis divides network traffic into time intervals and computes various network performance metrics along with their probability distributions to detect Interest Flooding Attacks in Named Data Networking (NDN) environments.

### File Information
- **Filename**: `attack_detection_results.csv`
- **Records**: 6 intervals analyzed
- **Classification**: All intervals classified as IFA_Attack
- **Detection Method**: Hellinger Distance with threshold-based classification

## Column Definitions

### Interval Identification
- **Interval**: Sequential interval number (1-6)
- **Start_Index**: Starting index of the time interval
- **End_Index**: Ending index of the time interval  
- **Records_in_Interval**: Number of data records within each interval

### Network Traffic Metrics (Averages)
- **Avg_Total_Requests**: Average number of total network requests per interval
- **Avg_Attack_Interests**: Average number of malicious interest packets per interval
- **Avg_Dropped_Packets**: Average number of dropped packets per interval
- **Avg_NACK_Sent**: Average number of Negative Acknowledgments sent per interval

### Probability Distributions
- **Probability_Total_Requests**: Normalized probability of total requests
- **Probability_Attack_Interests**: Normalized probability of attack interests
- **Probability_Dropped_Packets**: Normalized probability of dropped packets
- **Probability_NACK_Sent**: Normalized probability of NACK packets

### Detection Metrics
- **Hellinger_Distance**: Statistical distance measure between probability distributions (range: 0-1)
- **Classification**: Attack classification result (IFA_Attack/Normal)
- **Threshold**: Decision threshold for classification (0.25)

## Key Findings

### Attack Pattern Analysis
- **Attack Type**: Interest Flooding Attack (IFA) detected across all intervals
- **Attack Intensity**: High proportion of attack interests (89-94% of total requests)
- **Network Impact**: Consistent packet dropping and NACK generation patterns

### Statistical Characteristics
- **Hellinger Distance Range**: 0.549 - 0.569 (all above threshold)
- **Average Attack Interests**: 39.9 - 51.0 per interval
- **Average Total Requests**: 44.1 - 54.0 per interval
- **Detection Accuracy**: 100% attack detection (all intervals above threshold)

### Temporal Patterns
- **Consistent Attack**: Sustained attack pattern across all 6 intervals
- **Stable Metrics**: Relatively consistent network performance degradation
- **Threshold Effectiveness**: 0.25 threshold successfully identifies all attack intervals

## Technical Details

### Detection Algorithm
The detection system uses **Hellinger Distance** to measure the statistical divergence between:
- Normal network traffic probability distributions
- Observed traffic probability distributions

**Hellinger Distance Formula**:
```
H(P,Q) = (1/√2) * √(Σᵢ(√pᵢ - √qᵢ)²)
```

### Classification Logic
- **Attack Detected**: Hellinger Distance > Threshold (0.25)
- **Normal Traffic**: Hellinger Distance ≤ Threshold (0.25)

### Interest Flooding Attack (IFA)
IFA is a type of Denial of Service attack in NDN where:
- Attackers flood the network with excessive Interest packets
- Legitimate requests get dropped due to resource exhaustion
- Network performance degrades significantly

## Data Quality

### Completeness
- **Complete Dataset**: All intervals contain full metric calculations
- **No Missing Values**: All probability and distance measures computed
- **Consistent Structure**: Uniform data format across intervals

### Reliability Indicators
- **Probability Normalization**: All probabilities sum appropriately within intervals
- **Distance Bounds**: Hellinger distances within valid range [0,1]
- **Logical Consistency**: Attack metrics correlate with classification results

## Usage Applications

### Network Security
- **Attack Detection**: Real-time IFA detection in NDN networks
- **Security Monitoring**: Continuous network health assessment
- **Incident Response**: Attack pattern analysis and forensics

### Research Applications
- **Algorithm Validation**: Benchmark for attack detection algorithms
- **Performance Analysis**: Network behavior under attack conditions
- **Statistical Methods**: Hellinger distance effectiveness evaluation

### Machine Learning
- **Feature Engineering**: Network metrics as ML features
- **Classification Training**: Labeled attack/normal data for supervised learning
- **Anomaly Detection**: Statistical distribution analysis methods

## Data Interpretation Guidelines

### Normal vs Attack Traffic
- **Normal Traffic**: Hellinger Distance < 0.25, balanced request/response patterns
- **Attack Traffic**: Hellinger Distance > 0.25, high attack interest ratio

### Performance Impact Assessment
- **High Dropped Packets**: Indicates network congestion from attack
- **Increased NACKs**: Shows network's negative response to invalid requests
- **Attack Interest Ratio**: Proportion of malicious vs legitimate traffic

## Limitations

- **Single Attack Type**: Dataset only contains IFA attacks, no normal traffic baseline
- **Short Duration**: Limited to 6 intervals, may not capture long-term patterns
- **Binary Classification**: Only distinguishes attack vs normal, no attack severity levels
- **Threshold Dependency**: Fixed threshold may not generalize to different network conditions

## Future Extensions

- **Multi-Class Detection**: Expand to detect different attack types
- **Adaptive Thresholds**: Dynamic threshold adjustment based on network conditions
- **Temporal Analysis**: Include time-series analysis for attack evolution
- **Feature Enhancement**: Additional network metrics and behavioral indicators

---

**Note**: This dataset represents a controlled analysis of Interest Flooding Attacks in Named Data Networking environments. All intervals show consistent attack patterns, indicating a sustained attack scenario rather than mixed normal/attack traffic.
