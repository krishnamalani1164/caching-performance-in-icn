# ----------------------------------------
# iFLAT Algorithm Simulation in Python
# (Based on the three given pseudocode algorithms)
# ----------------------------------------

class Face:
    """
    Represents a network interface (Face) in NDN.
    Each face has a name and a signal power in dBm.
    """
    def __init__(self, name, power_dbm=0):
        self.name = name
        self.power_dbm = power_dbm

    def GET_PHY_POWER_RX(self):
        # Returns received signal strength
        return self.power_dbm


class PITEntry:
    """
    Stores information about an Interest in the Pending Interest Table (PIT).
    Tracks the Interest name and which faces it has been sent to.
    """
    def __init__(self, interest_name):
        self.interest_name = interest_name
        self.sent_faces = []


class FIBEntry:
    """
    Represents a Forwarding Information Base (FIB) entry.
    Holds a list of possible next hops (faces) for forwarding Interests.
    """
    def __init__(self, next_hops):
        self.next_hops = next_hops  # List of Face objects

    def GET_NEXT_HOPS(self):
        return self.next_hops


class MeasurementInfo:
    """
    Stores and updates performance measurements:
    - cpdrx: Count of received data packets
    - cpitx: Count of transmitted Interests
    - drx: Dictionary mapping data names to received counts
    """
    def __init__(self):
        self.cpdrx = 0
        self.cpitx = 0
        self.drx = {}

    def ADD_PREFIX_MEASUREMENTS(self, pitEntry):
        # Pretend to set up measurement tracking for this Interest
        pass

    def Cpdrx(self):
        return self.cpdrx

    def Cpitx(self):
        return self.cpitx

    def UPDATE_itx(self, interest):
        # Count that we sent another Interest
        self.cpitx += 1

    def UPDATE_drx(self, data_name):
        # Count that we received data with this name
        self.drx[data_name] = self.drx.get(data_name, 0) + 1


# ------------------------
# Global lists / storage
# ------------------------

Blist = set()        # Blacklist for prefixes of fake Interests
Flist = set()        # Fake Interest names list
LocalStorage = {}    # Storage for producer's data


# ------------------------
# Network operation placeholders
# (In real NDN, these would send packets on the network)
# ------------------------

def LOOKUP_FIB(pitEntry):
    # In reality, looks up next hops for this Interest
    # Here we fake it with two faces
    return FIBEntry([Face("Face1", 15), Face("Face2", 8)])

def SEND_INTEREST(pitEntry, outFace, interest):
    pitEntry.sent_faces.append(outFace.name)
    print(f"[SEND_INTEREST] Sent Interest '{interest}' via {outFace.name}")

def REPLY_WITH_NACK(pitEntry, inFace, reason):
    print(f"[NACK] Sent to {inFace.name} for Interest '{pitEntry.interest_name}' Reason: {reason}")

def REJECT_PENDING_INTEREST(pitEntry):
    print(f"[DROP] Interest '{pitEntry.interest_name}' dropped.")

def SEND_DATA(data):
    print(f"[DATA] Sending data: {data}")

def GENERATE_WARNING_DATA(interest):
    return f"WARNING: Fake Interest detected for {interest}"

def SCHEDULE_UPDATE_IN_Flist():
    print("[UPDATE] Fake Interest list scheduled for update.")

def SEND_WARNING_DATA(wdata):
    print(f"[WARNING] {wdata}")


# ------------------------
# Algorithm 1: AfterReceiveInterest
# ------------------------
def AfterReceiveInterest(inFace, interest, pitEntry, meInfo, a=10, b=2):
    """
    Decides what to do with a newly received Interest packet:
    - Forward to next hops if valid
    - Send NACK if fake
    - Drop if nothing is sent
    """
    RSS = inFace.GET_PHY_POWER_RX()  # How strong is the signal
    meInfo.ADD_PREFIX_MEASUREMENTS(pitEntry)  # Start tracking performance
    fibEntry = LOOKUP_FIB(pitEntry)  # Get possible next hops from FIB

    sent = False  # Tracks if we sent the Interest forward

    for nextHop in fibEntry.GET_NEXT_HOPS():
        outFace = nextHop

        # If node is a producer or consumer → just send Interest
        if "Producer" in outFace.name or "Consumer" in outFace.name:
            SEND_INTEREST(pitEntry, outFace, interest)
            sent = True
            continue

        # Relay node logic
        if RSS > a:  # Only handle if signal is above threshold
            if interest in Blist:
                # Forward if receive-to-transmit ratio is high enough
                if meInfo.Cpdrx() / max(1, meInfo.Cpitx()) > b:
                    SEND_INTEREST(pitEntry, outFace, interest)
                    meInfo.UPDATE_itx(interest)
                    sent = True
            else:
                # If fake, send a NACK back
                REPLY_WITH_NACK(pitEntry, inFace, "IFADetected")

    # If we never forwarded the Interest, drop it
    if not sent:
        REJECT_PENDING_INTEREST(pitEntry)


# ------------------------
# Algorithm 2: BeforeSatisfyInterest
# ------------------------
def BeforeSatisfyInterest(data_name, is_warning, meInfo):
    """
    Called when Data is about to be sent to satisfy an Interest.
    - If warning data, add to blacklist
    - If normal data, update reception count
    """
    if is_warning:
        Blist.add(data_name)
        print(f"[BLACKLIST] Added prefix {data_name}")
    else:
        meInfo.UPDATE_drx(data_name)
        print(f"[UPDATE] Data received for {data_name}")


# ------------------------
# Algorithm 3: ProducerDetectionIFA & CounterMeasureIFA
# ------------------------
def ProducerDetectionIFA(interest):
    """
    Runs at the producer to detect Interest Flooding.
    - If Interest is in fake list, countermeasure directly
    - If legitimate data exists, send it
    - Else, mark as fake and countermeasure
    """
    i = interest
    if i not in Flist:
        data = LocalStorage.get(i)
        if data is not None:
            SEND_DATA(data)
        else:
            Flist.add(i)
            CounterMeasureIFA(i)
    else:
        CounterMeasureIFA(i)

def CounterMeasureIFA(interest):
    """
    Sends warning data in response to a fake Interest.
    Also schedules updates to the fake list.
    """
    wdata = GENERATE_WARNING_DATA(interest)
    SCHEDULE_UPDATE_IN_Flist()
    SEND_WARNING_DATA(wdata)


# ------------------------
# Example Simulation Run
# ------------------------
if __name__ == "__main__":
    # Create incoming face (Relay Node with power 12 dBm)
    incoming_face = Face("RelayNode1", power_dbm=12)

    # Create a PIT entry for Interest1
    pit = PITEntry("Interest1")

    # Measurement tracking object
    meInfo = MeasurementInfo()

    # 1️⃣ Simulate receiving an Interest at a relay
    AfterReceiveInterest(incoming_face, "Interest1", pit, meInfo)

    # 2️⃣ Simulate satisfying Interest with normal data
    BeforeSatisfyInterest("Interest1", False, meInfo)

    # 3️⃣ Simulate producer detecting a fake Interest
    ProducerDetectionIFA("FakeInterest1")
