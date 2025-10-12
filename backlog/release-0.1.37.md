# Release 0.1.37

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

**Enhanced Multi-Agent Workflows** - Extended agent coordination and new workflow patterns

Building on the router foundation from v0.1.36, this release extends multi-agent collaboration patterns and introduces new systematic workflows for common investment tasks.

**Extended `/analyze` Workflow**:
- Add News Sentry for material events and insider trading alerts
- Add Risk Shield for portfolio fit and concentration risk analysis
- Add Tax Scout for tax implications of buying/selling positions
- Complete bottom-up → top-down → risk → news → tax pipeline

**New Workflow: `/discover`** - Systematic Idea Generation:
- Screen Forge identifies candidates matching investment criteria
- Quill performs deep fundamental analysis on shortlist
- Risk Shield assesses portfolio fit and concentration
- Atlas provides strategic allocation recommendations
- Notionist catalogs research and investment theses

**New Workflow: `/optimize-tax`** - Tax-Loss Harvesting:
- Tax Scout identifies tax-loss harvesting opportunities
- Hedge Smith suggests replacement positions to maintain exposure
- Rebalance Bot executes tax-efficient rebalancing
- Complete tax optimization pipeline with wash-sale compliance

**New Workflow: `/protect`** - Portfolio Hedging:
- Risk Shield analyzes portfolio exposures and vulnerabilities
- Hedge Smith designs protective options strategies
- Atlas evaluates hedging cost vs portfolio protection
- Complete hedging workflow with multiple strategy options

**Workflow Orchestration Improvements**:
- Better parallel execution coordination
- Progress tracking for multi-step workflows
- Workflow result synthesis across agents
- Error recovery and partial completion handling

---

## Technical Improvements

**Workflow Engine** (Planned):
- [ ] Create workflow orchestration layer for complex multi-agent sequences
- [ ] Implement workflow state management and checkpointing
- [ ] Add workflow progress visualization in TUI
- [ ] Build workflow templates for common investment tasks

**Extended `/analyze` Workflow** (Planned):
- [ ] Integrate News Sentry for material event detection
- [ ] Integrate Risk Shield for portfolio risk assessment
- [ ] Integrate Tax Scout for tax implications analysis
- [ ] Add workflow result synthesis across all agents

**New Workflows** (Planned):
- [ ] Implement `/discover` systematic idea generation workflow
- [ ] Implement `/optimize-tax` tax-loss harvesting workflow
- [ ] Implement `/protect` portfolio hedging workflow
- [ ] Add workflow documentation and examples

**Documentation Updates** (Planned):
- [ ] Update `docs/user-guide/multi-agent-workflows.md` - New workflows
- [ ] Update `docs/user-guide/getting-started.md` - Workflow examples
- [ ] Create `docs/architecture/workflows.md` - Workflow design patterns
- [ ] Update `README.md` - New workflow capabilities

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
