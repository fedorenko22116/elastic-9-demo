#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import random

ES_URL = 'http://localhost:9201'
INDEX = 'logs-app'
AUTH = ('elastic', 'elastic123')

base_time = datetime.utcnow() - timedelta(hours=6)

print('Generating harder scenario with 10000 logs...')

for i in range(10000):
    timestamp = base_time + timedelta(seconds=i*2.16)
    progress = i / 10000
    
    # 70% normal INFO/DEBUG logs (noise)
    if random.random() < 0.7:
        log = {
            '@timestamp': timestamp.isoformat(),
            'timestamp': timestamp.isoformat(),
            'level': random.choice(['INFO', 'INFO', 'INFO', 'DEBUG']),
            'service': random.choice(['api-gateway', 'payment-service', 'user-service', 'notification-service', 'auth-service']),
            'message': random.choice([
                'Request processed successfully',
                'User session created',
                'Cache hit for key',
                'Health check passed',
                'API request received',
                'Response sent to client',
                'Database query completed',
                'Service started successfully',
                'Configuration loaded',
                'Metrics collected'
            ]),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'response_time': random.randint(10, 200)
        }
    
    # Phase 1 (0-25%): Subtle database performance degradation in auth-service
    elif progress < 0.25:
        if random.random() < 0.08:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'WARN',
                'service': 'auth-service',
                'message': random.choice([
                    'Slow database query detected: SELECT * FROM users took 2.1s',
                    'Database query took longer than expected: 2.3s',
                    'Query performance degraded: users table scan 2.5s'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(2000, 3000)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'INFO',
                'service': random.choice(['api-gateway', 'payment-service', 'user-service']),
                'message': 'Request processed successfully',
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(50, 300)
            }
    
    # Phase 2 (25-50%): Connection pool issues emerge
    elif progress < 0.5:
        if random.random() < 0.12:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': random.choice(['WARN', 'ERROR']),
                'service': 'auth-service',
                'message': random.choice([
                    'Connection pool at 80% capacity - 40/50 connections',
                    'Connection pool exhausted - max 50 connections',
                    'Waiting for available database connection',
                    'Connection pool timeout after 5s'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(5000, 12000)
            }
        elif random.random() < 0.15:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'WARN',
                'service': 'api-gateway',
                'message': random.choice([
                    'Auth service response time increased: 3.2s',
                    'Slow response from auth-service',
                    'Auth service latency detected'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(3000, 6000)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'INFO',
                'service': random.choice(['payment-service', 'user-service', 'notification-service']),
                'message': 'Request processed successfully',
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(100, 500)
            }
    
    # Phase 3 (50-75%): Cascading timeouts
    elif progress < 0.75:
        if random.random() < 0.18:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'api-gateway',
                'message': random.choice([
                    'Auth service timeout - retrying request',
                    'Request timeout after 10s - auth-service',
                    'Failed to authenticate user - timeout',
                    'Upstream service timeout: auth-service'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(10000, 15000)
            }
        elif random.random() < 0.2:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'auth-service',
                'message': random.choice([
                    'Database connection timeout',
                    'Connection pool exhausted - rejecting request',
                    'Unable to acquire database connection'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(8000, 20000)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': random.choice(['INFO', 'WARN']),
                'service': random.choice(['payment-service', 'user-service', 'notification-service']),
                'message': random.choice(['Request processed', 'High latency detected', 'Service degraded']),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(500, 2000)
            }
    
    # Phase 4 (75-100%): System-wide failure
    else:
        if random.random() < 0.25:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': random.choice(['payment-service', 'notification-service', 'user-service']),
                'message': random.choice([
                    'Circuit breaker OPEN - too many failures',
                    'Unable to reach auth-service',
                    'Request rejected - system overloaded',
                    'Service unavailable - dependency failure'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(100, 500)
            }
        elif random.random() < 0.3:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'api-gateway',
                'message': random.choice([
                    '503 Service Unavailable - downstream services failing',
                    'Multiple service failures detected',
                    'System overload - rejecting requests'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(200, 1000)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': random.choice(['INFO', 'WARN']),
                'service': random.choice(['api-gateway', 'payment-service', 'user-service', 'notification-service']),
                'message': random.choice([
                    'Request processed successfully',
                    'Degraded performance detected',
                    'Service operating in fallback mode'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(200, 3000)
            }
    
    requests.post(f'{ES_URL}/{INDEX}/_doc', auth=AUTH, json=log)
    
    if (i + 1) % 1000 == 0:
        print(f'{i + 1} logs generated...')

print('✅ Done! 10000 logs with harder scenario')
print('Challenge: Find root cause among 70% noise (INFO/DEBUG logs)')
