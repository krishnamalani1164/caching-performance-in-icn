import os
import random
import datetime
import time
import collections
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Base classes for Network elements
class Node:
    def __init__(self, name):
        self.name = name
        self.fib = {}  # Forwarding Information Base
        self.pit = {}  # Pending Interest Table
        self.cs = []   # Content Store with limited cache size (15 images)

class InterestPacket:
    def __init__(self, name):
        self.name = name
        self.nonce = random.randint(1000, 9999)

class DataPacket:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class ContentIDManager:
    _content_id_map = {}
    
    @classmethod
    def initialize_index(cls, publishers):
        """Initialize index for all images across publishers"""
        image_id = 100  # Starting ID range from 100
        for publisher in publishers:
            for image_name in publisher.images.keys():
                if image_name not in cls._content_id_map:
                    cls._content_id_map[image_name] = image_id
                    image_id += 1
    
    @classmethod
    def get_unique_id(cls, content_name):
        """Retrieve the unique ID for a given content name."""
        return cls._content_id_map.get(content_name, None)
    
# Router class with caching policies and FIB, PIT, CS functionality
class Router(Node):
    CACHE_LIMIT = 15  # Cache size limit

    def __init__(self, name, caching_policy='LRU'):
        super().__init__(name)
        self.connections = []  
        self.cache_hits = 0  
        self.publisher_hits = 0  
        self.requests_served_from_cache = 0
        self.requests_served_from_publisher = 0
        self.cache_evictions = 0  
        self.cache_access_times = {}  
        self.cache_frequency = collections.defaultdict(int)  
        self.total_cache_access_time = 0  
        self.total_requests = 0  
        self.content_popularity = collections.defaultdict(int)  
        self.cache_ttl = {}  
        self.caching_policy = caching_policy  

    def receive_interest(self, interest_packet, subscriber):
        content_id = ContentIDManager.get_unique_id(interest_packet.name)
        self.content_popularity[interest_packet.name] += 1
        self.total_requests += 1
        self.log_event(f"Received interest for {interest_packet.name} with ID {content_id} from Subscriber {subscriber.name}")

        access_time = random.uniform(0.01, 0.1)
        self.total_cache_access_time += access_time

        if interest_packet.name not in self.pit:
            self.pit[interest_packet.name] = subscriber.name
            self.save_pit()

        if interest_packet.name in self.cs:
            self.cache_hits += 1
            self.requests_served_from_cache += 1
            data_packet = DataPacket(name=interest_packet.name, content=interest_packet.name)
            self.log_event(f"Cache hit: Serving {interest_packet.name} with ID {content_id} from cache")
            subscriber.receive_data(data_packet)
        else:
            self.publisher_hits += 1
            self.log_event(f"Cache miss: Fetching {interest_packet.name} with ID {content_id} from Publisher or other routers")
            next_hop = self.fib.get(interest_packet.name)
            if next_hop:
                if isinstance(next_hop, Router):
                    next_hop.receive_interest(interest_packet, subscriber)
                elif isinstance(next_hop, Publisher):
                    data_packet = next_hop.serve_content(interest_packet.name)
                    if data_packet:
                        self.receive_data(data_packet)
                        subscriber.receive_data(data_packet)
            else:
                self.log_event(f"No route found in FIB for {interest_packet.name}")
            
            self.requests_served_from_publisher += 1

    def receive_data(self, data_packet):
        current_time = datetime.datetime.now()
        for content, expiry_time in list(self.cache_ttl.items()):
            if current_time > expiry_time:
                self.cs.remove(content)
                self.cache_ttl.pop(content)
                self.log_event(f"Content {content} expired and removed from cache")

        ttl = current_time + datetime.timedelta(minutes=5)
        self.cache_ttl[data_packet.name] = ttl

        content_id = ContentIDManager.get_unique_id(data_packet.name)

        if len(self.cs) >= Router.CACHE_LIMIT:
            self.cache_evictions += 1  
            if self.caching_policy == 'LRU':
                lru_content = min(self.cache_access_times, key=self.cache_access_times.get)
                self.cs.remove(lru_content)
                self.cache_access_times.pop(lru_content)
            elif self.caching_policy == 'LFU':
                lfu_content = min(self.cache_frequency, key=self.cache_frequency.get)
                self.cs.remove(lfu_content)
                self.cache_frequency.pop(lfu_content)
            elif self.caching_policy == 'FIFO':
                self.cs.pop(0)  
            elif self.caching_policy == 'MRU':
                mru_content = max(self.cache_access_times, key=self.cache_access_times.get)
                self.cs.remove(mru_content)
                self.cache_access_times.pop(mru_content)

        self.cs.append(data_packet.name)

        if self.caching_policy in ['LRU', 'MRU']:
            self.cache_access_times[data_packet.name] = datetime.datetime.now()
        elif self.caching_policy == 'LFU':
            self.cache_frequency[data_packet.name] += 1

        self.log_event(f"Cached {data_packet.name} with ID {content_id} in {self.name}'s Content Store with TTL of 5 minutes")
        self.save_cs()
        
    def save_fib(self):
        # Define the base FIB directory under Output/FIB
        fib_base_dir = 'Output/FIB'
        os.makedirs(fib_base_dir, exist_ok=True)  # Ensure FIB base directory exists
        
        # Define the specific directory for this router under Output/FIB
        fib_dir = os.path.join(fib_base_dir, self.name)
        os.makedirs(fib_dir, exist_ok=True)  # Ensure the router's FIB directory exists

        # Save FIB entries in a CSV file within this router's directory
        with open(f'{fib_dir}/fib.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID", "Next Hop"])  # Column headers
            for name, next_hop in self.fib.items():
                content_id = ContentIDManager.get_unique_id(name)
                next_hop_name = next_hop.name if next_hop else "None"
                writer.writerow([name, content_id, next_hop_name])

        print(f"FIB saved for {self.name} in directory: {fib_dir}")

    def save_pit(self):
        pit_dir = os.path.join('Output', 'PIT', self.name)
        os.makedirs(pit_dir, exist_ok=True)
        
        with open(f'{pit_dir}/pit.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID", "Face", "Lifetime"])
            for name, requester in self.pit.items():
                content_id = ContentIDManager.get_unique_id(name)
                writer.writerow([name, content_id, requester])
        print(f"PIT saved for {self.name} at {pit_dir}")

    def save_cs(self):
        # Define CS directory under Output/CS with router-specific subdirectories
        cs_dir = os.path.join('Output', 'CS', self.name)
        os.makedirs(cs_dir, exist_ok=True)
        
        with open(f'{cs_dir}/cs.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["CachedContent", "ID"])
            for content in self.cs:
                content_id = ContentIDManager.get_unique_id(content)
                writer.writerow([content, content_id])

        print(f"CS saved for {self.name} at {cs_dir}")

    def log_event(self, message):
        os.makedirs('Logs', exist_ok=True)
        with open(f'Logs/log_{self.name}.txt', 'a') as log_file:
            log_file.write(f"[{datetime.datetime.now()}] {message}\n")

class Publisher(Node):
    def __init__(self, name, folder):
        super().__init__(name)
        self.folder = folder
        self.images = self.load_images()

    def load_images(self):
        images = {}
        os.makedirs(self.folder, exist_ok=True)
        image_files = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]
        for image_name in image_files:
            file_path = os.path.join(self.folder, image_name)
            images[image_name] = file_path
        return images

    def serve_content(self, content_name):
        if content_name in self.images:
            file_path = self.images[content_name]
            with open(file_path, 'rb') as img_file:
                content = img_file.read()
            return DataPacket(name=content_name, content=content)
        return None

class Subscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.active = True

    def send_interest(self, content_name, router):
        interest_packet = InterestPacket(name=content_name)
        if isinstance(router, Router):
            router.receive_interest(interest_packet, self)

    def receive_data(self, data_packet):
        print(f"Subscriber {self.name} received data for {data_packet.name}")

def setup_network():
    # Select a single caching policy to apply to all routers
    print("Select a caching policy for all routers (LRU, LFU, FIFO, MRU):")
    policy = input("Enter caching policy for all routers: ").strip().upper()
    if policy not in ['LRU', 'LFU', 'FIFO', 'MRU']:
        print("Invalid policy selected. Please choose from LRU, LFU, FIFO, MRU.")
        return setup_network()

    num_routers = int(input("Enter the number of routers: "))
    routers = [Router(f'Router{i}', caching_policy=policy) for i in range(1, num_routers + 1)]
    
    publisher1 = Publisher('Publisher1', 'cats')
    publisher2 = Publisher('Publisher2', 'dogs')
    publishers = [publisher1, publisher2]
    
    num_subscribers = int(input("Enter the number of subscribers: "))
    subscribers = [Subscriber(f'Subscriber{i}') for i in range(1, num_subscribers + 1)]
    
    for i, subscriber in enumerate(subscribers):
        router_index = i % (num_routers - 2)
        subscriber.connected_router = routers[router_index]
    
    ContentIDManager.initialize_index(publishers)

    for i, router in enumerate(routers[:-1]):
        router.fib.update({f"cat_image{j}.jpg": routers[i + 1] for j in range(1, 51)})
        router.fib.update({f"dog_image{j}.jpg": routers[i + 1] for j in range(1, 51)})

    routers[-1].fib.update({f"cat_image{j}.jpg": publisher1 for j in range(1, 51)})
    routers[-1].fib.update({f"dog_image{j}.jpg": publisher2 for j in range(1, 51)})

    return routers, publishers, subscribers

def run_simulation(routers, publishers, subscribers, iterations):
    contents = [f"cat_image{i}.jpg" for i in range(1, 51)] + [f"dog_image{i}.jpg" for i in range(1, 51)]
    simulation_data = []  
    active_prob = 0.9  # Probability that a subscriber stays active each iteration

    for _ in range(iterations):
        for subscriber in subscribers:
            subscriber.active = random.random() < active_prob

        active_subscribers = [s for s in subscribers if s.active]
        if active_subscribers:
            subscriber = random.choice(active_subscribers)
            content_to_request = random.choice(contents)
            subscriber.send_interest(content_to_request, subscriber.connected_router)

        latency = random.uniform(0.01, 0.1)
        total_requests = sum(router.cache_hits + router.publisher_hits for router in routers)
        total_cache_hits = sum(router.cache_hits for router in routers)
        avg_cache_hit = (total_cache_hits / total_requests) * 100 if total_requests > 0 else 0
        avg_latency = latency / total_requests if total_requests > 0 else 0
        total_hop_reduction = sum(router.requests_served_from_cache for router in routers) / total_requests if total_requests > 0 else 0
        
        simulation_data.append([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            len(active_subscribers),
            total_requests,
            total_hop_reduction,
            avg_cache_hit,
            avg_latency
        ])

    save_simulation_log(simulation_data)
    plot_simulation_log(simulation_data)

def save_simulation_log(simulation_data):
    os.makedirs('Simulation_Log', exist_ok=True)
    with open('Simulation_Log/simulation_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Simulation Time", "No of Clients", "Total no of requests", "Average hop reduction", "Average Cache hit", "Average latency"])
        writer.writerows(simulation_data)
    print("Simulation log saved successfully.")

def plot_network_graph(routers, publishers, subscribers):
    G = nx.Graph()

    # Add routers as nodes
    for router in routers:
        G.add_node(router.name, label='Router', color='lightblue')

    # Add publishers as nodes
    for publisher in publishers:
        G.add_node(publisher.name, label='Publisher', color='lightgreen')

    # Add subscribers as nodes
    for subscriber in subscribers:
        G.add_node(subscriber.name, label='Subscriber', color='salmon')

    # Add edges between routers based on connections in FIB
    for router in routers:
        for destination, next_hop in router.fib.items():
            if next_hop and next_hop.name in G:
                G.add_edge(router.name, next_hop.name)

    # Connect subscribers to their associated router
    for subscriber in subscribers:
        if subscriber.connected_router:
            G.add_edge(subscriber.name, subscriber.connected_router.name)

    # Connect routers to publishers (last router in chain connected to publisher)
    for router in routers:
        for destination, next_hop in router.fib.items():
            if isinstance(next_hop, Publisher) and next_hop.name in G:
                G.add_edge(router.name, next_hop.name)

    # Set colors for nodes
    colors = [G.nodes[node]['color'] for node in G.nodes]
    
    # Draw the network graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=colors, font_weight='bold', node_size=800, font_size=10)
    plt.title("Network Topology: Routers, Publishers, and Subscribers")
    plt.show()

def plot_simulation_log(simulation_data):
    df = pd.DataFrame(simulation_data, columns=["Simulation Time", "No of Clients", "Total no of requests", "Average hop reduction", "Average Cache hit", "Average latency"])
    df['Index'] = range(1, len(df) + 1)
    
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    axs[0, 0].plot(df["Index"], df["No of Clients"], color='blue')
    axs[0, 0].set_title('No of Clients over Iterations')
    axs[0, 0].set_xlabel('Iteration')
    axs[0, 0].set_ylabel('No of Clients')
    
    axs[0, 1].plot(df["Index"], df["Average Cache hit"], color='green')
    axs[0, 1].set_title('Average Cache hit over Iterations')
    axs[0, 1].set_xlabel('Iteration')
    axs[0, 1].set_ylabel('Average Cache hit')
    
    axs[1, 0].plot(df["Index"], df["Average latency"], color='red')
    axs[1, 0].set_title('Average latency over Iterations')
    axs[1, 0].set_xlabel('Iteration')
    axs[1, 0].set_ylabel('Average latency')
    
    axs[1, 1].plot(df["Index"], df["Average hop reduction"], color='purple')
    axs[1, 1].set_title('Average hop reduction over Iterations')
    axs[1, 1].set_xlabel('Iteration')
    axs[1, 1].set_ylabel('Average hop reduction')
    
    plt.tight_layout()
    plt.show()


def main():
    routers, publishers, subscribers = setup_network()
    iterations = int(input("Enter the number of content requests in the simulation: "))
    run_simulation(routers, publishers, subscribers, iterations)
    
    # Plot the network topology after the simulation
    plot_network_graph(routers, publishers, subscribers)

if __name__ == "__main__":
    main()
