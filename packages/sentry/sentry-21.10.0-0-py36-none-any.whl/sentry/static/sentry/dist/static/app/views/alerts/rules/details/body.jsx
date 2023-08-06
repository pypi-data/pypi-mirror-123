Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const keyValueTable_1 = require("app/components/keyValueTable");
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const parser_1 = require("app/components/searchSyntax/parser");
const renderer_1 = (0, tslib_1.__importDefault)(require("app/components/searchSyntax/renderer"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const types_1 = require("app/views/alerts/incidentRules/types");
const getEventTypeFilter_1 = require("app/views/alerts/incidentRules/utils/getEventTypeFilter");
const timeline_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/rules/details/timeline"));
const alertBadge_1 = (0, tslib_1.__importDefault)(require("../../alertBadge"));
const types_2 = require("../../types");
const constants_1 = require("./constants");
const metricChart_1 = (0, tslib_1.__importDefault)(require("./metricChart"));
const relatedIssues_1 = (0, tslib_1.__importDefault)(require("./relatedIssues"));
const relatedTransactions_1 = (0, tslib_1.__importDefault)(require("./relatedTransactions"));
class DetailsBody extends React.Component {
    getMetricText() {
        const { rule } = this.props;
        if (!rule) {
            return '';
        }
        const { aggregate } = rule;
        return (0, locale_1.tct)('[metric]', {
            metric: aggregate,
        });
    }
    getTimeWindow() {
        const { rule } = this.props;
        if (!rule) {
            return '';
        }
        const { timeWindow } = rule;
        return (0, locale_1.tct)('[window]', {
            window: <duration_1.default seconds={timeWindow * 60}/>,
        });
    }
    getInterval() {
        const { timePeriod: { start, end }, rule, } = this.props;
        const startDate = moment_1.default.utc(start);
        const endDate = moment_1.default.utc(end);
        const timeWindow = rule === null || rule === void 0 ? void 0 : rule.timeWindow;
        if (timeWindow &&
            endDate.diff(startDate) < constants_1.API_INTERVAL_POINTS_LIMIT * timeWindow * 60 * 1000) {
            return `${timeWindow}m`;
        }
        return (0, utils_1.getInterval)({ start, end }, 'high');
    }
    getFilter() {
        const { rule } = this.props;
        const { dataset, query } = rule !== null && rule !== void 0 ? rule : {};
        if (!rule) {
            return null;
        }
        const eventType = dataset === types_1.Dataset.SESSIONS ? null : (0, getEventTypeFilter_1.extractEventTypeFilterFromRule)(rule);
        const parsedQuery = (0, parser_1.parseSearch)([eventType, query].join(' ').trim());
        return (<Filters>
        {query || eventType ? (<renderer_1.default parsedQuery={parsedQuery !== null && parsedQuery !== void 0 ? parsedQuery : []}/>) : (<notAvailable_1.default />)}
      </Filters>);
    }
    renderTrigger(trigger) {
        const { rule } = this.props;
        if (!rule) {
            return null;
        }
        const status = trigger.label === 'critical' ? (<StatusWrapper>
          <icons_1.IconFire color="red300" size="sm"/> Critical
        </StatusWrapper>) : trigger.label === 'warning' ? (<StatusWrapper>
          <icons_1.IconWarning color="yellow300" size="sm"/> Warning
        </StatusWrapper>) : (<StatusWrapper>
          <icons_1.IconCheckmark color="green300" size="sm" isCircled/> Resolved
        </StatusWrapper>);
        const thresholdTypeText = rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE ? (0, locale_1.t)('above') : (0, locale_1.t)('below');
        return (<TriggerCondition>
        {status}
        <TriggerText>{`${thresholdTypeText} ${trigger.alertThreshold}`}</TriggerText>
      </TriggerCondition>);
    }
    renderRuleDetails() {
        var _a, _b, _c;
        const { rule } = this.props;
        if (rule === undefined) {
            return <placeholder_1.default height="200px"/>;
        }
        const criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(({ label }) => label === 'critical');
        const warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(({ label }) => label === 'warning');
        const ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        const teamActor = ownerId && { type: 'team', id: ownerId, name: '' };
        return (<React.Fragment>
        <SidebarGroup>
          <Heading>{(0, locale_1.t)('Metric')}</Heading>
          <RuleText>{this.getMetricText()}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{(0, locale_1.t)('Environment')}</Heading>
          <RuleText>{(_b = rule.environment) !== null && _b !== void 0 ? _b : 'All'}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{(0, locale_1.t)('Filters')}</Heading>
          {this.getFilter()}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{(0, locale_1.t)('Conditions')}</Heading>
          {criticalTrigger && this.renderTrigger(criticalTrigger)}
          {warningTrigger && this.renderTrigger(warningTrigger)}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{(0, locale_1.t)('Other Details')}</Heading>
          <keyValueTable_1.KeyValueTable>
            <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Team')} value={teamActor ? <actorAvatar_1.default actor={teamActor} size={24}/> : 'Unassigned'}/>

            {rule.createdBy && (<keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Created By')} value={<CreatedBy>{(_c = rule.createdBy.name) !== null && _c !== void 0 ? _c : '-'}</CreatedBy>}/>)}

            {rule.dateModified && (<keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Last Modified')} value={<timeSince_1.default date={rule.dateModified} suffix={(0, locale_1.t)('ago')}/>}/>)}
          </keyValueTable_1.KeyValueTable>
        </SidebarGroup>
      </React.Fragment>);
    }
    renderMetricStatus() {
        const { incidents } = this.props;
        // get current status
        const activeIncident = incidents === null || incidents === void 0 ? void 0 : incidents.find(({ dateClosed }) => !dateClosed);
        const status = activeIncident ? activeIncident.status : types_2.IncidentStatus.CLOSED;
        const latestIncident = (incidents === null || incidents === void 0 ? void 0 : incidents.length) ? incidents[0] : null;
        // The date at which the alert was triggered or resolved
        const activityDate = activeIncident
            ? activeIncident.dateStarted
            : latestIncident
                ? latestIncident.dateClosed
                : null;
        return (<StatusContainer>
        <HeaderItem>
          <Heading noMargin>{(0, locale_1.t)('Current Status')}</Heading>
          <Status>
            <alertBadge_1.default status={status} hideText/>
            {activeIncident ? (0, locale_1.t)('Triggered') : (0, locale_1.t)('Resolved')}
            {activityDate ? <timeSince_1.default date={activityDate}/> : ''}
          </Status>
        </HeaderItem>
      </StatusContainer>);
    }
    renderLoading() {
        return (<Layout.Body>
        <Layout.Main>
          <placeholder_1.default height="38px"/>
          <ChartPanel>
            <panels_1.PanelBody withPadding>
              <placeholder_1.default height="200px"/>
            </panels_1.PanelBody>
          </ChartPanel>
        </Layout.Main>
        <Layout.Side>
          <placeholder_1.default height="200px"/>
        </Layout.Side>
      </Layout.Body>);
    }
    render() {
        const { api, rule, incidents, location, organization, timePeriod, selectedIncident, handleZoom, params: { orgId }, } = this.props;
        if (!rule) {
            return this.renderLoading();
        }
        const { query, projects: projectSlugs, dataset } = rule;
        const queryWithTypeFilter = `${query} ${(0, getEventTypeFilter_1.extractEventTypeFilterFromRule)(rule)}`.trim();
        return (<projects_1.default orgId={orgId} slugs={projectSlugs}>
        {({ initiallyLoaded, projects }) => {
                return initiallyLoaded ? (<React.Fragment>
              {selectedIncident &&
                        selectedIncident.alertRule.status === types_2.AlertRuleStatus.SNAPSHOT && (<StyledLayoutBody>
                    <StyledAlert type="warning" icon={<icons_1.IconInfo size="md"/>}>
                      {(0, locale_1.t)('Alert Rule settings have been updated since this alert was triggered.')}
                    </StyledAlert>
                  </StyledLayoutBody>)}
              <StyledLayoutBodyWrapper>
                <Layout.Main>
                  <HeaderContainer>
                    <HeaderGrid>
                      <HeaderItem>
                        <Heading noMargin>{(0, locale_1.t)('Display')}</Heading>
                        <ChartControls>
                          <dropdownControl_1.default label={timePeriod.display}>
                            {constants_1.TIME_OPTIONS.map(({ label, value }) => (<dropdownControl_1.DropdownItem key={value} eventKey={value} isActive={!timePeriod.custom && timePeriod.period === value} onSelect={this.props.handleTimePeriodChange}>
                                {label}
                              </dropdownControl_1.DropdownItem>))}
                          </dropdownControl_1.default>
                        </ChartControls>
                      </HeaderItem>
                      {projects && projects.length && (<HeaderItem>
                          <Heading noMargin>{(0, locale_1.t)('Project')}</Heading>

                          <idBadge_1.default avatarSize={16} project={projects[0]}/>
                        </HeaderItem>)}
                      <HeaderItem>
                        <Heading noMargin>
                          {(0, locale_1.t)('Time Interval')}
                          <tooltip_1.default title={(0, locale_1.t)('The time window over which the metric is evaluated.')}>
                            <icons_1.IconInfo size="xs" color="gray200"/>
                          </tooltip_1.default>
                        </Heading>

                        <RuleText>{this.getTimeWindow()}</RuleText>
                      </HeaderItem>
                    </HeaderGrid>
                  </HeaderContainer>

                  <metricChart_1.default api={api} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} organization={organization} projects={projects} interval={this.getInterval()} filter={this.getFilter()} query={dataset === types_1.Dataset.SESSIONS ? query : queryWithTypeFilter} orgId={orgId} handleZoom={handleZoom}/>
                  <DetailWrapper>
                    <ActivityWrapper>
                      {[types_1.Dataset.SESSIONS, types_1.Dataset.ERRORS].includes(dataset) && (<relatedIssues_1.default organization={organization} rule={rule} projects={(projects || []).filter(project => rule.projects.includes(project.slug))} timePeriod={timePeriod} query={dataset === types_1.Dataset.ERRORS
                            ? queryWithTypeFilter
                            : dataset === types_1.Dataset.SESSIONS
                                ? `${query} error.unhandled:true`
                                : undefined}/>)}
                      {dataset === types_1.Dataset.TRANSACTIONS && (<relatedTransactions_1.default organization={organization} location={location} rule={rule} projects={(projects || []).filter(project => rule.projects.includes(project.slug))} start={timePeriod.start} end={timePeriod.end} filter={(0, getEventTypeFilter_1.extractEventTypeFilterFromRule)(rule)}/>)}
                    </ActivityWrapper>
                  </DetailWrapper>
                </Layout.Main>
                <Layout.Side>
                  {this.renderMetricStatus()}
                  <timeline_1.default api={api} organization={organization} rule={rule} incidents={incidents}/>
                  {this.renderRuleDetails()}
                </Layout.Side>
              </StyledLayoutBodyWrapper>
            </React.Fragment>) : (<placeholder_1.default height="200px"/>);
            }}
      </projects_1.default>);
    }
}
exports.default = DetailsBody;
const SidebarGroup = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const DetailWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    flex-direction: column-reverse;
  }
`;
const StatusWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  svg {
    margin-right: ${(0, space_1.default)(0.5)};
  }
`;
const HeaderContainer = (0, styled_1.default)('div') `
  height: 60px;
  display: flex;
  flex-direction: row;
  align-content: flex-start;
`;
const HeaderGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto auto auto;
  align-items: stretch;
  grid-gap: 60px;
`;
const HeaderItem = (0, styled_1.default)('div') `
  flex: 1;
  display: flex;
  flex-direction: column;

  > *:nth-child(2) {
    flex: 1;
    display: flex;
    align-items: center;
  }
`;
const StyledLayoutBody = (0, styled_1.default)(Layout.Body) `
  flex-grow: 0;
  padding-bottom: 0 !important;
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: auto;
  }
`;
const StyledLayoutBodyWrapper = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -${(0, space_1.default)(3)};
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: 0;
`;
const ActivityWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
`;
const Status = (0, styled_1.default)('div') `
  position: relative;
  display: grid;
  grid-template-columns: auto auto auto;
  grid-gap: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeLarge};
`;
const StatusContainer = (0, styled_1.default)('div') `
  height: 60px;
  display: flex;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const Heading = (0, styled_1.default)(styles_1.SectionHeading) `
  display: grid;
  grid-template-columns: auto auto;
  justify-content: flex-start;
  margin-top: ${p => (p.noMargin ? 0 : (0, space_1.default)(2))};
  margin-bottom: ${(0, space_1.default)(0.5)};
  line-height: 1;
  gap: ${(0, space_1.default)(1)};
`;
const ChartControls = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  align-items: center;
`;
const ChartPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-top: ${(0, space_1.default)(2)};
`;
const RuleText = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
`;
const Filters = (0, styled_1.default)('span') `
  overflow-wrap: break-word;
  word-break: break-word;
  white-space: pre-wrap;
  font-size: ${p => p.theme.fontSizeSmall};

  line-height: 25px;
  font-family: ${p => p.theme.text.familyMono};
`;
const TriggerCondition = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const TriggerText = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(0.5)};
  white-space: nowrap;
`;
const CreatedBy = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
`;
//# sourceMappingURL=body.jsx.map