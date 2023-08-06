Object.defineProperty(exports, "__esModule", { value: true });
exports.makeRuleDetailsQuery = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const details_1 = require("app/views/alerts/details");
const constants_1 = require("../rules/details/constants");
const types_1 = require("../types");
const utils_1 = require("../utils");
/**
 * Retrieve the start/end for showing the graph of the metric
 * Will show at least 150 and no more than 10,000 data points
 */
const makeRuleDetailsQuery = (incident) => {
    const { timeWindow } = incident.alertRule;
    const timeWindowMillis = timeWindow * 60 * 1000;
    const minRange = timeWindowMillis * constants_1.API_INTERVAL_POINTS_MIN;
    const maxRange = timeWindowMillis * constants_1.API_INTERVAL_POINTS_LIMIT;
    const now = moment_1.default.utc();
    const startDate = moment_1.default.utc(incident.dateStarted);
    // make a copy of now since we will modify endDate and use now for comparing
    const endDate = incident.dateClosed ? moment_1.default.utc(incident.dateClosed) : (0, moment_1.default)(now);
    const incidentRange = Math.max(endDate.diff(startDate), 3 * timeWindowMillis);
    const range = Math.min(maxRange, Math.max(minRange, incidentRange));
    const halfRange = moment_1.default.duration(range / 2);
    return {
        start: (0, dates_1.getUtcDateString)(startDate.subtract(halfRange)),
        end: (0, dates_1.getUtcDateString)(moment_1.default.min(endDate.add(halfRange), now)),
    };
};
exports.makeRuleDetailsQuery = makeRuleDetailsQuery;
class AlertListRow extends react_1.Component {
    constructor() {
        super(...arguments);
        /**
         * Memoized function to find a project from a list of projects
         */
        this.getProject = (0, memoize_1.default)((slug, projects) => projects.find(project => project.slug === slug));
    }
    get metricPreset() {
        const { incident } = this.props;
        return incident ? (0, utils_1.getIncidentMetricPreset)(incident) : undefined;
    }
    render() {
        var _a, _b, _c;
        const { incident, projectsLoaded, projects, organization } = this.props;
        const slug = incident.projects[0];
        const started = (0, moment_1.default)(incident.dateStarted);
        const duration = moment_1.default
            .duration((0, moment_1.default)(incident.dateClosed || new Date()).diff(started))
            .as('seconds');
        const alertLink = {
            pathname: (0, details_1.alertDetailsLink)(organization, incident),
            query: { alert: incident.identifier },
        };
        const ownerId = (_a = incident.alertRule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        let teamName = '';
        if (ownerId) {
            teamName = (_c = (_b = teamStore_1.default.getById(ownerId)) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
        }
        const teamActor = ownerId
            ? { type: 'team', id: ownerId, name: teamName }
            : null;
        return (<errorBoundary_1.default>
        <Title>
          <link_1.default to={alertLink}>{incident.title}</link_1.default>
        </Title>

        <NoWrapNumeric>
          {(0, getDynamicText_1.default)({
                value: <timeSince_1.default date={incident.dateStarted} extraShort/>,
                fixed: '1w ago',
            })}
        </NoWrapNumeric>
        <NoWrapNumeric>
          {incident.status === types_1.IncidentStatus.CLOSED ? (<duration_1.default seconds={(0, getDynamicText_1.default)({ value: duration, fixed: 1200 })}/>) : (<tag_1.default type="warning">{(0, locale_1.t)('Still Active')}</tag_1.default>)}
        </NoWrapNumeric>

        <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug } : this.getProject(slug, projects)}/>
        <NoWrapNumeric>#{incident.id}</NoWrapNumeric>

        <FlexCenter>
          {teamActor ? (<react_1.Fragment>
              <StyledActorAvatar actor={teamActor} size={24} hasTooltip={false}/>{' '}
              <TeamWrapper>{teamActor.name}</TeamWrapper>
            </react_1.Fragment>) : ('-')}
        </FlexCenter>
      </errorBoundary_1.default>);
    }
}
const Title = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  min-width: 130px;
`;
const NoWrapNumeric = (0, styled_1.default)('div') `
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
`;
const ProjectBadge = (0, styled_1.default)(idBadge_1.default) `
  flex-shrink: 0;
`;
const FlexCenter = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  display: flex;
  align-items: center;
`;
const TeamWrapper = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default}
`;
const StyledActorAvatar = (0, styled_1.default)(actorAvatar_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = AlertListRow;
//# sourceMappingURL=row.jsx.map