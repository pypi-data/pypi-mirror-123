Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const utils_1 = require("./utils");
class TeamIssuesReviewed extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { issuesBreakdown: null });
    }
    getEndpoints() {
        const { organization, start, end, period, utc, teamSlug } = this.props;
        const datetime = { start, end, period, utc };
        return [
            [
                'issuesBreakdown',
                `/teams/${organization.slug}/${teamSlug}/issue-breakdown/`,
                {
                    query: Object.assign({}, (0, getParams_1.getParams)(datetime)),
                },
            ],
        ];
    }
    componentDidUpdate(prevProps) {
        const { start, end, period, utc, teamSlug, projects } = this.props;
        if (prevProps.start !== start ||
            prevProps.end !== end ||
            prevProps.period !== period ||
            prevProps.utc !== utc ||
            prevProps.teamSlug !== teamSlug ||
            !(0, isEqual_1.default)(prevProps.projects, projects)) {
            this.remountComponent();
        }
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { issuesBreakdown, loading } = this.state;
        const { projects } = this.props;
        const allReviewedByDay = {};
        const allNotReviewedByDay = {};
        // Total reviewed & total reviewed keyed by project ID
        const projectTotals = {};
        if (issuesBreakdown) {
            // The issues breakdown is split into projectId ->
            for (const [projectId, entries] of Object.entries(issuesBreakdown)) {
                for (const [bucket, { reviewed, total }] of Object.entries(entries)) {
                    if (!projectTotals[projectId]) {
                        projectTotals[projectId] = { reviewed: 0, total: 0 };
                    }
                    projectTotals[projectId].reviewed += reviewed;
                    projectTotals[projectId].total += total;
                    if (allReviewedByDay[bucket] === undefined) {
                        allReviewedByDay[bucket] = reviewed;
                    }
                    else {
                        allReviewedByDay[bucket] += reviewed;
                    }
                    const notReviewed = total - reviewed;
                    if (allNotReviewedByDay[bucket] === undefined) {
                        allNotReviewedByDay[bucket] = notReviewed;
                    }
                    else {
                        allNotReviewedByDay[bucket] += notReviewed;
                    }
                }
            }
        }
        const reviewedSeries = (0, utils_1.convertDayValueObjectToSeries)(allReviewedByDay);
        const notReviewedSeries = (0, utils_1.convertDayValueObjectToSeries)(allNotReviewedByDay);
        return (<react_1.Fragment>
        <IssuesChartWrapper>
          {loading && <placeholder_1.default height="200px"/>}
          {!loading && (<barChart_1.default style={{ height: 200 }} stacked isGroupedByDate legend={{ right: 0, top: 0 }} series={[
                    {
                        seriesName: (0, locale_1.t)('Reviewed'),
                        data: (0, utils_1.convertDaySeriesToWeeks)(reviewedSeries),
                    },
                    {
                        seriesName: (0, locale_1.t)('Not Reviewed'),
                        data: (0, utils_1.convertDaySeriesToWeeks)(notReviewedSeries),
                    },
                ]}/>)}
        </IssuesChartWrapper>
        <StyledPanelTable headers={[
                (0, locale_1.t)('Project'),
                <AlignRight key="forReview">{(0, locale_1.t)('For Review')}</AlignRight>,
                <AlignRight key="reviewed">{(0, locale_1.t)('Reviewed')}</AlignRight>,
                <AlignRight key="change">{(0, locale_1.t)('% Reviewed')}</AlignRight>,
            ]} isLoading={loading}>
          {projects.map(project => {
                var _a;
                const { total, reviewed } = (_a = projectTotals[project.id]) !== null && _a !== void 0 ? _a : {};
                return (<react_1.Fragment key={project.id}>
                <ProjectBadgeContainer>
                  <ProjectBadge avatarSize={18} project={project}/>
                </ProjectBadgeContainer>
                <AlignRight>{total}</AlignRight>
                <AlignRight>{reviewed}</AlignRight>
                <AlignRight>
                  {total === 0 ? '\u2014' : (0, formatters_1.formatPercentage)(reviewed / total)}
                </AlignRight>
              </react_1.Fragment>);
            })}
        </StyledPanelTable>
      </react_1.Fragment>);
    }
}
exports.default = TeamIssuesReviewed;
const ChartWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(2)};
`;
const IssuesChartWrapper = (0, styled_1.default)(ChartWrapper) `
  border-bottom: 1px solid ${p => p.theme.border};
`;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: 1fr 0.2fr 0.2fr 0.2fr;
  font-size: ${p => p.theme.fontSizeMedium};
  white-space: nowrap;
  margin-bottom: 0;
  border: 0;
  box-shadow: unset;

  & > div {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }
`;
const ProjectBadgeContainer = (0, styled_1.default)('div') `
  display: flex;
`;
const ProjectBadge = (0, styled_1.default)(idBadge_1.default) `
  flex-shrink: 0;
`;
const AlignRight = (0, styled_1.default)('div') `
  text-align: right;
  font-variant-numeric: tabular-nums;
`;
//# sourceMappingURL=teamIssuesReviewed.jsx.map