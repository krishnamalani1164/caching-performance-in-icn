# NDN Cache Policy Simulation

A comprehensive Named Data Networking (NDN) simulation framework that implements and compares different caching policies in content-centric networks. This project simulates content distribution, caching strategies, and network performance metrics across multiple routers, publishers, and subscribers.

## 🚀 Features

- **Multiple Caching Policies**: LRU, LFU, FIFO, MRU
- **Network Topology Visualization**: Interactive network graphs
- **Performance Metrics**: Cache hit ratio, latency, hop reduction
- **Data Persistence**: Save/load network configurations
- **Comprehensive Logging**: Detailed event tracking and statistics
- **Visual Analytics**: Policy comparison charts and performance graphs

## 🏗️ Architecture

### Core Components

- **Node**: Base class for all network entities
- **Router**: Implements caching policies with FIB, PIT, and CS
- **Publisher**: Content providers with image repositories
- **Subscriber**: Content consumers that generate requests
- **ContentIDManager**: Manages unique content identification

### Network Elements

- **FIB (Forwarding Information Base)**: Routing table for content names
- **PIT (Pending Interest Table)**: Tracks outstanding requests
- **CS (Content Store)**: Cache storage with configurable policies

## 📋 Requirements

```python
networkx
matplotlib
pandas
pickle
csv
collections
datetime
random
os
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ndn-cache-simulation.git
cd ndn-cache-simulation
```

2. Install required packages:
```bash
pip install networkx matplotlib pandas
```

3. Create content directories:
```bash
mkdir cats dogs
# Add image files to these directories
```

## 🎯 Usage

### Basic Simulation

```python
python main.py
```

The program will guide you through:
1. Network setup (routers, subscribers count)
2. Content request simulation parameters
3. Automatic policy comparison and visualization

### Network Configuration

- **Routers**: Configurable number with chain topology
- **Publishers**: Two publishers (cats, dogs) with 50 images each
- **Subscribers**: Configurable number, distributed across routers
- **Cache Size**: 15 items per router (configurable)

### Caching Policies

| Policy | Description | Eviction Strategy |
|--------|-------------|-------------------|
| **LRU** | Least Recently Used | Remove oldest accessed item |
| **LFU** | Least Frequently Used | Remove least accessed item |
| **FIFO** | First In First Out | Remove first cached item |
| **MRU** | Most Recently Used | Remove most recently accessed item |

## 📊 Output Files

### Directory Structure
```
├── Output/
│   ├── FIB/          # Forwarding Information Base
│   ├── PIT/          # Pending Interest Table
│   └── CS/           # Content Store snapshots
├── Logs/             # Event logs per router
├── Policy_Stats/     # Individual policy statistics
├── Simulation_Results/ # Combined policy comparison
└── Saved_Network/    # Network configuration persistence
```

### Generated Files

- **FIB Tables**: `fib.csv` - Content name to next-hop mappings
- **PIT Tables**: `pit.csv` - Outstanding interest tracking
- **Content Store**: `cs.csv` - Current cache contents
- **Policy Statistics**: `{policy}_stats.csv` - Performance metrics
- **Comparison Results**: `policy_comparison.csv` - Cross-policy analysis

## 📈 Performance Metrics

### Key Metrics Tracked

- **Cache Hit Ratio**: Percentage of requests served from cache
- **Latency**: Average response time per request
- **Hop Reduction**: Network traversal optimization
- **Content Popularity**: Request frequency distribution
- **Cache Evictions**: Memory management efficiency

### Visualization

- Network topology graphs
- Policy performance comparison charts
- Time-series analysis of metrics
- Merged policy comparison views

## 🔧 Configuration

### Router Settings
```python
CACHE_LIMIT = 15  # Maximum cache size
TTL = 5  # Content Time-To-Live (minutes)
```

### Simulation Parameters
```python
active_prob = 0.9  # Subscriber activity probability
content_range = 100  # Total available content items
```

## 📝 Code Example

```python
# Create network components
routers = [Router(f'Router{i}') for i in range(1, num_routers + 1)]
publishers = [Publisher('Publisher1', 'cats'), Publisher('Publisher2', 'dogs')]
subscribers = [Subscriber(f'Subscriber{i}') for i in range(1, num_subscribers + 1)]

# Run simulation with specific policy
stats = run_simulation(routers, publishers, subscribers, 'LRU', iterations=100)

# Visualize results
plot_network_graph(routers, publishers, subscribers)
plot_policy_comparison(policy_stats)
```

## 🧪 Testing

The simulation automatically tests all four caching policies and generates:
- Individual policy performance graphs
- Comparative analysis charts
- Statistical summaries
- Network topology visualizations

## 📊 Sample Results

Expected performance characteristics:
- **LRU**: Good for temporal locality
- **LFU**: Optimal for skewed popularity distributions
- **FIFO**: Simple, predictable behavior
- **MRU**: Effective for scanning patterns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Router initialization bug in `__init__` method (line 53, 56)
- Memory usage may increase with large content catalogs
- Graph visualization performance with >20 nodes

## 🔮 Future Enhancements

- [ ] Additional caching policies (RANDOM, LRU-K)
- [ ] Dynamic network topology changes
- [ ] Real-time monitoring dashboard
- [ ] Multi-threaded simulation support
- [ ] Machine learning-based cache optimization

## 📞 Support

For questions or issues, please:
- Open an GitHub issue
- Check existing documentation
- Review the code comments for implementation details

---

**Note**: Ensure you have sufficient image content in the `cats` and `dogs` directories before running simulations. The system expects numbered image files (e.g., `cat_image1.jpg`, `dog_image1.jpg`).
