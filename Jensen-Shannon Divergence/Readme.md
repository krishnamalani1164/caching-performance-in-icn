# Jensen-Shannon Divergence Implementation

## Overview

The Jensen-Shannon (JS) divergence is a method for measuring similarity between two probability distributions. It's a symmetric and smoothed version of the Kullback-Leibler (KL) divergence, making it more stable and interpretable for comparing distributions.

## Mathematical Definition

```
JS(P, Q) = 0.5 * KL(P || M) + 0.5 * KL(Q || M)
```

Where:
- `P` and `Q` are probability distributions
- `M = 0.5 * (P + Q)` is the average distribution
- `KL(P || Q)` is the Kullback-Leibler divergence

## Key Properties

- **Symmetric**: JS(P, Q) = JS(Q, P)
- **Bounded**: 0 ≤ JS(P, Q) ≤ log(2) ≈ 0.693
- **Finite**: Always produces finite values (unlike KL divergence)
- **Metric**: The square root of JS divergence satisfies triangle inequality

## Implementation Example

```python
import numpy as np

def kl_divergence(p, q, epsilon=1e-10):
    """Compute KL divergence with smoothing to avoid log(0)"""
    p = np.clip(p, epsilon, 1.0)
    q = np.clip(q, epsilon, 1.0)
    return np.sum(p * np.log(p / q))

def jensen_shannon_divergence(p, q):
    """Compute Jensen-Shannon divergence between two distributions"""
    p = np.array(p)
    q = np.array(q)
    
    # Normalize to ensure they're valid probability distributions
    p = p / np.sum(p)
    q = q / np.sum(q)
    
    # Compute average distribution
    m = 0.5 * (p + q)
    
    # Compute JS divergence
    js_div = 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)
    
    return js_div
```

## Usage

```python
# Example distributions
dist1 = [0.5, 0.3, 0.2]
dist2 = [0.4, 0.4, 0.2]

js_score = jensen_shannon_divergence(dist1, dist2)
print(f"JS Divergence: {js_score:.4f}")

# Convert to distance metric (0-1 range)
js_distance = np.sqrt(js_score)
print(f"JS Distance: {js_distance:.4f}")
```

## Applications

- **Text Analysis**: Comparing topic distributions in documents
- **Machine Learning**: Evaluating generative models (e.g., in GANs)
- **Bioinformatics**: Comparing DNA/protein sequence compositions
- **Image Processing**: Histogram comparison for image similarity

## Advantages over KL Divergence

1. **Symmetry**: Treats both distributions equally
2. **Numerical Stability**: No division by zero issues
3. **Bounded Output**: Easier to interpret and compare
4. **Smoothing Effect**: Less sensitive to small probability values

## Implementation Notes

- Always normalize input distributions to sum to 1
- Add small epsilon to avoid log(0) in KL divergence computation
- Consider using natural logarithm vs log base 2 depending on desired range
- For large datasets, consider vectorized implementations for efficiency
