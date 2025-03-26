import hashlib
import json
import time
import os
from typing import List, Dict, Any

class Blockchain:
    def __init__(self, blockchain_file='blockchain_data.json'):
        self.blockchain_file = blockchain_file
        self.chain: List[Dict[str, Any]] = []
        self.pending_votes: List[Dict[str, Any]] = []
        
        # Load existing blockchain or create new
        if os.path.exists(self.blockchain_file):
            self.load_blockchain()
        else:
            self.create_genesis_block()
            self.save_blockchain()

    def create_genesis_block(self):
        genesis_block = {
            'index': 1,
            'timestamp': time.time(),
            'votes': [],
            'proof': 1,
            'previous_hash': '0'
        }
        self.chain.append(genesis_block)

    def save_blockchain(self):
        """
        Save the entire blockchain to a JSON file
        """
        try:
            with open(self.blockchain_file, 'w') as f:
                json.dump({
                    'chain': self.chain,
                    'pending_votes': self.pending_votes
                }, f, indent=4)
            print(f"Blockchain saved to {self.blockchain_file}")
        except Exception as e:
            print(f"Error saving blockchain: {e}")

    def load_blockchain(self):
        """
        Load blockchain from JSON file
        """
        try:
            with open(self.blockchain_file, 'r') as f:
                data = json.load(f)
                self.chain = data.get('chain', [])
                self.pending_votes = data.get('pending_votes', [])
            
            # If no chain exists, create genesis block
            if not self.chain:
                self.create_genesis_block()
            
            print(f"Blockchain loaded from {self.blockchain_file}")
        except FileNotFoundError:
            print(f"Blockchain file {self.blockchain_file} not found. Creating new blockchain.")
            self.create_genesis_block()
        except json.JSONDecodeError:
            print("Error decoding blockchain file. Creating new blockchain.")
            self.create_genesis_block()
        except Exception as e:
            print(f"Unexpected error loading blockchain: {e}")
            self.create_genesis_block()

    def create_block(self, proof: int, previous_hash: str) -> Dict[str, Any]:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'votes': self.pending_votes.copy(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_votes = []
        self.chain.append(block)
        
        # Save blockchain after creating a new block
        self.save_blockchain()
        
        return block

    def get_previous_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_block(self, block: Dict[str, Any]) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):
            block = self.chain[current_index]
            
            # Check previous hash
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            
            # Check proof of work
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            current_index += 1
        
        return True

    def add_vote(self, voter_id: str, candidate_id: str) -> Dict[str, Any]:
        vote = {
            'voter_id': voter_id,
            'candidate_id': candidate_id,
            'timestamp': time.time()
        }
        self.pending_votes.append(vote)
        
        # If pending votes reach a certain threshold, mine a new block
        if len(self.pending_votes) >= 5:  # You can adjust this threshold
            previous_block = self.get_previous_block()
            proof = self.proof_of_work(previous_block['proof'])
            previous_hash = self.hash_block(previous_block)
            self.create_block(proof, previous_hash)
        
        # Optionally save after adding a vote
        self.save_blockchain()
        
        return self.get_previous_block()

    def get_votes_for_candidate(self, candidate_id: str) -> List[Dict[str, Any]]:
        candidate_votes = []
        for block in self.chain:
            for vote in block.get('votes', []):
                if vote['candidate_id'] == candidate_id:
                    candidate_votes.append(vote)
        return candidate_votes

    def get_total_blocks(self) -> int:
        return len(self.chain)

    def get_blockchain_size(self) -> int:
        return len(json.dumps(self.chain))