#!/bin/bash
# ============================================================
# Zia Properties - Agent Portal Setup Script
# Run this from your project root directory
# ============================================================

set -e  # Exit on error

echo "=========================================="
echo "  Zia Properties Agent Portal Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "ERROR: Please run this script from your Django project root"
    exit 1
fi

TEMPLATES_DIR="frontend/templates/frontend"
VIEWS_FILE="frontend/views.py"
URLS_FILE="frontend/urls.py"

echo "[1/7] Creating agent portal templates..."

# ============================================================
# AGENT TENANTS TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_tenants.html" << 'TENANTSEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}My Tenants{% endblock %}
{% block page_title %}My <span>Tenants</span>{% endblock %}

{% block top_actions %}
<a href="#" class="btn btn-primary"><i class="fas fa-plus"></i> Add Tenant</a>
{% endblock %}

{% block content %}
<div class="card">
  <div class="card-header">
    <div class="card-title">All Tenants ({{ total_count }})</div>
    <form method="get" class="filter-bar" style="margin: 0;">
      <input type="text" name="search" class="search-box" placeholder="Search tenants..." value="{{ request.GET.search }}">
    </form>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Tenant</th>
        <th>Property</th>
        <th>Phone</th>
        <th>Status</th>
        <th>Verified</th>
        <th>Joined</th>
      </tr>
    </thead>
    <tbody>
      {% for tenant in tenants %}
      <tr>
        <td>
          <div class="tenant-info">
            <div class="tenant-avatar">{{ tenant.property_name|slice:":1"|upper }}</div>
            <div>
              <div class="tenant-name">{{ tenant.property_name }}</div>
              <div class="tenant-email">{{ tenant.email }}</div>
            </div>
          </div>
        </td>
        <td>{{ tenant.property_name }}</td>
        <td>{{ tenant.phone }}</td>
        <td>
          <span class="status-badge {% if tenant.is_active %}active{% else %}pending{% endif %}">
            <span class="status-dot {% if tenant.is_active %}active{% else %}pending{% endif %}"></span>
            {% if tenant.is_active %}Active{% else %}Inactive{% endif %}
          </span>
        </td>
        <td>
          {% if tenant.is_verified %}
          <span style="color: var(--success);"><i class="fas fa-check-circle"></i></span>
          {% else %}
          <span style="color: var(--text-secondary);"><i class="fas fa-clock"></i></span>
          {% endif %}
        </td>
        <td style="color: var(--text-secondary);">{{ tenant.created_at|date:"M d, Y" }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 3rem;">No tenants found. <a href="#" style="color: var(--primary-light);">Add your first tenant</a></td></tr>
      {% endfor %}
    </tbody>
  </table>

  {% if tenants.has_other_pages %}
  <div class="pagination">
    {% if tenants.has_previous %}
    <a href="?page={{ tenants.previous_page_number }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}"><i class="fas fa-chevron-left"></i></a>
    {% endif %}
    {% for num in tenants.paginator.page_range %}
    {% if tenants.number == num %}
    <span class="current">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}">{{ num }}</a>
    {% endif %}
    {% endfor %}
    {% if tenants.has_next %}
    <a href="?page={{ tenants.next_page_number }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}"><i class="fas fa-chevron-right"></i></a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
TENANTSEOF

echo "  ✓ agent_tenants.html"

# ============================================================
# AGENT LEASES TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_leases.html" << 'LEASESEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}My Leases{% endblock %}
{% block page_title %}My <span>Leases</span>{% endblock %}

{% block top_actions %}
<a href="#" class="btn btn-primary"><i class="fas fa-plus"></i> Create Lease</a>
{% endblock %}

{% block content %}
<div class="stats-grid" style="margin-bottom: 1.5rem;">
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem;">{{ total_count }}</div>
    <div class="stat-label">Total Leases</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--success);">{{ active_count }}</div>
    <div class="stat-label">Active</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--accent-warm);">{{ ending_soon_count }}</div>
    <div class="stat-label">Ending Soon</div>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <div class="card-title">All Leases</div>
    <form method="get" class="filter-bar" style="margin: 0;">
      <select name="status" class="filter-select" onchange="this.form.submit()">
        <option value="">All Status</option>
        <option value="active" {% if request.GET.status == 'active' %}selected{% endif %}>Active</option>
        <option value="expired" {% if request.GET.status == 'expired' %}selected{% endif %}>Expired</option>
      </select>
    </form>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Tenant</th>
        <th>Property</th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Rent Amount</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {% for lease in leases %}
      <tr>
        <td>
          <div class="tenant-info">
            <div class="tenant-avatar">{{ lease.tenant.property_name|slice:":1"|upper }}</div>
            <div>
              <div class="tenant-name">{{ lease.tenant.property_name }}</div>
              <div class="tenant-email">{{ lease.tenant.email }}</div>
            </div>
          </div>
        </td>
        <td>{{ lease.property.property_name }}</td>
        <td>{{ lease.start_date|date:"M d, Y" }}</td>
        <td>{{ lease.end_date|date:"M d, Y" }}</td>
        <td style="font-weight: 600;">KES {{ lease.rent_amount|floatformat:2 }}</td>
        <td>
          <span class="status-badge {% if lease.is_active %}active{% else %}pending{% endif %}">
            <span class="status-dot {% if lease.is_active %}active{% else %}pending{% endif %}"></span>
            {% if lease.is_active %}Active{% else %}Expired{% endif %}
          </span>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 3rem;">No leases found. <a href="#" style="color: var(--primary-light);">Create your first lease</a></td></tr>
      {% endfor %}
    </tbody>
  </table>

  {% if leases.has_other_pages %}
  <div class="pagination">
    {% if leases.has_previous %}
    <a href="?page={{ leases.previous_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-left"></i></a>
    {% endif %}
    {% for num in leases.paginator.page_range %}
    {% if leases.number == num %}
    <span class="current">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}">{{ num }}</a>
    {% endif %}
    {% endfor %}
    {% if leases.has_next %}
    <a href="?page={{ leases.next_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-right"></i></a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
LEASESEOF

echo "  ✓ agent_leases.html"

# ============================================================
# AGENT PAYMENTS TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_payments.html" << 'PAYMENTSEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}Payments{% endblock %}
{% block page_title %}Payment <span>History</span>{% endblock %}

{% block content %}
<div class="stats-grid" style="margin-bottom: 1.5rem;">
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--success);">KES {{ total_revenue|floatformat:0 }}</div>
    <div class="stat-label">Total Revenue</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--accent);">KES {{ monthly_revenue|floatformat:0 }}</div>
    <div class="stat-label">This Month</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem;">{{ total_count }}</div>
    <div class="stat-label">Total Payments</div>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <div class="card-title">All Payments</div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Tenant</th>
        <th>Property</th>
        <th>Amount</th>
        <th>Method</th>
        <th>Receipt</th>
        <th>Date</th>
      </tr>
    </thead>
    <tbody>
      {% for payment in payments %}
      <tr>
        <td>
          <div class="tenant-info">
            <div class="tenant-avatar">{{ payment.tenant.property_name|slice:":1"|upper }}</div>
            <div>
              <div class="tenant-name">{{ payment.tenant.property_name }}</div>
              <div class="tenant-email">{{ payment.tenant.email }}</div>
            </div>
          </div>
        </td>
        <td>{{ payment.lease.property.property_name }}</td>
        <td style="font-weight: 600; color: var(--success);">KES {{ payment.amount_paid|floatformat:2 }}</td>
        <td>{{ payment.payment_method|title }}</td>
        <td><code style="background: var(--bg-dark); padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.8rem;">{{ payment.receipt_number }}</code></td>
        <td style="color: var(--text-secondary);">{{ payment.payment_date|date:"M d, Y" }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 3rem;">No payments found.</td></tr>
      {% endfor %}
    </tbody>
  </table>

  {% if payments.has_other_pages %}
  <div class="pagination">
    {% if payments.has_previous %}
    <a href="?page={{ payments.previous_page_number }}"><i class="fas fa-chevron-left"></i></a>
    {% endif %}
    {% for num in payments.paginator.page_range %}
    {% if payments.number == num %}
    <span class="current">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}">{{ num }}</a>
    {% endif %}
    {% endfor %}
    {% if payments.has_next %}
    <a href="?page={{ payments.next_page_number }}"><i class="fas fa-chevron-right"></i></a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
PAYMENTSEOF

echo "  ✓ agent_payments.html"

# ============================================================
# AGENT MAINTENANCE TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_maintenance.html" << 'MAINTENANCEEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}Maintenance{% endblock %}
{% block page_title %}Maintenance <span>Requests</span>{% endblock %}

{% block top_actions %}
<a href="#" class="btn btn-primary"><i class="fas fa-plus"></i> New Request</a>
{% endblock %}

{% block content %}
<div class="stats-grid" style="margin-bottom: 1.5rem;">
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--accent-warm);">{{ pending_count }}</div>
    <div class="stat-label">Pending</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--accent);">{{ in_progress_count }}</div>
    <div class="stat-label">In Progress</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--success);">{{ resolved_count }}</div>
    <div class="stat-label">Resolved</div>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <div class="card-title">All Requests ({{ total_count }})</div>
    <form method="get" class="filter-bar" style="margin: 0;">
      <select name="status" class="filter-select" onchange="this.form.submit()">
        <option value="">All Status</option>
        <option value="pending" {% if request.GET.status == 'pending' %}selected{% endif %}>Pending</option>
        <option value="in_progress" {% if request.GET.status == 'in_progress' %}selected{% endif %}>In Progress</option>
        <option value="resolved" {% if request.GET.status == 'resolved' %}selected{% endif %}>Resolved</option>
      </select>
    </form>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Property</th>
        <th>Issue</th>
        <th>Status</th>
        <th>Requested</th>
      </tr>
    </thead>
    <tbody>
      {% for req in maintenance %}
      <tr>
        <td>{{ req.property.property_name }}</td>
        <td>{{ req.issue|truncatechars:50 }}</td>
        <td>
          <span class="status-badge {{ req.status }}">
            <span class="status-dot {{ req.status }}"></span>
            {{ req.status|title }}
          </span>
        </td>
        <td style="color: var(--text-secondary);">{{ req.requested_on|date:"M d, Y" }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="4" style="text-align: center; color: var(--text-secondary); padding: 3rem;">No maintenance requests found.</td></tr>
      {% endfor %}
    </tbody>
  </table>

  {% if maintenance.has_other_pages %}
  <div class="pagination">
    {% if maintenance.has_previous %}
    <a href="?page={{ maintenance.previous_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-left"></i></a>
    {% endif %}
    {% for num in maintenance.paginator.page_range %}
    {% if maintenance.number == num %}
    <span class="current">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}">{{ num }}</a>
    {% endif %}
    {% endfor %}
    {% if maintenance.has_next %}
    <a href="?page={{ maintenance.next_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-right"></i></a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
MAINTENANCEEOF

echo "  ✓ agent_maintenance.html"

# ============================================================
# AGENT INSPECTIONS TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_inspections.html" << 'INSPECTIONSEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}Inspections{% endblock %}
{% block page_title %}Property <span>Inspections</span>{% endblock %}

{% block top_actions %}
<a href="#" class="btn btn-primary"><i class="fas fa-plus"></i> Schedule Inspection</a>
{% endblock %}

{% block content %}
<div class="stats-grid" style="margin-bottom: 1.5rem;">
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--accent-warm);">{{ scheduled_count }}</div>
    <div class="stat-label">Scheduled</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem; color: var(--success);">{{ completed_count }}</div>
    <div class="stat-label">Completed</div>
  </div>
  <div class="stat-card" style="padding: 1rem;">
    <div class="stat-value" style="font-size: 1.5rem;">{{ total_count }}</div>
    <div class="stat-label">Total</div>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <div class="card-title">All Inspections</div>
    <form method="get" class="filter-bar" style="margin: 0;">
      <select name="status" class="filter-select" onchange="this.form.submit()">
        <option value="">All Status</option>
        <option value="scheduled" {% if request.GET.status == 'scheduled' %}selected{% endif %}>Scheduled</option>
        <option value="completed" {% if request.GET.status == 'completed' %}selected{% endif %}>Completed</option>
        <option value="canceled" {% if request.GET.status == 'canceled' %}selected{% endif %}>Canceled</option>
      </select>
    </form>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Property</th>
        <th>Inspector</th>
        <th>Date</th>
        <th>Status</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      {% for inspection in inspections %}
      <tr>
        <td>{{ inspection.property.property_name }}</td>
        <td>{{ inspection.inspector_name }}</td>
        <td>{{ inspection.inspection_date|date:"M d, Y" }}</td>
        <td>
          <span class="status-badge {{ inspection.status }}">
            <span class="status-dot {{ inspection.status }}"></span>
            {{ inspection.status|title }}
          </span>
        </td>
        <td style="color: var(--text-secondary);">{{ inspection.notes|truncatechars:40 }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="5" style="text-align: center; color: var(--text-secondary); padding: 3rem;">No inspections found. <a href="#" style="color: var(--primary-light);">Schedule your first inspection</a></td></tr>
      {% endfor %}
    </tbody>
  </table>

  {% if inspections.has_other_pages %}
  <div class="pagination">
    {% if inspections.has_previous %}
    <a href="?page={{ inspections.previous_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-left"></i></a>
    {% endif %}
    {% for num in inspections.paginator.page_range %}
    {% if inspections.number == num %}
    <span class="current">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}">{{ num }}</a>
    {% endif %}
    {% endfor %}
    {% if inspections.has_next %}
    <a href="?page={{ inspections.next_page_number }}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}"><i class="fas fa-chevron-right"></i></a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
INSPECTIONSEOF

echo "  ✓ agent_inspections.html"

# ============================================================
# AGENT ANALYTICS TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_analytics.html" << 'ANALYTICSEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}Analytics{% endblock %}
{% block page_title %}Performance <span>Analytics</span>{% endblock %}

{% block content %}
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-header">
      <div class="stat-icon blue"><i class="fas fa-home"></i></div>
    </div>
    <div class="stat-value">{{ total_properties }}</div>
    <div class="stat-label">Properties</div>
  </div>
  <div class="stat-card">
    <div class="stat-header">
      <div class="stat-icon green"><i class="fas fa-users"></i></div>
    </div>
    <div class="stat-value">{{ total_tenants }}</div>
    <div class="stat-label">Tenants</div>
  </div>
  <div class="stat-card">
    <div class="stat-header">
      <div class="stat-icon orange"><i class="fas fa-percentage"></i></div>
    </div>
    <div class="stat-value">{{ occupancy_rate }}%</div>
    <div class="stat-label">Occupancy Rate</div>
  </div>
  <div class="stat-card">
    <div class="stat-header">
      <div class="stat-icon cyan"><i class="fas fa-money-bill-wave"></i></div>
    </div>
    <div class="stat-value">KES {{ total_revenue|floatformat:0 }}</div>
    <div class="stat-label">Total Revenue</div>
  </div>
</div>

<div class="stats-grid" style="grid-template-columns: 2fr 1fr;">
  <div class="card">
    <div class="card-header">
      <div class="card-title">Monthly Revenue Trend</div>
    </div>
    <div style="position: relative; height: 350px;">
      <canvas id="revenueTrendChart"></canvas>
    </div>
  </div>
  <div class="card">
    <div class="card-header">
      <div class="card-title">Properties by Type</div>
    </div>
    <div style="position: relative; height: 350px;">
      <canvas id="propertyTypeChart"></canvas>
    </div>
  </div>
</div>

<div class="card" style="margin-top: 1.25rem;">
  <div class="card-header">
    <div class="card-title">Performance Summary</div>
  </div>
  <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
    <div style="text-align: center; padding: 1.5rem;">
      <div style="font-size: 2rem; font-weight: 700; color: var(--primary-light);">KES {{ avg_rent|floatformat:0 }}</div>
      <div style="color: var(--text-secondary); margin-top: 0.5rem;">Average Rent</div>
    </div>
    <div style="text-align: center; padding: 1.5rem; border-left: 1px solid var(--border); border-right: 1px solid var(--border);">
      <div style="font-size: 2rem; font-weight: 700; color: var(--success);">{{ total_leases }}</div>
      <div style="color: var(--text-secondary); margin-top: 0.5rem;">Total Leases</div>
    </div>
    <div style="text-align: center; padding: 1.5rem;">
      <div style="font-size: 2rem; font-weight: 700; color: var(--accent);">{{ agent.commission_rate|default:0 }}%</div>
      <div style="color: var(--text-secondary); margin-top: 0.5rem;">Commission Rate</div>
    </div>
  </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
  // Revenue Trend Chart
  const monthlyData = {{ monthly_data|safe }};
  new Chart(document.getElementById('revenueTrendChart'), {
    type: 'bar',
    data: {
      labels: monthlyData.map(d => d.month),
      datasets: [{
        label: 'Revenue (KES)',
        data: monthlyData.map(d => d.revenue),
        backgroundColor: 'rgba(99, 102, 241, 0.6)',
        borderColor: '#6366f1',
        borderWidth: 2,
        borderRadius: 8,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(99, 102, 241, 0.1)' }, ticks: { color: '#94a3b8' } },
        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
      }
    }
  });

  // Property Type Chart
  const typeData = {{ properties_by_type|safe }};
  new Chart(document.getElementById('propertyTypeChart'), {
    type: 'doughnut',
    data: {
      labels: typeData.map(t => t.property_type),
      datasets: [{
        data: typeData.map(t => t.count),
        backgroundColor: ['#6366f1', '#06b6d4', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899'],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: { position: 'bottom', labels: { color: '#94a3b8', padding: 15, font: { size: 12 } } }
      }
    }
  });
</script>
{% endblock %}
ANALYTICSEOF

echo "  ✓ agent_analytics.html"

# ============================================================
# AGENT SETTINGS TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_settings.html" << 'SETTINGSEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}Settings{% endblock %}
{% block page_title %}Profile <span>Settings</span>{% endblock %}

{% block content %}
<div class="stats-grid" style="grid-template-columns: 1fr 2fr; margin-bottom: 0;">
  <!-- Profile Card -->
  <div class="card" style="text-align: center;">
    <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--accent)); margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 700; color: white;">
      {{ agent_name|slice:":2"|upper }}
    </div>
    <h3 style="font-family: 'Space Grotesk', sans-serif; margin-bottom: 0.25rem;">{{ agent_name }}</h3>
    <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">{{ agent.agent_type|title }} Agent</p>
    <div style="display: flex; justify-content: center; gap: 0.5rem;">
      <span class="status-badge active">Verified</span>
      {% if agent.is_premium %}<span class="status-badge" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-warm);"><i class="fas fa-crown"></i> Premium</span>{% endif %}
    </div>
  </div>

  <!-- Edit Form -->
  <div class="card">
    <div class="card-header">
      <div class="card-title">Edit Profile</div>
    </div>
    <form method="post" enctype="multipart/form-data">
      {% csrf_token %}
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
        <div class="form-group">
          <label>First Name</label>
          <input type="text" name="first_name" class="signup-input" value="{{ agent.first_name }}">
        </div>
        <div class="form-group">
          <label>Last Name</label>
          <input type="text" name="last_name" class="signup-input" value="{{ agent.last_name }}">
        </div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
        <div class="form-group">
          <label>Phone Number</label>
          <input type="text" name="phone_number" class="signup-input" value="{{ agent.phone_number }}">
        </div>
        <div class="form-group">
          <label>Commission Rate (%)</label>
          <input type="number" name="commission_rate" class="signup-input" value="{{ agent.commission_rate|default:'' }}" step="0.01">
        </div>
      </div>
      <div class="form-group" style="margin-bottom: 1rem;">
        <label>Bio</label>
        <textarea name="bio" class="signup-input" rows="3">{{ agent.bio|default:'' }}</textarea>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
        <div class="form-group">
          <label>Agency Name</label>
          <input type="text" name="agency_name" class="signup-input" value="{{ agent.agency_name|default:'' }}">
        </div>
        <div class="form-group">
          <label>Business Reg. No</label>
          <input type="text" name="business_reg_no" class="signup-input" value="{{ agent.business_reg_no|default:'' }}">
        </div>
      </div>
      <div class="form-group" style="margin-bottom: 1rem;">
        <label>License Number</label>
        <input type="text" name="license_no" class="signup-input" value="{{ agent.license_no|default:'' }}">
      </div>
      <div class="form-group" style="margin-bottom: 1rem;">
        <label>Physical Address</label>
        <textarea name="physical_address" class="signup-input" rows="2">{{ agent.physical_address|default:'' }}</textarea>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
        <div class="form-group">
          <label>City</label>
          <input type="text" name="city" class="signup-input" value="{{ agent.city|default:'' }}">
        </div>
        <div class="form-group">
          <label>Country</label>
          <input type="text" name="country" class="signup-input" value="{{ agent.country|default:'Kenya' }}">
        </div>
      </div>
      <button type="submit" class="btn btn-primary" style="width: 100%;">
        <i class="fas fa-save"></i> Save Changes
      </button>
    </form>
  </div>
</div>
{% endblock %}
SETTINGSEOF

echo "  ✓ agent_settings.html"

# ============================================================
# AGENT PROPERTY DETAIL TEMPLATE
# ============================================================
cat > "$TEMPLATES_DIR/agent_property_detail.html" << 'PROPERTYDETAILEOF'
{% extends 'frontend/agent_base.html' %}

{% block title %}{{ property.property_name }}{% endblock %}
{% block page_title %}Property <span>Details</span>{% endblock %}

{% block top_actions %}
<a href="{% url 'frontend:agent_properties' %}" class="btn btn-outline"><i class="fas fa-arrow-left"></i> Back</a>
{% endblock %}

{% block content %}
<div class="stats-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 0;">
  <!-- Property Info -->
  <div class="card">
    <div style="width: 100%; height: 250px; background: linear-gradient(135deg, var(--bg-card-hover), var(--bg-dark)); border-radius: 16px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: center; overflow: hidden;">
      {% if property.image %}
      <img src="{{ property.image.url }}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 16px;">
      {% else %}
      <i class="fas fa-home" style="font-size: 4rem; color: var(--text-secondary);"></i>
      {% endif %}
    </div>
    <h2 style="font-family: 'Space Grotesk', sans-serif; margin-bottom: 0.5rem;">{{ property.property_name }}</h2>
    <p style="color: var(--text-secondary); margin-bottom: 1rem;"><i class="fas fa-map-marker-alt"></i> {{ property.location }}</p>
    <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
      <span class="status-badge {% if property.is_available %}active{% else %}pending{% endif %}">
        {% if property.is_available %}Available{% else %}Rented{% endif %}
      </span>
      <span class="status-badge" style="background: rgba(99, 102, 241, 0.15); color: var(--primary-light);">
        {{ property.get_property_type_display }}
      </span>
      {% if property.is_featured %}
      <span class="status-badge" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-warm);">
        <i class="fas fa-star"></i> Featured
      </span>
      {% endif %}
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;">
      <div style="background: var(--bg-dark); padding: 1rem; border-radius: 12px;">
        <div style="font-size: 1.25rem; font-weight: 700;">{{ property.bedrooms }}</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">Bedrooms</div>
      </div>
      <div style="background: var(--bg-dark); padding: 1rem; border-radius: 12px;">
        <div style="font-size: 1.25rem; font-weight: 700;">{{ property.bathrooms }}</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">Bathrooms</div>
      </div>
      <div style="background: var(--bg-dark); padding: 1rem; border-radius: 12px;">
        <div style="font-size: 1.25rem; font-weight: 700;">{{ property.size|default:"N/A" }}</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">Size (sqm)</div>
      </div>
    </div>
    <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color: var(--text-secondary);">Price</span>
        <span style="font-size: 1.5rem; font-weight: 700; color: var(--success);">KES {{ property.price|floatformat:2 }}</span>
      </div>
    </div>
  </div>

  <!-- Side Info -->
  <div>
    <!-- Tenants -->
    <div class="card" style="margin-bottom: 1.25rem;">
      <div class="card-header">
        <div class="card-title">Current Tenants</div>
      </div>
      {% for tenant in tenants %}
      <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
        <div class="tenant-avatar">{{ tenant.property_name|slice:":1"|upper }}</div>
        <div style="flex: 1;">
          <div class="tenant-name">{{ tenant.property_name }}</div>
          <div class="tenant-email">{{ tenant.email }} | {{ tenant.phone }}</div>
        </div>
        <span class="status-badge {% if tenant.is_active %}active{% else %}pending{% endif %}">
          {% if tenant.is_active %}Active{% else %}Inactive{% endif %}
        </span>
      </div>
      {% empty %}
      <p style="color: var(--text-secondary); text-align: center; padding: 1rem;">No tenants assigned</p>
      {% endfor %}
    </div>

    <!-- Active Leases -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">Active Leases</div>
      </div>
      {% for lease in leases %}
      <div style="padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
          <span style="font-weight: 600;">KES {{ lease.rent_amount|floatformat:2 }}/month</span>
          <span style="color: var(--text-secondary); font-size: 0.85rem;">{{ lease.payment_frequency|title }}</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: var(--text-secondary); font-size: 0.85rem;">
          <span>{{ lease.start_date|date:"M d, Y" }} - {{ lease.end_date|date:"M d, Y" }}</span>
          <span class="status-badge {% if lease.is_active %}active{% else %}pending{% endif %}">
            {% if lease.is_active %}Active{% else %}Expired{% endif %}
          </span>
        </div>
      </div>
      {% empty %}
      <p style="color: var(--text-secondary); text-align: center; padding: 1rem;">No active leases</p>
      {% endfor %}
    </div>
  </div>
</div>

<!-- Maintenance History -->
<div class="card" style="margin-top: 1.25rem;">
  <div class="card-header">
    <div class="card-title">Maintenance History</div>
  </div>
  <table class="data-table">
    <thead>
      <tr>
        <th>Issue</th>
        <th>Status</th>
        <th>Date</th>
      </tr>
    </thead>
    <tbody>
      {% for req in maintenance %}
      <tr>
        <td>{{ req.issue|truncatechars:60 }}</td>
        <td>
          <span class="status-badge {{ req.status }}">
            <span class="status-dot {{ req.status }}"></span>
            {{ req.status|title }}
          </span>
        </td>
        <td style="color: var(--text-secondary);">{{ req.requested_on|date:"M d, Y" }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="3" style="text-align: center; color: var(--text-secondary);">No maintenance records</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
PROPERTYDETAILEOF

echo "  ✓ agent_property_detail.html"

echo ""
echo "[2/7] Templates created successfully!"
echo ""
echo "=========================================="
echo "  NEXT STEPS:"
echo "=========================================="
echo ""
echo "1. Make sure your views.py has all the agent portal views"
echo "2. Make sure your urls.py has all the agent portal URL patterns"
echo "3. Run: python manage.py collectstatic"
echo "4. Restart your Django server"
echo "5. Log in as an agent and test all pages"
echo ""
echo "Agent Portal URLs:"
echo "  /agent/dashboard/     - Dashboard"
echo "  /agent/properties/    - My Properties"
echo "  /agent/tenants/       - My Tenants"
echo "  /agent/leases/        - My Leases"
echo "  /agent/payments/      - Payments"
echo "  /agent/maintenance/   - Maintenance"
echo "  /agent/inspections/  - Inspections"
echo "  /agent/analytics/     - Analytics"
echo "  /agent/settings/      - Settings"
echo ""
