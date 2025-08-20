# Stages & Steps

## Thread types → initial stage
| thread_type | module     | stage           |
|-------------|------------|-----------------|
| company     | *home*      | company_ready   |
| product     | *home*      | product_ready   |
| module      | home       | onboarding      |
| module      | social     | social_ready    |
| module      | analytics  | analytics_ready |
| *fallback*  | *any*      | onboarding      |

## Stage checklists
### onboarding
- [ ] greet and set expectations
- [ ] collect user_id/company_id in state
- [ ] branch to company/product on command

### company_ready
- [ ] load company profile into state.context
- [ ] confirm required fields
- [ ] hand off to company_agent

### product_ready
- [ ] load product into state.context
- [ ] validate product_id present
- [ ] hand off to product_agent

### social_ready
- [ ] verify social tokens present
- [ ] fetch pages summary
- [ ] set stage → social_active

### analytics_ready
- [ ] verify GA/analytics connection
- [ ] pull last 7d summary
- [ ] set stage → analytics_active
