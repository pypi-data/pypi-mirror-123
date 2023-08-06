Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const types_1 = require("app/views/alerts/incidentRules/types");
const alertBadge_1 = (0, tslib_1.__importDefault)(require("../alertBadge"));
const types_2 = require("../types");
const utils_1 = require("../utils");
class RuleListRow extends React.Component {
    constructor() {
        super(...arguments);
        /**
         * Memoized function to find a project from a list of projects
         */
        this.getProject = (0, memoize_1.default)((slug, projects) => projects.find(project => project.slug === slug));
    }
    activeIncident() {
        var _a;
        const { rule } = this.props;
        return (((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) !== undefined &&
            [types_2.IncidentStatus.CRITICAL, types_2.IncidentStatus.WARNING].includes(rule.latestIncident.status));
    }
    renderLastIncidentDate() {
        const { rule } = this.props;
        if ((0, utils_1.isIssueAlert)(rule)) {
            return null;
        }
        if (!rule.latestIncident) {
            return '-';
        }
        if (this.activeIncident()) {
            return (<div>
          {(0, locale_1.t)('Triggered ')}
          <timeSince_1.default date={rule.latestIncident.dateCreated}/>
        </div>);
        }
        return (<div>
        {(0, locale_1.t)('Resolved ')}
        <timeSince_1.default date={rule.latestIncident.dateClosed}/>
      </div>);
    }
    renderAlertRuleStatus() {
        var _a, _b;
        const { rule } = this.props;
        if ((0, utils_1.isIssueAlert)(rule)) {
            return null;
        }
        const activeIncident = this.activeIncident();
        const criticalTrigger = rule.triggers.find(({ label }) => label === 'critical');
        const warningTrigger = rule.triggers.find(({ label }) => label === 'warning');
        const resolvedTrigger = rule.resolveThreshold;
        const trigger = activeIncident && ((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) === types_2.IncidentStatus.CRITICAL
            ? criticalTrigger
            : warningTrigger !== null && warningTrigger !== void 0 ? warningTrigger : criticalTrigger;
        let iconColor = 'green300';
        let iconDirection;
        let thresholdTypeText = activeIncident && rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE
            ? (0, locale_1.t)('Above')
            : (0, locale_1.t)('Below');
        if (activeIncident) {
            iconColor =
                (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'critical'
                    ? 'red300'
                    : (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'warning'
                        ? 'yellow300'
                        : 'green300';
            iconDirection = rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE ? 'up' : 'down';
        }
        else {
            // Use the Resolved threshold type, which is opposite of Critical
            iconDirection = rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE ? 'down' : 'up';
            thresholdTypeText =
                rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE ? (0, locale_1.t)('Below') : (0, locale_1.t)('Above');
        }
        return (<FlexCenter>
        <icons_1.IconArrow color={iconColor} direction={iconDirection}/>
        <TriggerText>
          {`${thresholdTypeText} ${rule.latestIncident || (!rule.latestIncident && !resolvedTrigger)
                ? (_b = trigger === null || trigger === void 0 ? void 0 : trigger.alertThreshold) === null || _b === void 0 ? void 0 : _b.toLocaleString()
                : resolvedTrigger === null || resolvedTrigger === void 0 ? void 0 : resolvedTrigger.toLocaleString()}`}
        </TriggerText>
      </FlexCenter>);
    }
    render() {
        var _a, _b, _c, _d;
        const { rule, projectsLoaded, projects, orgId, onDelete, userTeams } = this.props;
        const slug = rule.projects[0];
        const editLink = `/organizations/${orgId}/alerts/${(0, utils_1.isIssueAlert)(rule) ? 'rules' : 'metric-rules'}/${slug}/${rule.id}/`;
        const detailsLink = `/organizations/${orgId}/alerts/rules/details/${rule.id}/`;
        const ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        const teamActor = ownerId
            ? { type: 'team', id: ownerId, name: '' }
            : null;
        const canEdit = ownerId ? userTeams.has(ownerId) : true;
        const alertLink = (0, utils_1.isIssueAlert)(rule) ? (rule.name) : (<TitleLink to={(0, utils_1.isIssueAlert)(rule) ? editLink : detailsLink}>{rule.name}</TitleLink>);
        const IssueStatusText = {
            [types_2.IncidentStatus.CRITICAL]: (0, locale_1.t)('Critical'),
            [types_2.IncidentStatus.WARNING]: (0, locale_1.t)('Warning'),
            [types_2.IncidentStatus.CLOSED]: (0, locale_1.t)('Resolved'),
            [types_2.IncidentStatus.OPENED]: (0, locale_1.t)('Resolved'),
        };
        return (<errorBoundary_1.default>
        <AlertNameWrapper isIssueAlert={(0, utils_1.isIssueAlert)(rule)}>
          <FlexCenter>
            <tooltip_1.default title={(0, utils_1.isIssueAlert)(rule)
                ? (0, locale_1.t)('Issue Alert')
                : (0, locale_1.tct)('Metric Alert Status: [status]', {
                    status: IssueStatusText[(_c = (_b = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _b === void 0 ? void 0 : _b.status) !== null && _c !== void 0 ? _c : types_2.IncidentStatus.CLOSED],
                })}>
              <alertBadge_1.default status={(_d = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _d === void 0 ? void 0 : _d.status} isIssue={(0, utils_1.isIssueAlert)(rule)} hideText/>
            </tooltip_1.default>
          </FlexCenter>
          <AlertNameAndStatus>
            <AlertName>{alertLink}</AlertName>
            {!(0, utils_1.isIssueAlert)(rule) && this.renderLastIncidentDate()}
          </AlertNameAndStatus>
        </AlertNameWrapper>
        <FlexCenter>{this.renderAlertRuleStatus()}</FlexCenter>

        <FlexCenter>
          <ProjectBadgeContainer>
            <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug } : this.getProject(slug, projects)}/>
          </ProjectBadgeContainer>
        </FlexCenter>

        <FlexCenter>
          {teamActor ? <actorAvatar_1.default actor={teamActor} size={24}/> : '-'}
        </FlexCenter>

        <FlexCenter>
          <StyledDateTime date={(0, getDynamicText_1.default)({
                value: rule.dateCreated,
                fixed: new Date('2021-04-20'),
            })} format="ll"/>
        </FlexCenter>
        <ActionsRow>
          <access_1.default access={['alerts:write']}>
            {({ hasAccess }) => (<React.Fragment>
                <StyledDropdownLink>
                  <dropdownLink_1.default anchorRight caret={false} title={<button_1.default tooltipProps={{
                        containerDisplayMode: 'flex',
                    }} size="small" type="button" aria-label={(0, locale_1.t)('Show more')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
                    <li>
                      <link_1.default to={editLink}>{(0, locale_1.t)('Edit')}</link_1.default>
                    </li>
                    <confirm_1.default disabled={!hasAccess || !canEdit} message={(0, locale_1.tct)("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                    name: rule.name,
                })} header={(0, locale_1.t)('Delete Alert Rule?')} priority="danger" confirmText={(0, locale_1.t)('Delete Rule')} onConfirm={() => onDelete(slug, rule)}>
                      <menuItemActionLink_1.default title={(0, locale_1.t)('Delete')}>
                        {(0, locale_1.t)('Delete')}
                      </menuItemActionLink_1.default>
                    </confirm_1.default>
                  </dropdownLink_1.default>
                </StyledDropdownLink>

                {/* Small screen actions */}
                <StyledButtonBar gap={1}>
                  <confirm_1.default disabled={!hasAccess || !canEdit} message={(0, locale_1.tct)("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                    name: rule.name,
                })} header={(0, locale_1.t)('Delete Alert Rule?')} priority="danger" confirmText={(0, locale_1.t)('Delete Rule')} onConfirm={() => onDelete(slug, rule)}>
                    <button_1.default type="button" icon={<icons_1.IconDelete />} size="small" title={(0, locale_1.t)('Delete')}/>
                  </confirm_1.default>
                  <tooltip_1.default title={(0, locale_1.t)('Edit')}>
                    <button_1.default size="small" type="button" icon={<icons_1.IconSettings />} to={editLink}/>
                  </tooltip_1.default>
                </StyledButtonBar>
              </React.Fragment>)}
          </access_1.default>
        </ActionsRow>
      </errorBoundary_1.default>);
    }
}
const TitleLink = (0, styled_1.default)(link_1.default) `
  ${overflowEllipsis_1.default}
`;
const FlexCenter = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const AlertNameWrapper = (0, styled_1.default)(FlexCenter) `
  ${p => p.isIssueAlert && `padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(2)}; line-height: 2.4;`}
`;
const AlertNameAndStatus = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  margin-left: ${(0, space_1.default)(1.5)};
  line-height: 1.35;
`;
const AlertName = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  font-size: ${p => p.theme.fontSizeLarge};

  @media (max-width: ${p => p.theme.breakpoints[3]}) {
    max-width: 300px;
  }
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    max-width: 165px;
  }
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    max-width: 100px;
  }
`;
const ProjectBadgeContainer = (0, styled_1.default)('div') `
  width: 100%;
`;
const ProjectBadge = (0, styled_1.default)(idBadge_1.default) `
  flex-shrink: 0;
`;
const StyledDateTime = (0, styled_1.default)(dateTime_1.default) `
  font-variant-numeric: tabular-nums;
`;
const TriggerText = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  display: none;
  justify-content: flex-start;
  align-items: center;

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    display: flex;
  }
`;
const StyledDropdownLink = (0, styled_1.default)('div') `
  display: none;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    display: block;
  }
`;
const ActionsRow = (0, styled_1.default)(FlexCenter) `
  justify-content: center;
  padding: ${(0, space_1.default)(1)};
`;
exports.default = RuleListRow;
//# sourceMappingURL=row.jsx.map