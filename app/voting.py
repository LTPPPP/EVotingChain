from typing import List, Dict, Any
import hashlib
import uuid
import time
from app.utils import validate_email

class VotingSystem:
    def __init__(self, election_start_time: float = None):
        self.voters: List[Dict[str, Any]] = []
        self.candidates: List[Dict[str, Any]] = []
        self.registered_voters: List[str] = []
        self.election_start_time = election_start_time or time.time()
        self.election_duration = 24 * 60 * 60  # 24 hours in seconds

    def register_voter(self, name: str, email: str) -> str:
        """
        Register a new voter and generate a unique voter ID
        """
        if not validate_email(email):
            raise ValueError("Invalid email address")

        # Check if email already exists
        if any(voter['email'] == email for voter in self.voters):
            raise ValueError("Email already registered")

        voter_id = str(uuid.uuid4())
        voter = {
            'id': voter_id,
            'name': name,
            'email': email,
            'has_voted': False,
            'registration_time': time.time()
        }
        self.voters.append(voter)
        self.registered_voters.append(voter_id)
        return voter_id

    def register_candidate(self, name: str, party: str) -> str:
        """
        Register a new candidate
        """
        candidate_id = str(uuid.uuid4())
        candidate = {
            'id': candidate_id,
            'name': name,
            'party': party,
            'registration_time': time.time()
        }
        self.candidates.append(candidate)
        return candidate_id

    def verify_voter(self, voter_id: str) -> bool:
        """
        Verify if a voter is registered and has not already voted
        """
        for voter in self.voters:
            if (voter['id'] == voter_id and 
                not voter['has_voted'] and 
                time.time() - self.election_start_time <= self.election_duration):
                return True
        return False

    def cast_vote(self, voter_id: str, candidate_id: str, blockchain) -> bool:
        """
        Cast a vote after verification
        """
        # Check if voting period is active
        if time.time() - self.election_start_time > self.election_duration:
            raise ValueError("Voting period has ended")

        # Verify voter
        if not self.verify_voter(voter_id):
            raise ValueError("Invalid voter or already voted")

        # Verify candidate exists
        if not any(candidate['id'] == candidate_id for candidate in self.candidates):
            raise ValueError("Invalid candidate")

        # Mark voter as having voted
        for voter in self.voters:
            if voter['id'] == voter_id:
                voter['has_voted'] = True
                break

        # Add vote to blockchain
        blockchain.add_vote(voter_id, candidate_id)
        return True

    def get_election_results(self, blockchain) -> List[Dict[str, Any]]:
        """
        Tally the votes and return results
        """
        results = []
        for candidate in self.candidates:
            candidate_votes = blockchain.get_votes_for_candidate(candidate['id'])
            results.append({
                'candidate': candidate,
                'vote_count': len(candidate_votes)
            })
        
        return sorted(results, key=lambda x: x['vote_count'], reverse=True)

    def get_voter_count(self) -> int:
        """
        Get total number of registered voters
        """
        return len(self.registered_voters)

    def get_candidate_count(self) -> int:
        """
        Get total number of registered candidates
        """
        return len(self.candidates)