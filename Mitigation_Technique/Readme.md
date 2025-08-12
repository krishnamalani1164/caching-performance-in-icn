# iFLAT Algorithm Simulation

A Python implementation of the **iFLAT (Interest Flooding Attack mitigation using Trust-based approach)** algorithm for Named Data Networking (NDN) security.

## Overview

This project simulates the iFLAT algorithm, which provides defense against Interest Flooding Attacks (IFA) in NDN networks. The algorithm uses signal strength analysis, performance metrics, and collaborative detection to identify and mitigate fake Interest packets.

## Features

- **Signal Strength Analysis**: Uses received signal strength (RSS) to filter suspicious Interests
- **Performance-Based Forwarding**: Implements receive-to-transmit ratio thresholds
- **Collaborative Detection**: Maintains blacklists and fake Interest lists across network nodes
- **Producer-Side Detection**: Identifies flooding attempts at content producers
- **Warning System**: Generates and propagates warning messages for detected attacks

## Algorithm Components

The implementation includes three main algorithms:

1. **AfterReceiveInterest**: Handles incoming Interest packets at relay nodes
2. **BeforeSatisfyInterest**: Processes Data packets before satisfaction
3. **ProducerDetectionIFA**: Detects and responds to flooding attacks at producers


## Usage

### Basic Simulation

```python
from mitigation import *

# Create network components
incoming_face = Face("RelayNode1", power_dbm=12)
pit = PITEntry("Interest1")
meInfo = MeasurementInfo()

# Simulate Interest processing
AfterReceiveInterest(incoming_face, "Interest1", pit, meInfo)

# Simulate data satisfaction
BeforeSatisfyInterest("Interest1", False, meInfo)

# Simulate producer detection
ProducerDetectionIFA("FakeInterest1")
```

### Customizing Thresholds

```python
# Adjust RSS threshold (a) and ratio threshold (b)
AfterReceiveInterest(incoming_face, interest, pit, meInfo, a=15, b=3)
```

## Classes

### Core Components

- **`Face`**: Represents network interfaces with signal power measurements
- **`PITEntry`**: Manages Pending Interest Table entries
- **`FIBEntry`**: Handles Forwarding Information Base lookups
- **`MeasurementInfo`**: Tracks performance metrics (packet counts, ratios)

### Global Storage

- **`Blist`**: Blacklist for malicious prefixes
- **`Flist`**: List of identified fake Interests
- **`LocalStorage`**: Producer's content storage

## Algorithm Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `a` | 10 | RSS threshold (dBm) for Interest processing |
| `b` | 2 | Minimum receive-to-transmit ratio for forwarding |

## Example Output

```
[SEND_INTEREST] Sent Interest 'Interest1' via Face1
[SEND_INTEREST] Sent Interest 'Interest1' via Face2
[UPDATE] Data received for Interest1
[BLACKLIST] Added prefix FakeInterest1
[WARNING] WARNING: Fake Interest detected for FakeInterest1
```

## Network Operations

The simulation includes placeholder functions for actual NDN operations:

- `SEND_INTEREST()`: Forwards Interest packets
- `REPLY_WITH_NACK()`: Sends negative acknowledgments
- `SEND_DATA()`: Transmits Data packets
- `GENERATE_WARNING_DATA()`: Creates attack warnings

## Research Context

This implementation is based on research in NDN security, specifically addressing:

- Interest Flooding Attacks (IFA)
- Trust-based mitigation strategies
- Signal strength-based filtering
- Collaborative defense mechanisms

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- Named Data Networking (NDN) Project
- Interest Flooding Attack mitigation research
- Trust-based security approaches in NDN

## Contact

For questions or collaboration opportunities, please open an issue or contact the maintainers.

---

**Note**: This is a simulation implementation for research and educational purposes. For production NDN deployments, additional security considerations and optimizations would be required.
