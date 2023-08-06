Object.defineProperty(exports, "__esModule", { value: true });
exports.ADOPTION_STAGE_LABELS = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const collapsible_1 = (0, tslib_1.__importDefault)(require("app/components/collapsible"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const list_1 = require("app/views/releases/list");
const utils_2 = require("../../utils");
const crashFree_1 = (0, tslib_1.__importDefault)(require("../crashFree"));
const healthStatsChart_1 = (0, tslib_1.__importDefault)(require("../healthStatsChart"));
const healthStatsPeriod_1 = (0, tslib_1.__importDefault)(require("../healthStatsPeriod"));
const utils_3 = require("../utils");
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const projectLink_1 = (0, tslib_1.__importDefault)(require("./projectLink"));
const adoptionStagesLink = (<externalLink_1.default href="https://docs.sentry.io/product/releases/health/#adoption-stages"/>);
exports.ADOPTION_STAGE_LABELS = {
    low_adoption: {
        name: (0, locale_1.t)('Low Adoption'),
        tooltipTitle: (0, locale_1.tct)('This release has a low percentage of sessions compared to other releases in this project. [link:Learn more]', { link: adoptionStagesLink }),
        type: 'warning',
    },
    adopted: {
        name: (0, locale_1.t)('Adopted'),
        tooltipTitle: (0, locale_1.tct)('This release has a high percentage of sessions compared to other releases in this project. [link:Learn more]', { link: adoptionStagesLink }),
        type: 'success',
    },
    replaced: {
        name: (0, locale_1.t)('Replaced'),
        tooltipTitle: (0, locale_1.tct)('This release was previously Adopted, but now has a lower level of sessions compared to other releases in this project. [link:Learn more]', { link: adoptionStagesLink }),
        type: 'default',
    },
};
const Content = ({ projects, showReleaseAdoptionStages, adoptionStages, releaseVersion, location, organization, activeDisplay, showPlaceholders, isTopRelease, getHealthData, }) => (<react_1.Fragment>
    <header_1.default>
      <Layout showReleaseAdoptionStages={showReleaseAdoptionStages}>
        <Column>{(0, locale_1.t)('Project Name')}</Column>
        {showReleaseAdoptionStages && (<AdoptionStageColumn>{(0, locale_1.t)('Adoption Stage')}</AdoptionStageColumn>)}
        <AdoptionColumn>
          <span>{(0, locale_1.t)('Adoption')}</span>
          <healthStatsPeriod_1.default location={location}/>
        </AdoptionColumn>
        <CrashFreeRateColumn>{(0, locale_1.t)('Crash Free Rate')}</CrashFreeRateColumn>
        <CrashesColumn>{(0, locale_1.t)('Crashes')}</CrashesColumn>
        <NewIssuesColumn>{(0, locale_1.t)('New Issues')}</NewIssuesColumn>
      </Layout>
    </header_1.default>

    <ProjectRows>
      <collapsible_1.default expandButton={({ onExpand, numberOfHiddenItems }) => (<ExpandButtonWrapper>
            <button_1.default priority="primary" size="xsmall" onClick={onExpand}>
              {(0, locale_1.tct)('Show [numberOfHiddenItems] More', { numberOfHiddenItems })}
            </button_1.default>
          </ExpandButtonWrapper>)} collapseButton={({ onCollapse }) => (<CollapseButtonWrapper>
            <button_1.default priority="primary" size="xsmall" onClick={onCollapse}>
              {(0, locale_1.t)('Collapse')}
            </button_1.default>
          </CollapseButtonWrapper>)}>
        {projects.map((project, index) => {
        const { id, slug, newGroups } = project;
        const crashCount = getHealthData.getCrashCount(releaseVersion, id, utils_3.DisplayOption.SESSIONS);
        const crashFreeRate = getHealthData.getCrashFreeRate(releaseVersion, id, activeDisplay);
        const get24hCountByProject = getHealthData.get24hCountByProject(id, activeDisplay);
        const timeSeries = getHealthData.getTimeSeries(releaseVersion, id, activeDisplay);
        const adoption = getHealthData.getAdoption(releaseVersion, id, activeDisplay);
        const adoptionStage = showReleaseAdoptionStages &&
            (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages[project.slug]) &&
            (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages[project.slug].stage);
        const isMobileProject = (0, list_1.isProjectMobileForReleases)(project.platform);
        const adoptionStageLabel = Boolean(get24hCountByProject && adoptionStage && isMobileProject) &&
            exports.ADOPTION_STAGE_LABELS[adoptionStage];
        return (<ProjectRow key={`${releaseVersion}-${slug}-health`}>
              <Layout showReleaseAdoptionStages={showReleaseAdoptionStages}>
                <Column>
                  <projectBadge_1.default project={project} avatarSize={16}/>
                </Column>

                {showReleaseAdoptionStages && (<AdoptionStageColumn>
                    {adoptionStageLabel ? (<link_1.default to={{
                        pathname: `/organizations/${organization.slug}/releases/`,
                        query: Object.assign(Object.assign({}, location.query), { query: `release.stage:${adoptionStage}` }),
                    }}>
                        <tooltip_1.default title={adoptionStageLabel.tooltipTitle}>
                          <tag_1.default type={adoptionStageLabel.type}>
                            {adoptionStageLabel.name}
                          </tag_1.default>
                        </tooltip_1.default>
                      </link_1.default>) : (<notAvailable_1.default />)}
                  </AdoptionStageColumn>)}

                <AdoptionColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="100px"/>) : (<AdoptionWrapper>
                      <span>{adoption ? Math.round(adoption) : '0'}%</span>
                      <healthStatsChart_1.default data={timeSeries} height={20} activeDisplay={activeDisplay}/>
                    </AdoptionWrapper>)}
                </AdoptionColumn>

                <CrashFreeRateColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : (0, utils_1.defined)(crashFreeRate) ? (<crashFree_1.default percent={crashFreeRate}/>) : (<notAvailable_1.default />)}
                </CrashFreeRateColumn>

                <CrashesColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : (0, utils_1.defined)(crashCount) ? (<tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
                      <globalSelectionLink_1.default to={(0, utils_2.getReleaseUnhandledIssuesUrl)(organization.slug, project.id, releaseVersion)}>
                        <count_1.default value={crashCount}/>
                      </globalSelectionLink_1.default>
                    </tooltip_1.default>) : (<notAvailable_1.default />)}
                </CrashesColumn>

                <NewIssuesColumn>
                  <tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
                    <globalSelectionLink_1.default to={(0, utils_2.getReleaseNewIssuesUrl)(organization.slug, project.id, releaseVersion)}>
                      <count_1.default value={newGroups || 0}/>
                    </globalSelectionLink_1.default>
                  </tooltip_1.default>
                </NewIssuesColumn>

                <ViewColumn>
                  <guideAnchor_1.default disabled={!isTopRelease || index !== 0} target="view_release">
                    <projectLink_1.default orgSlug={organization.slug} project={project} releaseVersion={releaseVersion} location={location}/>
                  </guideAnchor_1.default>
                </ViewColumn>
              </Layout>
            </ProjectRow>);
    })}
      </collapsible_1.default>
    </ProjectRows>
  </react_1.Fragment>);
exports.default = Content;
const ProjectRows = (0, styled_1.default)('div') `
  position: relative;
`;
const ExpandButtonWrapper = (0, styled_1.default)('div') `
  position: absolute;
  width: 100%;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: linear-gradient(
    180deg,
    hsla(0, 0%, 100%, 0.15) 0,
    ${p => p.theme.white}
  );
  background-repeat: repeat-x;
  border-bottom: ${(0, space_1.default)(1)} solid ${p => p.theme.white};
  border-top: ${(0, space_1.default)(1)} solid transparent;
  border-bottom-right-radius: ${p => p.theme.borderRadius};
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    border-bottom-left-radius: ${p => p.theme.borderRadius};
  }
`;
const CollapseButtonWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  height: 41px;
`;
const ProjectRow = (0, styled_1.default)(panels_1.PanelItem) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    font-size: ${p => p.theme.fontSizeMedium};
  }
`;
const Layout = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1.4fr 0.6fr 0.7fr;

  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  width: 100%;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;
  }

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    ${p => p.showReleaseAdoptionStages
    ? `
      grid-template-columns: 1fr 0.7fr 1fr 1fr 0.7fr 0.7fr 0.5fr;
    `
    : `
      grid-template-columns: 1fr 1fr 1fr 0.7fr 0.7fr 0.5fr;
    `}
  }
`;
const Column = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
  line-height: 20px;
`;
const NewIssuesColumn = (0, styled_1.default)(Column) `
  font-variant-numeric: tabular-nums;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    text-align: right;
  }
`;
const AdoptionColumn = (0, styled_1.default)(Column) `
  display: none;
  font-variant-numeric: tabular-nums;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: flex;
    /* Chart tooltips need overflow */
    overflow: visible;
  }

  & > * {
    flex: 1;
  }
`;
const AdoptionStageColumn = (0, styled_1.default)(Column) `
  display: none;
  font-variant-numeric: tabular-nums;

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    display: flex;

    /* Need to show the edges of the tags */
    overflow: visible;
  }
`;
const AdoptionWrapper = (0, styled_1.default)('span') `
  flex: 1;
  display: inline-grid;
  grid-template-columns: 30px 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;

  /* Chart tooltips need overflow */
  overflow: visible;
`;
const CrashFreeRateColumn = (0, styled_1.default)(Column) `
  font-variant-numeric: tabular-nums;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    text-align: center;
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    text-align: right;
  }
`;
const CrashesColumn = (0, styled_1.default)(Column) `
  display: none;
  font-variant-numeric: tabular-nums;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    text-align: right;
  }
`;
const ViewColumn = (0, styled_1.default)(Column) `
  text-align: right;
`;
const StyledPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  height: 15px;
  display: inline-block;
  position: relative;
  top: ${(0, space_1.default)(0.25)};
`;
//# sourceMappingURL=content.jsx.map