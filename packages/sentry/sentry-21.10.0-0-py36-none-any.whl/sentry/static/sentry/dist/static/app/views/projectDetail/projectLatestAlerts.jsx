Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const styles_1 = require("app/components/charts/styles");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("../alerts/types");
const missingAlertsButtons_1 = (0, tslib_1.__importDefault)(require("./missingFeatureButtons/missingAlertsButtons"));
const styles_2 = require("./styles");
const utils_1 = require("./utils");
const PLACEHOLDER_AND_EMPTY_HEIGHT = '172px';
class ProjectLatestAlerts extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.renderAlertRow = (alert) => {
            const { organization } = this.props;
            const { status, id, identifier, title, dateClosed, dateStarted } = alert;
            const isResolved = status === types_1.IncidentStatus.CLOSED;
            const isWarning = status === types_1.IncidentStatus.WARNING;
            const Icon = isResolved ? icons_1.IconCheckmark : isWarning ? icons_1.IconWarning : icons_1.IconFire;
            const statusProps = { isResolved, isWarning };
            return (<AlertRowLink to={`/organizations/${organization.slug}/alerts/${identifier}/`} key={id}>
        <AlertBadge {...statusProps} icon={Icon}>
          <AlertIconWrapper>
            <Icon color="white"/>
          </AlertIconWrapper>
        </AlertBadge>
        <AlertDetails>
          <AlertTitle>{title}</AlertTitle>
          <AlertDate {...statusProps}>
            {isResolved
                    ? (0, locale_1.tct)('Resolved [date]', {
                        date: dateClosed ? <timeSince_1.default date={dateClosed}/> : null,
                    })
                    : (0, locale_1.tct)('Triggered [date]', { date: <timeSince_1.default date={dateStarted}/> })}
          </AlertDate>
        </AlertDetails>
      </AlertRowLink>);
        };
    }
    shouldComponentUpdate(nextProps, nextState) {
        const { location, isProjectStabilized } = this.props;
        // TODO(project-detail): we temporarily removed refetching based on timeselector
        if (this.state !== nextState ||
            (0, utils_1.didProjectOrEnvironmentChange)(location, nextProps.location) ||
            isProjectStabilized !== nextProps.isProjectStabilized) {
            return true;
        }
        return false;
    }
    componentDidUpdate(prevProps) {
        const { location, isProjectStabilized } = this.props;
        if ((0, utils_1.didProjectOrEnvironmentChange)(prevProps.location, location) ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    }
    getEndpoints() {
        const { location, organization, isProjectStabilized } = this.props;
        if (!isProjectStabilized) {
            return [];
        }
        const query = Object.assign(Object.assign({}, (0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM))), { per_page: 3 });
        // we are listing 3 alerts total, first unresolved and then we fill with resolved
        return [
            [
                'unresolvedAlerts',
                `/organizations/${organization.slug}/incidents/`,
                { query: Object.assign(Object.assign({}, query), { status: 'open' }) },
            ],
            [
                'resolvedAlerts',
                `/organizations/${organization.slug}/incidents/`,
                { query: Object.assign(Object.assign({}, query), { status: 'closed' }) },
            ],
        ];
    }
    /**
     * If our alerts are empty, determine if we've configured alert rules (empty message differs then)
     */
    onLoadAllEndpointsSuccess() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { unresolvedAlerts, resolvedAlerts } = this.state;
            const { location, organization, isProjectStabilized } = this.props;
            if (!isProjectStabilized) {
                return;
            }
            if ([...(unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []), ...(resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : [])].length !== 0) {
                this.setState({ hasAlertRule: true });
                return;
            }
            this.setState({ loading: true });
            const alertRules = yield this.api.requestPromise(`/organizations/${organization.slug}/alert-rules/`, {
                method: 'GET',
                query: Object.assign(Object.assign({}, (0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM)])), { per_page: 1 }),
            });
            this.setState({ hasAlertRule: alertRules.length > 0, loading: false });
        });
    }
    get alertsLink() {
        const { organization } = this.props;
        // as this is a link to latest alerts, we want to only preserve project and environment
        return {
            pathname: `/organizations/${organization.slug}/alerts/`,
            query: {
                statsPeriod: undefined,
                start: undefined,
                end: undefined,
                utc: undefined,
            },
        };
    }
    renderInnerBody() {
        const { organization, projectSlug, isProjectStabilized } = this.props;
        const { loading, unresolvedAlerts, resolvedAlerts, hasAlertRule } = this.state;
        const alertsUnresolvedAndResolved = [
            ...(unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []),
            ...(resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : []),
        ];
        const checkingForAlertRules = alertsUnresolvedAndResolved.length === 0 && hasAlertRule === undefined;
        const showLoadingIndicator = loading || checkingForAlertRules || !isProjectStabilized;
        if (showLoadingIndicator) {
            return <placeholder_1.default height={PLACEHOLDER_AND_EMPTY_HEIGHT}/>;
        }
        if (!hasAlertRule) {
            return (<missingAlertsButtons_1.default organization={organization} projectSlug={projectSlug}/>);
        }
        if (alertsUnresolvedAndResolved.length === 0) {
            return (<StyledEmptyStateWarning small>{(0, locale_1.t)('No alerts found')}</StyledEmptyStateWarning>);
        }
        return alertsUnresolvedAndResolved.slice(0, 3).map(this.renderAlertRow);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        return (<styles_2.SidebarSection>
        <styles_2.SectionHeadingWrapper>
          <styles_1.SectionHeading>{(0, locale_1.t)('Latest Alerts')}</styles_1.SectionHeading>
          <styles_2.SectionHeadingLink to={this.alertsLink}>
            <icons_1.IconOpen />
          </styles_2.SectionHeadingLink>
        </styles_2.SectionHeadingWrapper>

        <div>{this.renderInnerBody()}</div>
      </styles_2.SidebarSection>);
    }
}
const AlertRowLink = (0, styled_1.default)(link_1.default) `
  display: flex;
  align-items: center;
  height: 40px;
  margin-bottom: ${(0, space_1.default)(3)};
  margin-left: ${(0, space_1.default)(0.5)};
  &,
  &:hover,
  &:focus {
    color: inherit;
  }
  &:first-child {
    margin-top: ${(0, space_1.default)(1)};
  }
`;
const getStatusColor = ({ theme, isResolved, isWarning, }) => isResolved ? theme.green300 : isWarning ? theme.yellow300 : theme.red300;
const AlertBadge = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  /* icon warning needs to be treated differently to look visually centered */
  line-height: ${p => (p.icon === icons_1.IconWarning ? undefined : 1)};

  &:before {
    content: '';
    width: 30px;
    height: 30px;
    border-radius: ${p => p.theme.borderRadius};
    background-color: ${p => getStatusColor(p)};
    transform: rotate(45deg);
  }
`;
const AlertIconWrapper = (0, styled_1.default)('div') `
  position: absolute;
`;
const AlertDetails = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-left: ${(0, space_1.default)(2)};
  ${overflowEllipsis_1.default}
`;
const AlertTitle = (0, styled_1.default)('div') `
  font-weight: 400;
  overflow: hidden;
  text-overflow: ellipsis;
`;
const AlertDate = (0, styled_1.default)('span') `
  color: ${p => getStatusColor(p)};
`;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  height: ${PLACEHOLDER_AND_EMPTY_HEIGHT};
  justify-content: center;
`;
exports.default = ProjectLatestAlerts;
//# sourceMappingURL=projectLatestAlerts.jsx.map