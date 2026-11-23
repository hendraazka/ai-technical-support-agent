
# Runbook: Connection Timeout

## Incident ID
INC-001

## Category
Network / Application Connectivity

## Symptoms
- Application reports connection timeout.
- API request exceeds configured timeout.
- Service cannot connect to a downstream dependency.
- Error code: ETIMEDOUT.

## Possible Root Causes
1. Target service is unavailable.
2. Network connectivity issue.
3. Firewall blocks the connection.
4. Downstream service is overloaded.
5. Application timeout configuration is too low.

## Investigation Steps
1. Check whether the target service is running.
2. Check network connectivity between services.
3. Inspect application and service logs.
4. Check CPU and memory utilization.
5. Check downstream service response time.
6. Review firewall and network policies.

## Recommended Actions
1. Verify target service availability.
2. Check network connectivity.
3. Review timeout configuration.
4. Escalate to the network team if connectivity fails.
5. Escalate to the application team if the downstream service is overloaded.

## Escalation Criteria
Escalate when:
- Timeout persists for more than 5 minutes.
- Multiple services are affected.
- The downstream service remains unavailable.
- Initial investigation cannot identify the cause.

## Important Notes
Do not restart production services without authorization.
Do not expose passwords, tokens, API keys, or other sensitive data in incident reports.

