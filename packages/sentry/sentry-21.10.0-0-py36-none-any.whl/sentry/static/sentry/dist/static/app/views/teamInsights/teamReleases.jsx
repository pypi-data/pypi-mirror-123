Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const chunk_1 = (0, tslib_1.__importDefault)(require("lodash/chunk"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class TeamReleases extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { weekReleases: null, periodReleases: null });
    }
    getEndpoints() {
        const { organization, start, end, period, utc, teamSlug } = this.props;
        const datetime = { start, end, period, utc };
        const endpoints = [
            [
                'periodReleases',
                `/teams/${organization.slug}/${teamSlug}/release-count/`,
                {
                    query: Object.assign({}, (0, getParams_1.getParams)(datetime)),
                },
            ],
            [
                'weekReleases',
                `/teams/${organization.slug}/${teamSlug}/release-count/`,
                {
                    query: {
                        statsPeriod: '7d',
                    },
                },
            ],
        ];
        return endpoints;
    }
    componentDidUpdate(prevProps) {
        const { teamSlug, start, end, period, utc } = this.props;
        if (prevProps.start !== start ||
            prevProps.end !== end ||
            prevProps.period !== period ||
            prevProps.utc !== utc ||
            !(0, isEqual_1.default)(prevProps.teamSlug, teamSlug)) {
            this.remountComponent();
        }
    }
    getReleaseCount(projectId, dataset) {
        const { periodReleases, weekReleases } = this.state;
        const releasesPeriod = dataset === 'week' ? weekReleases === null || weekReleases === void 0 ? void 0 : weekReleases.last_week_totals : periodReleases === null || periodReleases === void 0 ? void 0 : periodReleases.project_avgs;
        const count = (releasesPeriod === null || releasesPeriod === void 0 ? void 0 : releasesPeriod[projectId])
            ? Math.ceil(releasesPeriod === null || releasesPeriod === void 0 ? void 0 : releasesPeriod[projectId])
            : 0;
        return count;
    }
    getTrend(projectId) {
        const periodCount = this.getReleaseCount(projectId, 'period');
        const weekCount = this.getReleaseCount(projectId, 'week');
        if (periodCount === null || weekCount === null) {
            return null;
        }
        return weekCount - periodCount;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderReleaseCount(projectId, dataset) {
        const { loading } = this.state;
        if (loading) {
            return (<div>
          <placeholder_1.default width="80px" height="25px"/>
        </div>);
        }
        const count = this.getReleaseCount(Number(projectId), dataset);
        if (count === null) {
            return '\u2014';
        }
        return count;
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
        {`${(0, round_1.default)(Math.abs(trend), 3)}`}
        <PaddedIconArrow direction={trend >= 0 ? 'up' : 'down'} size="xs"/>
      </SubText>);
    }
    renderBody() {
        var _a, _b;
        const { projects, period } = this.props;
        const { periodReleases } = this.state;
        const data = Object.entries((_a = periodReleases === null || periodReleases === void 0 ? void 0 : periodReleases.release_counts) !== null && _a !== void 0 ? _a : {})
            .map(([bucket, count]) => ({
            value: Math.ceil(count),
            name: new Date(bucket).getTime(),
        }))
            .sort((a, b) => a.name - b.name);
        const projectAvgData = Object.values((_b = periodReleases === null || periodReleases === void 0 ? void 0 : periodReleases.project_avgs) !== null && _b !== void 0 ? _b : {}).reduce((total, currentData) => total + currentData, 0);
        // Convert from days to 7 day groups
        const seriesData = (0, chunk_1.default)(data, 7).map(week => {
            return {
                name: week[0].name,
                value: week.reduce((total, currentData) => total + currentData.value, 0),
            };
        });
        const prevSeriesData = (0, chunk_1.default)(data, 7).map(week => {
            return {
                name: week[0].name,
                value: Math.ceil(projectAvgData / projects.length),
            };
        });
        return (<div>
        <ChartWrapper>
          <StyledBarChart style={{ height: 190 }} isGroupedByDate useShortDate period="7d" legend={{ right: 3, top: 0 }} yAxis={{ minInterval: 1 }} xAxis={{
                type: 'time',
            }} series={[
                {
                    seriesName: (0, locale_1.t)('This Period'),
                    data: seriesData,
                },
            ]} previousPeriod={[
                {
                    seriesName: (0, locale_1.t)(`Last ${period} Average`),
                    data: prevSeriesData !== null && prevSeriesData !== void 0 ? prevSeriesData : [],
                },
            ]}/>
        </ChartWrapper>
        <StyledPanelTable isEmpty={projects.length === 0} headers={[
                (0, locale_1.t)('Project'),
                <RightAligned key="last">
              {(0, locale_1.tct)('Last [period] Average', { period })}
            </RightAligned>,
                <RightAligned key="curr">{(0, locale_1.t)('This Week')}</RightAligned>,
                <RightAligned key="diff">{(0, locale_1.t)('Difference')}</RightAligned>,
            ]}>
          {projects.map(project => (<react_1.Fragment key={project.id}>
              <ProjectBadgeContainer>
                <ProjectBadge avatarSize={18} project={project}/>
              </ProjectBadgeContainer>

              <ScoreWrapper>{this.renderReleaseCount(project.id, 'period')}</ScoreWrapper>
              <ScoreWrapper>{this.renderReleaseCount(project.id, 'week')}</ScoreWrapper>
              <ScoreWrapper>{this.renderTrend(project.id)}</ScoreWrapper>
            </react_1.Fragment>))}
        </StyledPanelTable>
      </div>);
    }
}
exports.default = TeamReleases;
const ChartWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const StyledBarChart = (0, styled_1.default)(barChart_1.default) ``;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: 1fr 0.2fr 0.2fr 0.2fr;
  white-space: nowrap;
  margin-bottom: 0;
  border: 0;
  font-size: ${p => p.theme.fontSizeMedium};
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
//# sourceMappingURL=teamReleases.jsx.map