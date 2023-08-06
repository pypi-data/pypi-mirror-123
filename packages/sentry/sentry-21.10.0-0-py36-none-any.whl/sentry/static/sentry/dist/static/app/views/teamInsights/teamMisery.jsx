Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const utils_1 = require("../performance/transactionSummary/utils");
/** The number of elements to display before collapsing */
const COLLAPSE_COUNT = 8;
function TeamMisery({ organization, location, projects, periodTableData, weekTableData, isLoading, period, }) {
    var _a;
    const [isExpanded, setIsExpanded] = (0, react_1.useState)(false);
    const miseryRenderer = (periodTableData === null || periodTableData === void 0 ? void 0 : periodTableData.meta) && (0, fieldRenderers_1.getFieldRenderer)('user_misery', periodTableData.meta);
    function expandResults() {
        setIsExpanded(true);
    }
    // Calculate trend, so we can sort based on it
    const sortedTableData = ((_a = periodTableData === null || periodTableData === void 0 ? void 0 : periodTableData.data) !== null && _a !== void 0 ? _a : [])
        .map(dataRow => {
        const weekRow = weekTableData === null || weekTableData === void 0 ? void 0 : weekTableData.data.find(row => row.project === dataRow.project && row.transaction === dataRow.transaction);
        const trend = weekRow
            ? (dataRow.user_misery - weekRow.user_misery) * 100
            : null;
        return Object.assign(Object.assign({}, dataRow), { trend });
    })
        .filter(x => x.trend !== null)
        .sort((a, b) => Math.abs(b.trend) - Math.abs(a.trend));
    const worseItems = sortedTableData.filter(x => Math.round(x.trend) < 0);
    const betterItems = sortedTableData.filter(x => Math.round(x.trend) > 0);
    const zeroItems = sortedTableData.filter(x => Math.round(x.trend) === 0);
    const groupedData = [...worseItems, ...betterItems, ...zeroItems];
    return (<react_1.Fragment>
      <StyledPanelTable isEmpty={projects.length === 0 || (periodTableData === null || periodTableData === void 0 ? void 0 : periodTableData.data.length) === 0} headers={[
            (0, locale_1.t)('Key transaction'),
            (0, locale_1.t)('Project'),
            (0, locale_1.tct)('Last [period]', { period }),
            (0, locale_1.t)('This Week'),
            <RightAligned key="change">{(0, locale_1.t)('Change')}</RightAligned>,
        ]} isLoading={isLoading}>
        {groupedData.map((dataRow, idx) => {
            const project = projects.find(({ slug }) => dataRow.project === slug);
            const { trend, project: projectId, transaction } = dataRow;
            const weekRow = weekTableData === null || weekTableData === void 0 ? void 0 : weekTableData.data.find(row => row.project === projectId && row.transaction === transaction);
            if (!weekRow || trend === null) {
                return null;
            }
            const periodMisery = miseryRenderer === null || miseryRenderer === void 0 ? void 0 : miseryRenderer(dataRow, { organization, location });
            const weekMisery = weekRow && (miseryRenderer === null || miseryRenderer === void 0 ? void 0 : miseryRenderer(weekRow, { organization, location }));
            const trendValue = Math.round(Math.abs(trend));
            if (idx >= COLLAPSE_COUNT && !isExpanded) {
                return null;
            }
            return (<react_1.Fragment key={idx}>
              <TransactionWrapper>
                <link_1.default to={(0, utils_1.transactionSummaryRouteWithQuery)({
                    orgSlug: organization.slug,
                    transaction: dataRow.transaction,
                    projectID: project === null || project === void 0 ? void 0 : project.id,
                    query: { query: 'transaction.duration:<15m' },
                })}>
                  {dataRow.transaction}
                </link_1.default>
              </TransactionWrapper>
              <ProjectBadgeContainer>
                {project && <ProjectBadge avatarSize={18} project={project}/>}
              </ProjectBadgeContainer>
              <div>{periodMisery}</div>
              <div>{weekMisery !== null && weekMisery !== void 0 ? weekMisery : '\u2014'}</div>
              <ScoreWrapper>
                {trendValue === 0 ? (<SubText>
                    {`0\u0025 `}
                    {(0, locale_1.t)('change')}
                  </SubText>) : (<TrendText color={trend >= 0 ? 'green300' : 'red300'}>
                    {`${trendValue}\u0025 `}
                    {trend >= 0 ? (0, locale_1.t)('better') : (0, locale_1.t)('worse')}
                  </TrendText>)}
              </ScoreWrapper>
            </react_1.Fragment>);
        })}
      </StyledPanelTable>
      {groupedData.length >= COLLAPSE_COUNT && !isExpanded && !isLoading && (<ShowMore onClick={expandResults}>
          <ShowMoreText>
            <StyledIconList color="gray300"/>
            {(0, locale_1.tct)('Show [count] More', { count: groupedData.length - 1 - COLLAPSE_COUNT })}
          </ShowMoreText>

          <icons_1.IconChevron color="gray300" direction="down"/>
        </ShowMore>)}
    </react_1.Fragment>);
}
function TeamMiseryWrapper({ organization, projects, location, period, start, end, }) {
    if (projects.length === 0) {
        return (<TeamMisery isLoading={false} organization={organization} location={location} projects={[]} period={period} periodTableData={{ data: [] }} weekTableData={{ data: [] }}/>);
    }
    const commonEventView = {
        id: undefined,
        query: 'transaction.duration:<15m team_key_transaction:true',
        projects: projects.map(project => Number(project.id)),
        version: 2,
        orderby: '-tpm',
        fields: [
            'transaction',
            'project',
            'tpm()',
            'count_unique(user)',
            'count_miserable(user)',
            'user_misery()',
        ],
    };
    const periodEventView = eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, commonEventView), { name: 'periodMisery', range: period, start,
        end }));
    const weekEventView = eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, commonEventView), { name: 'weekMisery', range: '7d' }));
    return (<discoverQuery_1.default eventView={periodEventView} orgSlug={organization.slug} location={location}>
      {({ isLoading, tableData: periodTableData }) => (<discoverQuery_1.default eventView={weekEventView} orgSlug={organization.slug} location={location}>
          {({ isLoading: isWeekLoading, tableData: weekTableData }) => (<TeamMisery isLoading={isLoading || isWeekLoading} organization={organization} location={location} projects={projects} period={period} periodTableData={periodTableData} weekTableData={weekTableData}/>)}
        </discoverQuery_1.default>)}
    </discoverQuery_1.default>);
}
exports.default = TeamMiseryWrapper;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: 1fr 0.5fr 112px 112px 0.25fr;
  font-size: ${p => p.theme.fontSizeMedium};
  white-space: nowrap;
  margin-bottom: 0;
  border: 0;
  box-shadow: unset;

  & > div {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }

  ${p => p.isEmpty &&
    (0, react_2.css) `
      & > div:last-child {
        padding: 48px ${(0, space_1.default)(2)};
      }
    `}
`;
const ProjectBadgeContainer = (0, styled_1.default)('div') `
  display: flex;
`;
const ProjectBadge = (0, styled_1.default)(idBadge_1.default) `
  flex-shrink: 0;
`;
const TransactionWrapper = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
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
const SubText = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
`;
const TrendText = (0, styled_1.default)('div') `
  color: ${p => p.theme[p.color]};
`;
const ShowMore = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  color: ${p => p.theme.subText};
  cursor: pointer;
  border-top: 1px solid ${p => p.theme.border};
`;
const StyledIconList = (0, styled_1.default)(icons_1.IconList) `
  margin-right: ${(0, space_1.default)(1)};
`;
const ShowMoreText = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex-grow: 1;
`;
//# sourceMappingURL=teamMisery.jsx.map