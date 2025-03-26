class Config:
    """
    Configuration settings for the Blockchain E-Voting System
    """
    # Blockchain configuration
    BLOCKCHAIN_DIFFICULTY = 4  # Number of leading zeros in proof of work
    
    # Voting system configuration
    MAX_VOTES_PER_ELECTION = 10000
    VOTER_REGISTRATION_PERIOD = 30  # days
    ELECTION_DURATION = 24  # hours

    # Security settings
    VOTE_ENCRYPTION_KEY = 'your_secure_encryption_key_here'  # Replace with a secure key
    
    # Database configuration (placeholder)
    DATABASE_URI = 'sqlite:///blockchain_evoting.db'
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'blockchain_evoting.log'