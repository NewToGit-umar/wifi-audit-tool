import json
import csv

class FileParser:
    """Parse various file formats"""
    
    @staticmethod
    def read_json(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def write_json(data, filepath):
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False
    
    @staticmethod
    def read_wordlist(filepath):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []
    
    @staticmethod
    def read_csv(filepath):
        try:
            data = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except:
            return []
