from bisect import bisect_left

class SegmentTree:
    def __init__(self, transactions):
        """
        Initialize the Segment Tree for fast transaction lookups.
        :param transactions: List of (timestamp, amount) tuples sorted by time.
        """
        self.n = len(transactions)
        self.transactions = transactions # store transactions
        self.tree = [0] * (4 * self.n) # Segment Tree storage
        self.build(0, 0, self.n - 1)
    
    def build(self, node, start, end):
        """Build segment tree recursively"""

        if start == end:
            self.tree[node] = self.transactions[start][1] # Store transaction amount
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.build(left_child, start, mid)
            self.build(right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def query(self, node, start, end, left, right):
        """Query sum of transactions in the range [left, right]"""
        
        if right < start or left > end:
            return 0 # Out of range
        if left <= start and end <= right:
            return self.tree[node] # Completely inside range
        
        mid = (start + end) // 2
        return self.query(2 * node + 1, start, mid, left, right) + \
                self.query(2 * node + 2, mid + 1, end, left, right)
    
    def update(self, node, start, end, idx, value):
        """Update transaction amount at index idx."""
        
        if start == end:
            self.tree[node] += value # Add new transaction amount
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, value)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, value)
            
            self.tree[node] = self.tree[2* node + 1] + self.tree[2 * node + 2]
    
    def get_total_amount_in_range(self, start_time, end_time):
        """Get sum of transactions in a given time range"""

        left = self._find_index(start_time)
        right = self._find_index(end_time)
        return self.query(0, 0, self.n - 1, left, right)

    def add_transaction(self, timestamp, amount):
        """Insert a new transaction and update the segment tree"""

        index = self._find_index(timestamp)
        if index < self.n and self.transactions[index][0] == timestamp:
            print("Transaction already exists at this timestamp.")
            return  # Avoid duplicate timestamps
        
        self.transactions.append((timestamp, amount))
        self.n += 1
        self.update(0, 0, self.n - 1, index, amount)  # Update only one node
    
    def _find_index(self, timestamp):
        """Find the index of a timestamp using binary search"""

        transactions_sorted = [t[0] for t in self.transactions]
        index = bisect_left(transactions_sorted, timestamp)
        print(f"Finding index for timestamp {timestamp} -> Found index: {index}")
        return index


# Example Transactions: [(timestamp, amount)]
transactions = [
    (1672531200, 1000),  # Timestamp (Unix) -> Amount
    (1672531210, 5000),
    (1672531230, 2000),
    (1672531245, 3000),
    (1672531260, 1500),
]

# Initialize segment tree
seg_tree = SegmentTree(transactions)

# Query: Find sum of transactions in the last 30 seconds
start_time = 1672531210
end_time = 1672531240
print("Total amount spent:", seg_tree.get_total_amount_in_range(start_time, end_time))

# Add a new transaction
seg_tree.add_transaction(1672531275, 4000)

# Query after update
print("Updated total amount spent:", seg_tree.get_total_amount_in_range(start_time, end_time))