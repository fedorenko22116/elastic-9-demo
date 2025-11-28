# AI Assistant Test Guide - Extreme Scenario

## Scenario Overview
15,000 logs over 8 hours with:
- **Root Cause**: auth-service database performance degradation
- **Red Herring 1**: cache-service memory leak
- **Red Herring 2**: payment-service network issues
- **75% noise**: Normal INFO/DEBUG logs

## Test Questions (Progressive Difficulty)

### Level 1: Surface Analysis (AI passed ✓)
- "What is the root cause of the system failure?"
- Expected: Identifies auth-service as problematic

### Level 2: Deep Root Cause Analysis
Ask these follow-up questions:

1. **"What was the FIRST problem that appeared in auth-service before the failures?"**
   - Expected: Should find slow database queries (WARN level)

2. **"Show me the timeline of auth-service issues from the beginning"**
   - Expected: Should trace back to database performance warnings

3. **"What specific error messages appeared in auth-service BEFORE the connection pool exhaustion?"**
   - Expected: Slow queries, database index issues

4. **"Compare the error patterns: are cache-service and payment-service issues independent or caused by auth-service?"**
   - Expected: Should identify cache/payment as independent issues

5. **"What is the difference between the root cause and symptoms in this incident?"**
   - Expected: Root = DB performance, Symptoms = timeouts/circuit breakers

### Level 3: Red Herring Detection

6. **"Is the cache-service memory leak related to the auth-service failures?"**
   - Expected: No, it's an independent issue (red herring)

7. **"Should we fix the payment-service network issues or auth-service database first?"**
   - Expected: Auth-service DB is priority (root cause)

8. **"List all the problems in order of when they first appeared"**
   - Expected: 
     1. auth-service slow DB queries
     2. cache-service memory issues
     3. payment-service network issues
     4. auth-service connection pool exhaustion
     5. Cascading failures

### Level 4: Actionable Insights

9. **"What specific action should we take to prevent this from happening again?"**
   - Expected: Optimize database queries, add indexes, increase connection pool

10. **"If we only had time to fix ONE thing right now, what should it be and why?"**
    - Expected: Auth-service database performance (root cause)

## Scoring
- **Basic (1-2 correct)**: Identifies symptoms
- **Good (3-5 correct)**: Finds root cause
- **Excellent (6-8 correct)**: Distinguishes root cause from red herrings
- **Expert (9-10 correct)**: Provides actionable insights with prioritization

## Current AI Performance
✓ Identified auth-service as problematic
✓ Recognized cascading failures
? Needs deeper analysis to find database root cause
? Needs to distinguish from red herrings
