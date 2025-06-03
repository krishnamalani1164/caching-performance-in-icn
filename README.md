# NDN Interest Flooding Attack Simulation

## 🎓 Research Internship Project
**Visvesvaraya National Institute of Technology (VNIT), Nagpur**  
*Computer Science & Engineering Department*

### 👨‍🎓 Research Intern Details
- **Institution**: VNIT Nagpur
- **Department**: Computer Science & Engineering
- **Research Area**: Named Data Networking (NDN) Security
- **Focus**: Interest Flooding Attack Detection and Mitigation

---

## 📋 Project Overview

This research project implements a comprehensive simulation framework for analyzing **Interest Flooding Attacks** in Named Data Networking (NDN) architectures. The simulation evaluates the impact of malicious subscribers on network performance across different caching policies and provides detailed analysis of attack mitigation strategies.

### 🎯 Research Objectives

1. **Simulate NDN Architecture**: Implement core NDN components (FIB, PIT, CS)
2. **Model Interest Flooding Attacks**: Create realistic attack scenarios with malicious subscribers
3. **Evaluate Caching Policies**: Compare LRU, LFU, FIFO, and MRU under attack conditions
4. **Performance Analysis**: Measure network degradation and defense effectiveness
5. **Visualization**: Generate comprehensive performance comparison graphs

---

## 🏗️ System Architecture

### Core Components

#### 1. **Network Nodes**
- **Router**: Implements NDN router with FIB, PIT, CS functionality
- **Publisher**: Content providers hosting image datasets
- **Subscriber**: Legitimate content consumers
- **MaliciousSubscriber**: Attack generators with configurable flooding rates

#### 2. **NDN Data Structures**
- **FIB (Forwarding Information Base)**: Routing table for content names
- **PIT (Pending Interest Table)**: Tracks outstanding Interest packets
- **CS (Content Store)**: In-network content cache with TTL support

#### 3. **Packet Types**
- **InterestPacket**: Content requests with unique nonces
- **DataPacket**: Content responses with actual data
- **NACK**: Negative acknowledgments for failed requests

---

## 🔬 Research Methodology

### Attack Simulation Framework

#### Interest Flooding Attack Model
```python
class MaliciousSubscriber(Subscriber):
    def __init__(self, name, attack_rate=150):
        # Configurable attack parameters
        self.attack_rate = attack_rate  # Interests per second
        self.attack_duration = configurable
        self.target_contents = random_selection
```

#### Performance Metrics
- **Cache Hit Ratio**: Percentage of requests served from cache
- **Network Latency**: Average response time under attack
- **Interest Drop Rate (IDR)**: Percentage of dropped Interest packets
- **NACK Rate**: Frequency of negative acknowledgments
- **Cache Eviction Rate**: Content replacement frequency

---

## 📊 Experimental Setup

### Network Configuration
- **Routers**: 3-10 configurable NDN routers
- **Publishers**: 2 content providers (cats/dogs image datasets)
- **Normal Subscribers**: 5-20 legitimate users
- **Attackers**: 4 malicious subscribers (150 interests/sec each)
- **Content**: 100 image files (50 cats + 50 dogs)

### Caching Policies Evaluated
1. **LRU (Least Recently Used)**: Evicts oldest accessed content
2. **LFU (Least Frequently Used)**: Evicts least popular content
3. **FIFO (First In, First Out)**: Evicts oldest cached content
4. **MRU (Most Recently Used)**: Evicts most recently accessed content

---

## 🚀 Installation & Usage

### Prerequisites
```bash
pip install networkx matplotlib pandas numpy
```

### Running the Simulation
```bash
python ndn_simulation.py
```

### Configuration Options
1. **Caching Policy**: Choose from LRU, LFU, FIFO, MRU
2. **Network Size**: Configure number of routers and subscribers
3. **Simulation Duration**: Set number of iterations
4. **Attack Parameters**: Modify attack rate and duration

---

## 📈 Results & Analysis

### Key Findings

#### 1. **Cache Hit Ratio Impact**
- **Without Attack**: 60-75% average hit ratio
- **With Attack**: 15-35% average hit ratio
- **Performance Degradation**: 40-60% reduction

#### 2. **Network Latency Analysis**
- **Baseline Latency**: 0.1-0.3 seconds
- **Under Attack**: 0.5-1.2 seconds
- **Latency Increase**: 3-4x degradation

#### 3. **Interest Drop Rate (IDR)**
- **Normal Conditions**: 0.5-3.0%
- **Attack Conditions**: 2.0-7.0%
- **Attack Impact**: 2-3x increase in packet drops

#### 4. **NACK Rate Comparison**
- **Normal Operations**: 0.3-1.8%
- **Under Attack**: 2.0-8.5%
- **Attack Amplification**: 4-5x increase

---

## 📁 Output Structure

```
Project/
├── Output/
│   ├── FIB/           # Forwarding Information Base logs
│   ├── PIT/           # Pending Interest Table logs
│   └── CS/            # Content Store logs
├── Simulation_Log/
│   ├── simulation_log.csv
│   ├── baseline_log.csv
│   └── network_performance_comparison.png
├── Logs/              # Detailed router logs
└── cats/dogs/         # Content datasets
```

---

## 🔧 Technical Implementation

### Advanced Features

#### 1. **Dynamic Content Management**
```python
class ContentIDManager:
    @classmethod
    def initialize_index(cls, publishers):
        # Global content indexing system
        # Unique ID assignment for efficient tracking
```

#### 2. **Multi-threaded Attack Simulation**
```python
def start_attack(self, contents, duration):
    self.attack_thread = threading.Thread(
        target=self._execute_attack,
        args=(self.connected_router,)
    )
    self.attack_thread.start()
```

#### 3. **Realistic Network Conditions**
- Packet loss simulation
- Congestion modeling
- TTL-based cache expiration
- Dynamic load balancing

---

## 📚 Research Contributions

### 1. **Comprehensive Attack Modeling**
- Realistic Interest flooding patterns
- Variable attack intensities
- Multi-attacker coordination

### 2. **Caching Policy Evaluation**
- Comparative analysis under attack conditions
- Performance trade-offs identification
- Optimization recommendations

### 3. **Visualization Framework**
- Real-time performance monitoring
- Comparative analysis graphs
- Network topology visualization

### 4. **Quantitative Analysis**
- Statistical performance metrics
- Attack impact quantification
- Defense effectiveness measurement

---

## 📖 Academic References

### NDN Security Research
- **Interest Flooding Attack Detection**: Advanced pattern recognition
- **Cache Poisoning Mitigation**: Content verification strategies
- **Network Resilience**: Distributed defense mechanisms

### Future Research Directions
1. **Machine Learning Integration**: AI-based attack detection
2. **Blockchain Security**: Decentralized content verification
3. **IoT Applications**: NDN security in edge computing
4. **Real-time Mitigation**: Adaptive defense strategies

---

## 🏆 Research Impact

### Academic Contributions
- **Novel Attack Simulation Framework**: Comprehensive NDN security testing
- **Performance Benchmarking**: Standardized evaluation metrics
- **Defense Strategy Analysis**: Comparative mitigation effectiveness

### Industry Applications
- **Network Security**: Enterprise NDN deployment guidelines
- **Performance Optimization**: Caching strategy recommendations
- **Attack Detection**: Real-time monitoring solutions

---

## 👥 Research Team

**Research Intern**: [Your Name]  
**Institution**: Visvesvaraya National Institute of Technology (VNIT), Nagpur  
**Supervisor**: [Supervisor Name]  
**Department**: Computer Science & Engineering  

---

## 📞 Contact Information

**Email**: [krishnamalani77@gmail.com] 

---

## 📄 License & Citation

### Academic Use
This research project is developed as part of academic research at VNIT Nagpur. 

### Citation Format
```
Krishna Malani. "NDN Interest Flooding Attack Simulation Framework." 
VNIT Nagpur, Computer Science & Engineering Department, 2024.
```

---

## 🔄 Version History

- **v1.0** (2024): Initial simulation framework
- **v1.1** (2024): Enhanced attack modeling
- **v1.2** (2024): Comprehensive visualization
- **v2.0** (2024): Multi-policy comparison analysis

---

**🎓 Developed during Research Internship at VNIT Nagpur**  
*Advancing NDN Security Research through Comprehensive Simulation*
