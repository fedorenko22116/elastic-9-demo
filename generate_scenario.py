#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import random

ES_URL = 'http://localhost:9201'
INDEX = 'logs-app'
AUTH = ('elastic', 'elastic123')

def create_index():
    requests.put(f'{ES_URL}/{INDEX}', auth=AUTH, json={
        "mappings": {
            "properties": {
                "@timestamp": {"type": "date"},
                "timestamp": {"type": "date"},
                "level": {"type": "keyword", "meta": {"description": "Log severity level: INFO, WARN, ERROR, DEBUG"}},
                "service": {"type": "keyword", "meta": {"description": "Microservice name"}},
                "message": {"type": "text", "meta": {"description": "Log message content"}},
                "user_id": {"type": "keyword"},
                "response_time": {"type": "integer", "meta": {"description": "Response time in milliseconds"}}
            }
        }
    })

def generate_logs():
    base_time = datetime.utcnow() - timedelta(hours=3)
    
    print('Generating cascading failure scenario...')
    
    for i in range(1500):
        timestamp = base_time + timedelta(minutes=i*0.12)
        progress = i / 1500
        
        if progress < 0.3:
            if random.random() < 0.15:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'WARN',
                    'service': 'auth-service',
                    'message': 'Slow database query detected: SELECT * FROM users took 2.5s',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(2000, 4000)
                }
            else:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': random.choice(['INFO', 'DEBUG']),
                    'service': random.choice(['api-gateway', 'payment-service', 'user-service', 'notification-service']),
                    'message': 'Request processed successfully',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(50, 300)
                }
        elif progress < 0.6:
            if random.random() < 0.25:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'ERROR',
                    'service': 'api-gateway',
                    'message': 'Auth service timeout - retrying request',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(5000, 10000)
                }
            elif random.random() < 0.3:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'ERROR',
                    'service': 'auth-service',
                    'message': 'Connection pool exhausted - max 50 connections',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(8000, 15000)
                }
            else:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': random.choice(['INFO', 'WARN']),
                    'service': random.choice(['payment-service', 'user-service', 'notification-service']),
                    'message': random.choice(['Request processed', 'High latency detected']),
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(500, 2000)
                }
        else:
            if random.random() < 0.4:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'ERROR',
                    'service': random.choice(['payment-service', 'notification-service']),
                    'message': random.choice([
                        'Circuit breaker OPEN - too many failures',
                        'Unable to reach auth-service',
                        'Request rejected - system overloaded'
                    ]),
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(100, 500)
                }
            elif random.random() < 0.5:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'ERROR',
                    'service': 'api-gateway',
                    'message': '503 Service Unavailable - downstream services failing',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(200, 1000)
                }
            else:
                log = {
                    '@timestamp': timestamp.isoformat(),
                    'timestamp': timestamp.isoformat(),
                    'level': 'WARN',
                    'service': 'user-service',
                    'message': 'Degraded performance - auth dependency issues',
                    'user_id': f'user_{random.randint(1000, 9999)}',
                    'response_time': random.randint(1000, 3000)
                }
        
        requests.post(f'{ES_URL}/{INDEX}/_doc', auth=AUTH, json=log)
        
        if (i + 1) % 300 == 0:
            print(f'{i + 1} logs generated...')
    
    print('✅ Done! 1500 logs generated')

if __name__ == '__main__':
    import time
    print('Waiting for Elasticsearch...')
    time.sleep(30)
    create_index()
    generate_logs()
