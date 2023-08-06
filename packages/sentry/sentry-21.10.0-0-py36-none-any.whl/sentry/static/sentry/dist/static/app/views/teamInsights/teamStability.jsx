Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const sessions_1 = require("app/utils/sessions");
const utils_1 = require("app/views/releases/utils");
class TeamStability extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { weekSessions: null, periodSessions: null });
    }
    getEndpoints() {
        const { organization, start, end, period, utc, projects } = this.props;
        const projectsWithSessions = projects.filter(project => project.hasSessions);
        if (projectsWithSessions.length === 0) {
            return [];
        }
        const datetime = { start, end, period, utc };
        const commonQuery = {
            environment: [],
            project: projectsWithSessions.map(p => p.id),
            field: 'sum(session)',
            groupBy: ['session.status', 'project'],
            interval: '1d',
        };
        const endpoints = [
            [
                'periodSessions',
                `/organizations/${organization.slug}/sessions/`,
                {
                    query: Object.assign(Object.assign({}, commonQuery), (0, getParams_1.getParams)(datetime)),
                },
            ],
            [
                'weekSessions',
                `/organizations/${organization.slug}/sessions/`,
                {
                    query: Object.assign(Object.assign({}, commonQuery), { statsPeriod: '7d' }),
                },
            ],
        ];
        return endpoints;
    }
    componentDidUpdate(prevProps) {
        const { projects, start, end, period, utc } = this.props;
        if (prevProps.start !== start ||
            prevProps.end !== end ||
            prevProps.period !== period ||
            prevProps.utc !== utc ||
            !(0, isEqual_1.default)(prevProps.projects, projects)) {
            this.remountComponent();
        }
    }
    getScore(projectId, dataset) {
        const { periodSessions, weekSessions } = this.state;
        const sessions = dataset === 'week' ? weekSessions : periodSessions;
        const projectGroups = sessions === null || sessions === void 0 ? void 0 : sessions.groups.filter(group => group.by.project === projectId);
        return (0, sessions_1.getCrashFreeRate)(projectGroups, types_1.SessionField.SESSIONS);
    }
    getTrend(projectId) {
        const periodScore = this.getScore(projectId, 'period');
        const weekScore = this.getScore(projectId, 'week');
        if (periodScore === null || weekScore === null) {
            return null;
        }
        return weekScore - periodScore;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderScore(projectId, dataset) {
        const { loading } = this.state;
        if (loading) {
            return (<div>
          <placeholder_1.default width="80px" height="25px"/>
        </div>);
        }
        const score = this.getScore(Number(projectId), dataset);
        if (score === null) {
            return '\u2014';
        }
        return (0, utils_1.displayCrashFreePercent)(score);
    }
    renderTrend(projectId) {
        const { loading } = this.state;
        if (loading) {
            return (<div>
          <placeholder_1.default width="80px" height="25px"/>
        </div>);
        }
        const trend = this.getTrend(Number(projectId));
        if (trend === null) {
            return '\u2014';
        }
        return (<SubText color={trend >= 0 ? 'green300' : 'red300'}>
        {`${(0, round_1.default)(Math.abs(trend), 3)}\u0025`}
        <PaddedIconArrow direction={trend >= 0 ? 'up' : 'down'} size="xs"/>
      </SubText>);
    }
    renderBody() {
        const { projects, period } = this.props;
        return (<StyledPanelTable isEmpty={projects.length === 0} headers={[
                (0, locale_1.t)('Project'),
                <RightAligned key="last">{(0, locale_1.tct)('Last [period]', { period })}</RightAligned>,
                <RightAligned key="curr">{(0, locale_1.t)('This Week')}</RightAligned>,
                <RightAligned key="diff">{(0, locale_1.t)('Difference')}</RightAligned>,
            ]}>
        {projects.map(project => (<react_1.Fragment key={project.id}>
            <ProjectBadgeContainer>
              <ProjectBadge avatarSize={18} project={project}/>
            </ProjectBadgeContainer>

            <ScoreWrapper>{this.renderScore(project.id, 'period')}</ScoreWrapper>
            <ScoreWrapper>{this.renderScore(project.id, 'week')}</ScoreWrapper>
            <ScoreWrapper>{this.renderTrend(project.id)}</ScoreWrapper>
          </react_1.Fragment>))}
      </StyledPanelTable>);
    }
}
exports.default = TeamStability;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: 1fr 0.2fr 0.2fr 0.2fr;
  white-space: nowrap;
  margin-bottom: 0;
  border: 0;
  box-shadow: unset;

  & > div {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }
`;
const RightAligned = (0, styled_1.default)('span') `
  text-align: right;
`;
const ScoreWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: flex-end;
  text-align: right;
`;
const PaddedIconArrow = (0, styled_1.default)(icons_1.IconArrow) `
  margin: 0 ${(0, space_1.default)(0.5)};
`;
const SubText = (0, styled_1.default)('div') `
  color: ${p => p.theme[p.color]};
`;
const ProjectBadgeContainer = (0, styled_1.default)('div') `
  display: flex;
`;
const ProjectBadge = (0, styled_1.default)(idBadge_1.default) `
  flex-shrink: 0;
`;
//# sourceMappingURL=teamStability.jsx.map