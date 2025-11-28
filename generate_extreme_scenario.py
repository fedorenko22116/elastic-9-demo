#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import random

ES_URL = 'http://localhost:9201'
INDEX = 'logs-app'
AUTH = ('elastic', 'elastic123')

base_time = datetime.utcnow() - timedelta(hours=8)

print('Generating EXTREME scenario with 15000 logs and multiple issues...')

for i in range(15000):
    timestamp = base_time + timedelta(seconds=i*1.92)
    progress = i / 15000
    
    # 75% normal INFO/DEBUG logs (heavy noise)
    if random.random() < 0.75:
        log = {
            '@timestamp': timestamp.isoformat(),
            'timestamp': timestamp.isoformat(),
            'level': random.choice(['INFO', 'INFO', 'INFO', 'DEBUG', 'DEBUG']),
            'service': random.choice(['api-gateway', 'payment-service', 'user-service', 'notification-service', 'auth-service', 'cache-service', 'search-service']),
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
                'Metrics collected',
                'Background job completed',
                'Scheduled task executed'
            ]),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'response_time': random.randint(10, 250)
        }
    
    # Issue 1: auth-service database degradation (root cause)
    elif progress < 0.3 and random.random() < 0.4:
        log = {
            '@timestamp': timestamp.isoformat(),
            'timestamp': timestamp.isoformat(),
            'level': 'WARN',
            'service': 'auth-service',
            'message': random.choice([
                'Slow database query: SELECT * FROM users took 2.2s',
                'Database index not used - full table scan',
                'Query optimizer chose suboptimal plan'
            ]),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'response_time': random.randint(2000, 3500)
        }
    
    # Issue 2: cache-service memory leak (red herring - starts early but not root cause)
    elif progress > 0.15 and progress < 0.6 and random.random() < 0.3:
        log = {
            '@timestamp': timestamp.isoformat(),
            'timestamp': timestamp.isoformat(),
            'level': random.choice(['WARN', 'ERROR']),
            'service': 'cache-service',
            'message': random.choice([
                f'Memory usage at {int(60 + progress * 40)}% - potential leak',
                'Cache eviction rate increased',
                'GC pause time increased to 500ms',
                'OutOfMemoryError: unable to allocate cache entry'
            ]),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'response_time': random.randint(100, 800)
        }
    
    # Issue 3: payment-service intermittent network issues (another red herring)
    elif progress > 0.2 and progress < 0.7 and random.random() < 0.25:
        log = {
            '@timestamp': timestamp.isoformat(),
            'timestamp': timestamp.isoformat(),
            'level': 'ERROR',
            'service': 'payment-service',
            'message': random.choice([
                'Network timeout connecting to payment gateway',
                'Connection reset by peer',
                'SSL handshake failed',
                'Payment gateway returned 502'
            ]),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'response_time': random.randint(5000, 8000)
        }
    
    # Cascading effect from auth-service
    elif progress > 0.3 and progress < 0.65:
        if random.random() < 0.5:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'auth-service',
                'message': random.choice([
                    'Connection pool exhausted - max 50 connections',
                    'Database connection timeout after 10s',
                    'Too many concurrent requests - rejecting'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(10000, 18000)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'api-gateway',
                'message': random.choice([
                    'Auth service timeout - retrying',
                    'Failed to authenticate user',
                    'Upstream timeout: auth-service'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(8000, 12000)
            }
    
    # System-wide collapse
    else:
        if random.random() < 0.4:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': random.choice(['user-service', 'notification-service', 'search-service']),
                'message': random.choice([
                    'Circuit breaker OPEN - too many failures',
                    'Unable to reach auth-service',
                    'Request rejected - system overloaded',
                    'Dependency failure - auth-service unavailable'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(100, 600)
            }
        else:
            log = {
                '@timestamp': timestamp.isoformat(),
                'timestamp': timestamp.isoformat(),
                'level': 'ERROR',
                'service': 'api-gateway',
                'message': random.choice([
                    '503 Service Unavailable',
                    'Multiple downstream failures',
                    'System degraded - high error rate'
                ]),
                'user_id': f'user_{random.randint(1000, 9999)}',
                'response_time': random.randint(200, 1500)
            }
    
    requests.post(f'{ES_URL}/{INDEX}/_doc', auth=AUTH, json=log)
    
    if (i + 1) % 1500 == 0:
        print(f'{i + 1} logs generated...')

print('✅ Done! 15000 logs with EXTREME challenge')
print('Multiple issues: auth DB (root), cache leak (red herring), payment network (red herring)')
print('Challenge: Identify the TRUE root cause among multiple concurrent problems')
