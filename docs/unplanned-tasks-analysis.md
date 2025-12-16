# Unplanned Tasks Analysis

This document provides analysis and recommendations for the unplanned tasks in the project backlog.

## Task U-1: Prometheus + Grafana Observability Dashboards

### Status
- **Priority**: Medium (correctly marked)
- **Required**: No - explicitly deferred (Option B in earlier conversation)
- **Value**: High for production, but not required for assignment

### Analysis
**Pros:**
- Provides visual dashboards for metrics already exposed at `/api/metrics`
- Production-ready observability stack
- Makes metrics more accessible than raw Prometheus format
- Good demonstration of production practices

**Cons:**
- Not required by assignment (requirements say "basic metrics", not dashboards)
- Adds complexity to Docker Compose setup
- Time investment (1.5-2h) for non-required feature
- Metrics are already accessible at `/api/metrics` endpoint

### Recommendation
**Defer or Optional Enhancement**
- The assignment requires "basic metrics" which are already implemented
- Prometheus/Grafana is an enhancement beyond "basic"
- Good to have for production, but not a requirement gap
- Can be added later if time permits

---

## Task U-2: Implement Partial/Substring Tag Matching in Search

### Status
- **Priority**: Medium (correctly marked)
- **Required**: No - current exact matching works
- **Value**: Medium - UX consistency improvement

### Analysis
**Pros:**
- Improves UX consistency (title/description use partial matching, tags don't)
- Makes tag filtering more user-friendly
- Easy to implement (already filtering in Python)
- Backward compatible (exact matches still work)

**Cons:**
- Current exact matching is functional
- Not a requirement gap
- Minor UX improvement, not critical

### Recommendation
**Nice-to-Have Enhancement**
- Low effort (0.5-1h) for good UX improvement
- Would make the filtering experience more consistent
- Can be implemented quickly if desired
- Not blocking anything

---

## Task U-3: Implement UI Smoke Tests (E2E Tests)

### Status
- **Priority**: High (correctly marked)
- **Required**: **YES** - Required by `docs/requirements.md` Section 11: Tests
- **Value**: High - Required deliverable

### Analysis
**Current State:**
- Directory structure exists: `frontend/tests/e2e/README.md`
- No actual tests implemented
- Marked as "Not yet implemented" in deliverables checklist

**Requirement:**
- `docs/requirements.md` Section 11 explicitly lists "UI smoke tests" as required
- `docs/deliverables-checklist.md` shows it as "Not yet implemented"

**Pros:**
- Required by assignment
- Validates critical user flows work end-to-end
- Catches integration issues between frontend and backend
- Demonstrates thorough testing approach

**Cons:**
- Requires setup time (Playwright/Cypress configuration)
- Requires writing test cases
- More time investment than U-1 or U-2

### Recommendation
**Should Implement - Required Deliverable**
- This is a **requirement gap**, not an optional enhancement
- Section 11 of requirements explicitly requires "UI smoke tests"
- Currently marked as incomplete in deliverables checklist
- Should be prioritized to complete all deliverables

**Suggested Approach:**
1. Choose testing framework (Playwright recommended - modern, fast, good DX)
2. Set up basic configuration
3. Implement tests for critical flows:
   - Login flow
   - Create task flow
   - View task detail
   - Upload attachment
   - Search/filter tasks
4. Keep tests simple but comprehensive (smoke tests, not full E2E suite)

---

## Summary & Recommendations

### Priority Order

1. **U-3: UI Smoke Tests** ⚠️ **HIGH PRIORITY**
   - **Status**: Required deliverable, not implemented
   - **Action**: Should implement to complete all deliverables
   - **Effort**: Medium (2-3h for basic smoke tests)

2. **U-2: Partial Tag Matching** 💡 **NICE-TO-HAVE**
   - **Status**: UX improvement, not required
   - **Action**: Implement if time permits (low effort, good UX)
   - **Effort**: Low (0.5-1h)

3. **U-1: Prometheus + Grafana** 📊 **OPTIONAL**
   - **Status**: Enhancement beyond requirements
   - **Action**: Defer unless specifically requested
   - **Effort**: Medium (1.5-2h)

### Final Recommendation

**Focus on U-3** to complete all required deliverables. The assignment explicitly requires UI smoke tests, and they're currently missing.

U-2 is a quick win if you have 30-60 minutes - it improves UX consistency with minimal effort.

U-1 can be deferred - it's beyond the "basic observability" requirement and adds complexity without being required.
