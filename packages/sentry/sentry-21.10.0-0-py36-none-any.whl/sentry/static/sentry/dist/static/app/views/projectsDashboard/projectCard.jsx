Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectCard = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const projects_1 = require("app/actionCreators/projects");
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const bookmarkStar_1 = (0, tslib_1.__importDefault)(require("app/components/projects/bookmarkStar"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const scoreCard_1 = (0, tslib_1.__importStar)(require("app/components/scoreCard"));
const platformCategories_1 = require("app/data/platformCategories");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const projectsStatsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStatsStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const callIfFunction_1 = require("app/utils/callIfFunction");
const formatters_1 = require("app/utils/formatters");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const missingReleasesButtons_1 = (0, tslib_1.__importStar)(require("app/views/projectDetail/missingFeatureButtons/missingReleasesButtons"));
const utils_2 = require("app/views/releases/utils");
const chart_1 = (0, tslib_1.__importDefault)(require("./chart"));
const deploys_1 = (0, tslib_1.__importStar)(require("./deploys"));
class ProjectCard extends react_1.Component {
    componentDidMount() {
        const { organization, project, api } = this.props;
        // fetch project stats
        (0, projects_1.loadStatsForProject)(api, project.id, {
            orgId: organization.slug,
            projectId: project.id,
            query: {
                transactionStats: this.hasPerformance ? '1' : undefined,
                sessionStats: '1',
            },
        });
    }
    get hasPerformance() {
        return this.props.organization.features.includes('performance-view');
    }
    get crashFreeTrend() {
        const { currentCrashFreeRate, previousCrashFreeRate } = this.props.project.sessionStats || {};
        if (!(0, utils_1.defined)(currentCrashFreeRate) || !(0, utils_1.defined)(previousCrashFreeRate)) {
            return undefined;
        }
        return (0, round_1.default)(currentCrashFreeRate - previousCrashFreeRate, currentCrashFreeRate > utils_2.CRASH_FREE_DECIMAL_THRESHOLD ? 3 : 0);
    }
    renderMissingFeatureCard() {
        const { organization, project } = this.props;
        if (project.platform && platformCategories_1.releaseHealth.includes(project.platform)) {
            return (<scoreCard_1.default title={(0, locale_1.t)('Crash Free Sessions')} score={<missingReleasesButtons_1.default organization={organization} health/>}/>);
        }
        return (<scoreCard_1.default title={(0, locale_1.t)('Crash Free Sessions')} score={<NotAvailable>
            {(0, locale_1.t)('Not Available')}
            <questionTooltip_1.default title={(0, locale_1.t)('Release Health is not yet supported on this platform.')} size="xs"/>
          </NotAvailable>}/>);
    }
    renderTrend() {
        const { currentCrashFreeRate } = this.props.project.sessionStats || {};
        if (!(0, utils_1.defined)(currentCrashFreeRate) || !(0, utils_1.defined)(this.crashFreeTrend)) {
            return null;
        }
        return (<div>
        {this.crashFreeTrend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {`${(0, formatters_1.formatAbbreviatedNumber)(Math.abs(this.crashFreeTrend))}\u0025`}
      </div>);
    }
    render() {
        var _a, _b;
        const { organization, project, hasProjectAccess } = this.props;
        const { stats, slug, transactionStats, sessionStats } = project;
        const { hasHealthData, currentCrashFreeRate } = sessionStats || {};
        const totalErrors = (_a = stats === null || stats === void 0 ? void 0 : stats.reduce((sum, [_, value]) => sum + value, 0)) !== null && _a !== void 0 ? _a : 0;
        const totalTransactions = (_b = transactionStats === null || transactionStats === void 0 ? void 0 : transactionStats.reduce((sum, [_, value]) => sum + value, 0)) !== null && _b !== void 0 ? _b : 0;
        const zeroTransactions = totalTransactions === 0;
        const hasFirstEvent = Boolean(project.firstEvent || project.firstTransactionEvent);
        return (<div data-test-id={slug}>
        <StyledProjectCard>
          <CardHeader>
            <HeaderRow>
              <StyledIdBadge project={project} avatarSize={18} hideOverflow disableLink={!hasProjectAccess}/>
              <bookmarkStar_1.default organization={organization} project={project}/>
            </HeaderRow>
            <SummaryLinks>
              {stats ? (<react_1.Fragment>
                  <link_1.default data-test-id="project-errors" to={`/organizations/${organization.slug}/issues/?project=${project.id}`}>
                    {(0, locale_1.t)('errors: %s', (0, formatters_1.formatAbbreviatedNumber)(totalErrors))}
                  </link_1.default>
                  {this.hasPerformance && (<react_1.Fragment>
                      <em>|</em>
                      <TransactionsLink data-test-id="project-transactions" to={`/organizations/${organization.slug}/performance/?project=${project.id}`}>
                        {(0, locale_1.t)('transactions: %s', (0, formatters_1.formatAbbreviatedNumber)(totalTransactions))}
                        {zeroTransactions && (<questionTooltip_1.default title={(0, locale_1.t)('Click here to learn more about performance monitoring')} position="top" size="xs"/>)}
                      </TransactionsLink>
                    </react_1.Fragment>)}
                </react_1.Fragment>) : (<SummaryLinkPlaceholder />)}
            </SummaryLinks>
          </CardHeader>
          <ChartContainer>
            {stats ? (<chart_1.default firstEvent={hasFirstEvent} stats={stats} transactionStats={transactionStats}/>) : (<placeholder_1.default height="150px"/>)}
          </ChartContainer>
          <FooterWrapper>
            <ScoreCardWrapper>
              {!stats ? (<react_1.Fragment>
                  <ReleaseTitle>{(0, locale_1.t)('Crash Free Sessions')}</ReleaseTitle>
                  <FooterPlaceholder />
                </react_1.Fragment>) : hasHealthData ? (<scoreCard_1.default title={(0, locale_1.t)('Crash Free Sessions')} score={(0, utils_1.defined)(currentCrashFreeRate)
                    ? (0, utils_2.displayCrashFreePercent)(currentCrashFreeRate)
                    : '\u2014'} trend={this.renderTrend()} trendStatus={this.crashFreeTrend
                    ? this.crashFreeTrend > 0
                        ? 'good'
                        : 'bad'
                    : undefined}/>) : (this.renderMissingFeatureCard())}
            </ScoreCardWrapper>
            <DeploysWrapper>
              <ReleaseTitle>{(0, locale_1.t)('Latest Deploys')}</ReleaseTitle>
              {stats ? <deploys_1.default project={project} shorten/> : <FooterPlaceholder />}
            </DeploysWrapper>
          </FooterWrapper>
        </StyledProjectCard>
      </div>);
    }
}
exports.ProjectCard = ProjectCard;
class ProjectCardContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.listeners = [
            projectsStatsStore_1.default.listen(itemsBySlug => {
                this.onProjectStoreUpdate(itemsBySlug);
            }, undefined),
        ];
    }
    getInitialState() {
        const { project } = this.props;
        const initialState = projectsStatsStore_1.default.getInitialState() || {};
        return {
            projectDetails: initialState[project.slug] || null,
        };
    }
    componentWillUnmount() {
        this.listeners.forEach(callIfFunction_1.callIfFunction);
    }
    onProjectStoreUpdate(itemsBySlug) {
        const { project } = this.props;
        // Don't update state if we already have stats
        if (!itemsBySlug[project.slug]) {
            return;
        }
        if (itemsBySlug[project.slug] === this.state.projectDetails) {
            return;
        }
        this.setState({
            projectDetails: itemsBySlug[project.slug],
        });
    }
    render() {
        const _a = this.props, { project } = _a, props = (0, tslib_1.__rest)(_a, ["project"]);
        const { projectDetails } = this.state;
        return (<ProjectCard {...props} project={Object.assign(Object.assign({}, project), (projectDetails || {}))}/>);
    }
}
const ChartContainer = (0, styled_1.default)('div') `
  position: relative;
  background: ${p => p.theme.backgroundSecondary};
`;
const CardHeader = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
`;
const HeaderRow = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto;
  justify-content: space-between;
  align-items: center;
`;
const StyledProjectCard = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  box-shadow: ${p => p.theme.dropShadowLight};
  min-height: 330px;
`;
const FooterWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1fr;
  div {
    border: none;
    box-shadow: none;
    font-size: ${p => p.theme.fontSizeMedium};
    padding: 0;
  }
  ${missingReleasesButtons_1.MissingReleaseButtonBar} {
    a {
      background-color: ${p => p.theme.background};
      border: 1px solid ${p => p.theme.border};
      border-radius: ${p => p.theme.borderRadius};
      color: ${p => p.theme.gray500};
    }
  }
`;
const ScoreCardWrapper = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(2)} 0 0 ${(0, space_1.default)(2)};
  ${scoreCard_1.ScorePanel} {
    min-height: auto;
  }
  ${scoreCard_1.HeaderTitle} {
    color: ${p => p.theme.gray300};
    font-weight: 600;
  }
  ${scoreCard_1.ScoreWrapper} {
    flex-direction: column;
    align-items: flex-start;
  }
  ${scoreCard_1.Score} {
    font-size: 28px;
  }
  ${scoreCard_1.Trend} {
    margin-left: 0;
    margin-top: ${(0, space_1.default)(0.5)};
  }
`;
const DeploysWrapper = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(2)};
  ${deploys_1.GetStarted} {
    display: block;
    height: 100%;
  }
  ${deploys_1.TextOverflow} {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-column-gap: ${(0, space_1.default)(1)};
    div {
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    a {
      display: grid;
    }
  }
  ${deploys_1.DeployRows} {
    grid-template-columns: 2fr auto;
    margin-right: ${(0, space_1.default)(2)};
    height: auto;
    svg {
      display: none;
    }
  }
`;
const ReleaseTitle = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
  font-weight: 600;
`;
const StyledIdBadge = (0, styled_1.default)(idBadge_1.default) `
  overflow: hidden;
  white-space: nowrap;
  flex-shrink: 1;
`;
const SummaryLinks = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;

  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};

  /* Need to offset for the project icon and margin */
  margin-left: 26px;

  a {
    color: ${p => p.theme.formText};
    :hover {
      color: ${p => p.theme.subText};
    }
  }
  em {
    font-style: normal;
    margin: 0 ${(0, space_1.default)(0.5)};
  }
`;
const TransactionsLink = (0, styled_1.default)(link_1.default) `
  display: flex;
  align-items: center;
  justify-content: space-between;

  > span {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const NotAvailable = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  font-weight: normal;
  display: grid;
  grid-template-columns: auto auto;
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
`;
const SummaryLinkPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  height: 15px;
  width: 180px;
  margin-top: ${(0, space_1.default)(0.75)};
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
const FooterPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  height: 40px;
  width: auto;
  margin-right: ${(0, space_1.default)(2)};
`;
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(ProjectCardContainer));
//# sourceMappingURL=projectCard.jsx.map