from flask import Flask, request, jsonify, render_template
from app.blockchain import Blockchain
from app.voting import VotingSystem
import logging
import uuid
import os

os.makedirs('logs', exist_ok=True)

app = Flask(__name__)
blockchain = Blockchain(blockchain_file='blockchain_data.json')
voting_system = VotingSystem()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/blockchain_evoting.log'),
        logging.StreamHandler()
    ]
)
# Web Interface Routes
@app.route('/')
def index():
    return render_template('index.html', 
                           candidates=voting_system.candidates,
                           voter_count=voting_system.get_voter_count(),
                           candidate_count=voting_system.get_candidate_count())

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/vote')
def vote_page():
    return render_template('vote.html', 
                           candidates=voting_system.candidates,
                           voters=voting_system.voters)

@app.route('/results')
def results_page():
    try:
        results = voting_system.get_election_results(blockchain)
        return render_template('results.html', results=results)
    except Exception as e:
        logging.error(f"Error retrieving election results: {str(e)}")
        return render_template('error.html', message='Unable to retrieve results')

# API Routes (kept from previous implementation)
@app.route('/api/register_voter', methods=['POST'])
def register_voter():
    try:
        data = request.form
        voter_id = voting_system.register_voter(
            name=data['name'], 
            email=data['email']
        )
        logging.info(f"Voter registered: {voter_id}")
        return render_template('success.html', 
                               message='Voter registered successfully', 
                               voter_id=voter_id)
    except ValueError as e:
        logging.error(f"Voter registration error: {str(e)}")
        return render_template('error.html', message=str(e))

@app.route('/api/register_candidate', methods=['POST'])
def register_candidate():
    try:
        data = request.form
        candidate_id = voting_system.register_candidate(
            name=data['name'], 
            party=data['party']
        )
        logging.info(f"Candidate registered: {candidate_id}")
        return render_template('success.html', 
                               message='Candidate registered successfully', 
                               candidate_id=candidate_id)
    except Exception as e:
        logging.error(f"Candidate registration error: {str(e)}")
        return render_template('error.html', message=str(e))

@app.route('/api/cast_vote', methods=['POST'])
def cast_vote():
    try:
        data = request.form
        success = voting_system.cast_vote(
            voter_id=data['voter_id'], 
            candidate_id=data['candidate_id'], 
            blockchain=blockchain
        )
        logging.info(f"Vote cast by voter: {data['voter_id']}")
        return render_template('success.html', message='Vote cast successfully')
    except ValueError as e:
        logging.error(f"Vote casting error: {str(e)}")
        return render_template('error.html', message=str(e))

@app.route('/blockchain_validation')
def validate_blockchain():
    try:
        is_valid = blockchain.is_chain_valid()
        logging.info(f"Blockchain validation result: {is_valid}")
        return render_template('blockchain_validation.html', 
                               is_valid=is_valid)
    except Exception as e:
        logging.error(f"Blockchain validation error: {str(e)}")
        return render_template('error.html', message='Blockchain validation failed')

# Templates (I'll provide these in a moment)
if __name__ == '__main__':
    # Create some sample data for testing
    try:
        # Register some candidates if not already registered
        if len(voting_system.candidates) == 0:
            voting_system.register_candidate("Alice Johnson", "Progressive Party")
            voting_system.register_candidate("Bob Smith", "Conservative Party")
            voting_system.register_candidate("Charlie Brown", "Independent")

        # Register some voters if not already registered
        if len(voting_system.registered_voters) == 0:
            for i in range(5):
                voting_system.register_voter(f"Voter {i+1}", f"voter{i+1}@example.com")
    except Exception as e:
        print(f"Error setting up sample data: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)