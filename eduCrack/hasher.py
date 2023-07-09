import hashlib


def detect_hash_algorithm(hashes_file):
    with open(hashes_file, 'r') as file:
        hashes = file.read().splitlines()

    algorithm_counts = {}

    for hash_value in hashes:
        for algorithm in hashlib.algorithms_available:
            hash_object = hashlib.new(algorithm)
            if hash_object.digest_size * 2 == len(hash_value):
                algorithm_name = algorithm.lower()
                algorithm_counts[algorithm_name] = algorithm_counts.get(algorithm_name, 0) + 1

    if algorithm_counts:
        sorted_algorithms = sorted(algorithm_counts, key=algorithm_counts.get, reverse=True)
        return sorted_algorithms[:3]
    else:
        print("Error: Unable to detect the hashing algorithm used in the file.")
        return None


def hash_password(algorithms, password):
    try:
        if isinstance(algorithms, str):
            algorithms = [algorithms]  # Convert single algorithm to a list

        hashes = []
        for algorithm in algorithms:
            if algorithm == 'ntlm':
                hashes.append(hashlib.new('md4', password.encode('utf-16le')).hexdigest())
            else:
                hasher = hashlib.new(algorithm)
                hasher.update(password.encode())
                hashes.append(hasher.hexdigest())

        return hashes

    except ValueError as e:
        print(f"Error: {e}")
        return []

