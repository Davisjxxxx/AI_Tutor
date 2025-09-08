# 🚨 EMERGENCY ROLLBACK PROCEDURE

## **CRITICAL: Keep This Document Accessible During Deployment**

### **When to Execute Rollback**
- API error rate > 10%
- Database connection failures
- SSL/TLS certificate issues
- Memory/CPU usage > 90%
- Any critical system failure

---

## **🚀 IMMEDIATE ROLLBACK (< 5 Minutes)**

### **Step 1: Stop Current Deployment**
```bash
# Navigate to project directory
cd /path/to/Content_Creation_System

# Stop all services immediately
docker-compose -f docker-compose.prod.yml down --remove-orphans

# Verify all containers are stopped
docker ps -a | grep content-creation
```

### **Step 2: Restore Previous Version**
```bash
# List available Docker images
docker images | grep ai-content-empire

# Tag previous stable version as latest
docker tag ai-content-empire:v1.0.0 ai-content-empire:latest

# Alternative: Pull last known good version
# docker pull your-registry/ai-content-empire:v1.0.0
# docker tag your-registry/ai-content-empire:v1.0.0 ai-content-empire:latest
```

### **Step 3: Start Previous Version**
```bash
# Start services with previous version
docker-compose -f docker-compose.prod.yml up -d

# Wait 30 seconds for services to initialize
sleep 30

# Verify services are running
docker-compose -f docker-compose.prod.yml ps
```

### **Step 4: Verify System Health**
```bash
# Check API health
curl -f https://your-domain.com/health || echo "❌ API Health Check Failed"

# Check database connectivity
curl -f https://your-domain.com/api/health || echo "❌ Database Health Check Failed"

# Check SSL certificate
curl -I https://your-domain.com || echo "❌ SSL Check Failed"

# Check monitoring
curl -f http://localhost:9090/api/v1/query?query=up || echo "❌ Monitoring Check Failed"
```

---

## **🗄️ DATABASE ROLLBACK (If Required)**

### **Only if Database Schema Changes Were Made**
```bash
# List available backups
ls -la /backups/ | grep $(date +%Y-%m-%d)

# Restore from pre-deployment backup
docker exec -i postgres psql -U user -d aura_prod < /backups/pre_deployment_backup.sql

# Alternative: Restore from specific backup
# docker exec -i postgres psql -U user -d aura_prod < /backups/backup_2024-08-29_07-00.sql

# Verify database restoration
docker exec postgres psql -U user -d aura_prod -c "SELECT COUNT(*) FROM users;"
```

---

## **📊 POST-ROLLBACK VERIFICATION**

### **System Health Checks**
```bash
# 1. API Endpoints
curl -f https://your-domain.com/api/v2/system/status
curl -f https://your-domain.com/api/auth/health
curl -f https://your-domain.com/api/content/health

# 2. Database Connectivity
docker exec postgres pg_isready -U user -d aura_prod

# 3. Redis Cache
docker exec redis redis-cli ping

# 4. File System
df -h | grep -E "(/$|/var)"

# 5. Memory Usage
free -h

# 6. Load Average
uptime
```

### **Application Functionality**
```bash
# Test user authentication
curl -X POST https://your-domain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'

# Test content generation (if auth token available)
curl -X POST https://your-domain.com/api/v2/content/viral/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"topic":"test","platform":"tiktok","target_audience":"general","content_goal":"test"}'
```

---

## **📢 COMMUNICATION PROTOCOL**

### **Immediate Notifications**
```bash
# Slack notification (replace with your webhook)
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🚨 EMERGENCY ROLLBACK EXECUTED: AI Content Empire rolled back to previous version. System status: STABLE. Time: '$(date)'"}' \
  YOUR_SLACK_WEBHOOK_URL

# Email notification (if configured)
echo "Emergency rollback executed at $(date). System restored to previous stable version." | \
  mail -s "🚨 AI Content Empire - Emergency Rollback" ops-team@company.com
```

### **Status Page Update**
```bash
# Update status page (example with curl)
curl -X POST https://api.statuspage.io/v1/pages/YOUR_PAGE_ID/incidents \
  -H "Authorization: OAuth YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "incident": {
      "name": "Deployment Rollback",
      "status": "investigating",
      "impact_override": "minor",
      "body": "We have rolled back to the previous stable version due to deployment issues. Service is now stable."
    }
  }'
```

---

## **🔍 INCIDENT DOCUMENTATION**

### **Capture Evidence**
```bash
# Save deployment logs
docker-compose -f docker-compose.prod.yml logs --since="1h" > rollback_logs_$(date +%Y%m%d_%H%M%S).txt

# Save system metrics
curl -s "http://localhost:9090/api/v1/query_range?query=up&start=$(date -d '1 hour ago' -u +%Y-%m-%dT%H:%M:%SZ)&end=$(date -u +%Y-%m-%dT%H:%M:%SZ)&step=60s" > metrics_during_incident.json

# Save error logs
docker logs backend_container > backend_errors_$(date +%Y%m%d_%H%M%S).log 2>&1
```

### **Create Incident Report**
```bash
cat > incident_report_$(date +%Y%m%d_%H%M%S).md << EOF
# Incident Report: Emergency Rollback

**Date:** $(date)
**Duration:** [TO BE FILLED]
**Impact:** [TO BE FILLED]

## Timeline
- **Deployment Start:** [TO BE FILLED]
- **Issue Detected:** [TO BE FILLED]
- **Rollback Initiated:** [TO BE FILLED]
- **Service Restored:** [TO BE FILLED]

## Root Cause
[TO BE FILLED AFTER INVESTIGATION]

## Resolution
Emergency rollback to previous stable version executed successfully.

## Action Items
- [ ] Investigate root cause
- [ ] Fix identified issues
- [ ] Plan re-deployment
- [ ] Update deployment procedures
EOF
```

---

## **⚡ QUICK REFERENCE COMMANDS**

### **Emergency Stop**
```bash
docker-compose -f docker-compose.prod.yml down --remove-orphans
```

### **Emergency Start (Previous Version)**
```bash
docker tag ai-content-empire:v1.0.0 ai-content-empire:latest
docker-compose -f docker-compose.prod.yml up -d
```

### **Health Check**
```bash
curl -f https://your-domain.com/health && echo "✅ System OK" || echo "❌ System Down"
```

### **View Logs**
```bash
docker-compose -f docker-compose.prod.yml logs --tail=50 -f
```

---

## **📞 EMERGENCY CONTACTS**

### **Primary Contacts**
- **Lead Engineer:** [Name] - [Phone] - [Email]
- **DevOps Engineer:** [Name] - [Phone] - [Email]
- **On-Call Engineer:** [Phone] - [Slack: @oncall]

### **Escalation**
- **Engineering Manager:** [Name] - [Phone]
- **CTO:** [Name] - [Phone]

### **External Support**
- **Hosting Provider:** [Support Number]
- **SSL Certificate Provider:** [Support Number]
- **Database Support:** [Support Number]

---

## **🎯 SUCCESS CRITERIA**

### **Rollback is Successful When:**
- [ ] All services are running (docker-compose ps shows "Up")
- [ ] API health checks return 200 OK
- [ ] Database connections are working
- [ ] SSL certificate is valid
- [ ] Monitoring shows green status
- [ ] No error spikes in logs
- [ ] User authentication works
- [ ] Core functionality is accessible

### **Post-Rollback Actions:**
1. **Immediate (0-15 minutes):**
   - Verify system stability
   - Update status page
   - Notify stakeholders

2. **Short-term (15-60 minutes):**
   - Monitor system metrics
   - Analyze logs for issues
   - Document incident timeline

3. **Medium-term (1-24 hours):**
   - Conduct post-mortem meeting
   - Identify root cause
   - Plan remediation steps

---

## **🚨 REMEMBER**

- **Stay Calm:** Follow the procedure step by step
- **Communicate:** Keep team informed of progress
- **Document:** Capture logs and evidence
- **Verify:** Always confirm system health after rollback
- **Learn:** Conduct thorough post-mortem

**The goal is to restore service quickly and safely. Don't rush - follow the procedure.**

---

*Last Updated: $(date)*
*Version: 1.0*
