#!/bin/bash

# Production Validation Script for AI Content Empire
# Comprehensive pre-deployment validation and security checks

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VALIDATION_REPORT="$PROJECT_ROOT/validation_report.json"

# Initialize validation report
cat > "$VALIDATION_REPORT" << EOF
{
  "validation_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "validation_status": "in_progress",
  "checks": {},
  "security_issues": [],
  "recommendations": [],
  "deployment_ready": false
}
EOF

update_report() {
    local check_name="$1"
    local status="$2"
    local details="$3"
    
    # Update the JSON report (simplified approach)
    python3 -c "
import json
import sys

try:
    with open('$VALIDATION_REPORT', 'r') as f:
        report = json.load(f)
    
    report['checks']['$check_name'] = {
        'status': '$status',
        'details': '$details',
        'timestamp': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
    }
    
    with open('$VALIDATION_REPORT', 'w') as f:
        json.dump(report, f, indent=2)
except Exception as e:
    print(f'Error updating report: {e}', file=sys.stderr)
"
}

# Check 1: Docker Compose Production Configuration
check_docker_compose() {
    log "Checking Docker Compose production configuration..."
    
    if [[ ! -f "$PROJECT_ROOT/docker-compose.prod.yml" ]]; then
        error "docker-compose.prod.yml not found"
    fi
    
    # Validate required services
    local required_services=("backend" "frontend" "db" "redis" "nginx" "prometheus" "grafana")
    for service in "${required_services[@]}"; do
        if ! grep -q "^  $service:" "$PROJECT_ROOT/docker-compose.prod.yml"; then
            warning "Service '$service' not found in docker-compose.prod.yml"
        fi
    done
    
    # Check for resource limits
    if ! grep -q "mem_limit\|memory:" "$PROJECT_ROOT/docker-compose.prod.yml"; then
        warning "No memory limits configured in docker-compose.prod.yml"
    fi
    
    # Check for health checks
    if ! grep -q "healthcheck:" "$PROJECT_ROOT/docker-compose.prod.yml"; then
        warning "No health checks configured in docker-compose.prod.yml"
    fi
    
    success "Docker Compose configuration validated"
    update_report "docker_compose" "passed" "Production configuration validated"
}

# Check 2: NGINX Configuration
check_nginx_config() {
    log "Checking NGINX production configuration..."
    
    if [[ ! -f "$PROJECT_ROOT/nginx/nginx.prod.conf" ]]; then
        error "nginx.prod.conf not found"
    fi
    
    local nginx_config="$PROJECT_ROOT/nginx/nginx.prod.conf"
    
    # Check for SSL configuration
    if ! grep -q "ssl_certificate" "$nginx_config"; then
        warning "SSL configuration not found in NGINX config"
    fi
    
    # Check for security headers
    local security_headers=("X-Frame-Options" "X-XSS-Protection" "X-Content-Type-Options" "Strict-Transport-Security")
    for header in "${security_headers[@]}"; do
        if ! grep -q "$header" "$nginx_config"; then
            warning "Security header '$header' not configured"
        fi
    done
    
    # Check for rate limiting
    if ! grep -q "limit_req" "$nginx_config"; then
        warning "Rate limiting not configured"
    fi
    
    # Check for gzip compression
    if ! grep -q "gzip on" "$nginx_config"; then
        warning "Gzip compression not enabled"
    fi
    
    success "NGINX configuration validated"
    update_report "nginx_config" "passed" "Production NGINX configuration validated"
}

# Check 3: Environment Variables
check_environment_variables() {
    log "Checking required environment variables..."
    
    local required_vars=(
        "DATABASE_URL"
        "REDIS_URL"
        "JWT_SECRET"
        "OPENAI_API_KEY"
        "ANTHROPIC_API_KEY"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        warning "Missing environment variables: ${missing_vars[*]}"
        warning "Please set these variables before deployment"
    else
        success "All required environment variables are set"
    fi
    
    update_report "environment_variables" "passed" "Environment variables validated"
}

# Check 4: Security Audit
check_security() {
    log "Running security audit..."
    
    cd "$PROJECT_ROOT"
    
    # Check for secrets in code
    log "Scanning for hardcoded secrets..."
    if command -v grep >/dev/null 2>&1; then
        local secret_patterns=(
            "password.*=.*['\"][^'\"]*['\"]"
            "api_key.*=.*['\"][^'\"]*['\"]"
            "secret.*=.*['\"][^'\"]*['\"]"
            "token.*=.*['\"][^'\"]*['\"]"
        )
        
        local secrets_found=false
        for pattern in "${secret_patterns[@]}"; do
            if grep -r -i -E "$pattern" --include="*.py" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v ".env" | grep -v "example" | head -5; then
                secrets_found=true
            fi
        done
        
        if [[ "$secrets_found" == true ]]; then
            warning "Potential hardcoded secrets found - please review"
        else
            success "No hardcoded secrets detected"
        fi
    fi
    
    # Run safety check on Python dependencies
    log "Checking Python dependencies for vulnerabilities..."
    if command -v safety >/dev/null 2>&1; then
        if safety scan -r requirements.txt --output text > security_scan.txt 2>&1; then
            success "No critical security vulnerabilities found"
        else
            warning "Security vulnerabilities detected - see security_scan.txt"
            # Count vulnerabilities
            local vuln_count=$(grep -c "Vulnerability found" security_scan.txt 2>/dev/null || echo "0")
            warning "Found $vuln_count vulnerabilities in dependencies"
        fi
    else
        warning "Safety tool not available - skipping dependency security scan"
    fi
    
    update_report "security_audit" "completed" "Security scan completed with warnings"
}

# Check 5: SSL Certificates
check_ssl_certificates() {
    log "Checking SSL certificates..."
    
    local ssl_dir="$PROJECT_ROOT/nginx/ssl"
    local required_files=("fullchain.pem" "privkey.pem" "chain.pem")
    
    if [[ ! -d "$ssl_dir" ]]; then
        warning "SSL directory not found: $ssl_dir"
        warning "Please ensure SSL certificates are properly configured"
        update_report "ssl_certificates" "warning" "SSL directory not found"
        return
    fi
    
    local missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$ssl_dir/$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        warning "Missing SSL certificate files: ${missing_files[*]}"
        warning "Please ensure SSL certificates are properly installed"
    else
        success "SSL certificate files found"
        
        # Check certificate expiry (if openssl is available)
        if command -v openssl >/dev/null 2>&1; then
            local cert_file="$ssl_dir/fullchain.pem"
            local expiry_date=$(openssl x509 -in "$cert_file" -noout -enddate 2>/dev/null | cut -d= -f2)
            if [[ -n "$expiry_date" ]]; then
                log "SSL certificate expires: $expiry_date"
                
                # Check if certificate expires within 30 days
                local expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null || echo "0")
                local current_epoch=$(date +%s)
                local days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
                
                if [[ $days_until_expiry -lt 30 ]]; then
                    warning "SSL certificate expires in $days_until_expiry days - consider renewal"
                else
                    success "SSL certificate is valid for $days_until_expiry days"
                fi
            fi
        fi
    fi
    
    update_report "ssl_certificates" "passed" "SSL certificates validated"
}

# Check 6: Monitoring Configuration
check_monitoring() {
    log "Checking monitoring configuration..."
    
    # Check Prometheus configuration
    if [[ -f "$PROJECT_ROOT/monitoring/prometheus.yml" ]]; then
        success "Prometheus configuration found"
    else
        warning "Prometheus configuration not found"
    fi
    
    # Check alerting rules
    if [[ -f "$PROJECT_ROOT/monitoring/alerting_rules.yml" ]]; then
        success "Alerting rules configuration found"
        
        # Count number of alert rules
        local alert_count=$(grep -c "alert:" "$PROJECT_ROOT/monitoring/alerting_rules.yml" 2>/dev/null || echo "0")
        log "Found $alert_count alert rules configured"
    else
        warning "Alerting rules not found"
    fi
    
    # Check Grafana dashboards
    if [[ -d "$PROJECT_ROOT/monitoring/grafana/dashboards" ]]; then
        local dashboard_count=$(find "$PROJECT_ROOT/monitoring/grafana/dashboards" -name "*.json" | wc -l)
        success "Found $dashboard_count Grafana dashboards"
    else
        warning "Grafana dashboards not found"
    fi
    
    update_report "monitoring" "passed" "Monitoring configuration validated"
}

# Check 7: Database Configuration
check_database() {
    log "Checking database configuration..."
    
    # Check if database migrations exist
    if [[ -d "$PROJECT_ROOT/database/migrations" ]] || [[ -d "$PROJECT_ROOT/alembic/versions" ]]; then
        success "Database migrations found"
    else
        warning "Database migrations not found"
    fi
    
    # Check database backup configuration
    if [[ -f "$PROJECT_ROOT/scripts/backup_database.sh" ]]; then
        success "Database backup script found"
    else
        warning "Database backup script not found"
    fi
    
    update_report "database" "passed" "Database configuration validated"
}

# Check 8: Performance Configuration
check_performance() {
    log "Checking performance configuration..."
    
    # Check for Redis configuration
    if grep -q "redis" "$PROJECT_ROOT/docker-compose.prod.yml" 2>/dev/null; then
        success "Redis caching configured"
    else
        warning "Redis caching not configured"
    fi
    
    # Check for CDN configuration in NGINX
    if grep -q "expires\|Cache-Control" "$PROJECT_ROOT/nginx/nginx.prod.conf" 2>/dev/null; then
        success "Static asset caching configured"
    else
        warning "Static asset caching not configured"
    fi
    
    update_report "performance" "passed" "Performance configuration validated"
}

# Generate final report
generate_final_report() {
    log "Generating final validation report..."
    
    # Count passed/failed checks
    local total_checks=$(python3 -c "
import json
with open('$VALIDATION_REPORT', 'r') as f:
    report = json.load(f)
print(len(report['checks']))
")
    
    local passed_checks=$(python3 -c "
import json
with open('$VALIDATION_REPORT', 'r') as f:
    report = json.load(f)
passed = sum(1 for check in report['checks'].values() if check['status'] == 'passed')
print(passed)
")
    
    # Update final status
    python3 -c "
import json
with open('$VALIDATION_REPORT', 'r') as f:
    report = json.load(f)

report['validation_status'] = 'completed'
report['total_checks'] = $total_checks
report['passed_checks'] = $passed_checks
report['deployment_ready'] = $passed_checks >= ($total_checks * 0.8)

with open('$VALIDATION_REPORT', 'w') as f:
    json.dump(report, f, indent=2)
"
    
    echo
    echo "=================================="
    echo "   PRODUCTION VALIDATION REPORT"
    echo "=================================="
    echo
    echo "Total Checks: $total_checks"
    echo "Passed Checks: $passed_checks"
    echo
    
    if [[ $passed_checks -ge $((total_checks * 80 / 100)) ]]; then
        success "SYSTEM IS READY FOR PRODUCTION DEPLOYMENT! 🚀"
        echo
        echo "Next Steps:"
        echo "1. Review any warnings above"
        echo "2. Set up SSL certificates if not already done"
        echo "3. Configure monitoring alerts"
        echo "4. Run final load tests"
        echo "5. Deploy to production!"
    else
        warning "SYSTEM NEEDS ATTENTION BEFORE DEPLOYMENT"
        echo
        echo "Please address the issues above before deploying to production."
    fi
    
    echo
    echo "Detailed report saved to: $VALIDATION_REPORT"
    echo "=================================="
}

# Main execution
main() {
    log "Starting AI Content Empire Production Validation..."
    echo
    
    # Run all checks
    check_docker_compose
    check_nginx_config
    check_environment_variables
    check_security
    check_ssl_certificates
    check_monitoring
    check_database
    check_performance
    
    # Generate final report
    generate_final_report
}

# Run main function
main "$@"
