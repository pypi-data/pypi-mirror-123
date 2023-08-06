Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const releaseChart_1 = (0, tslib_1.__importDefault)(require("app/components/group/releaseChart"));
const seenInfo_1 = (0, tslib_1.__importDefault)(require("app/components/group/seenInfo"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("./sidebarSection"));
const GroupReleaseStats = ({ organization, project, environments, allEnvironments, group, currentRelease, }) => {
    const environmentLabel = environments.length > 0
        ? environments.map(env => env.displayName).join(', ')
        : (0, locale_1.t)('All Environments');
    const shortEnvironmentLabel = environments.length > 1
        ? (0, locale_1.t)('selected environments')
        : environments.length === 1
            ? environments[0].displayName
            : undefined;
    const projectId = project.id;
    const projectSlug = project.slug;
    const hasRelease = new Set(project.features).has('releases');
    const releaseTrackingUrl = `/settings/${organization.slug}/projects/${project.slug}/release-tracking/`;
    return (<sidebarSection_1.default title={<span data-test-id="env-label">{environmentLabel}</span>}>
      {!group || !allEnvironments ? (<placeholder_1.default height="288px"/>) : (<react_1.Fragment>
          <releaseChart_1.default group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.release} releaseStats={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.stats} statsPeriod="24h" title={(0, locale_1.t)('Last 24 Hours')} firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>
          <releaseChart_1.default group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.release} releaseStats={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.stats} statsPeriod="30d" title={(0, locale_1.t)('Last 30 Days')} className="bar-chart-small" firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>

          <sidebarSection_1.default secondary title={<span>
                {(0, locale_1.t)('Last seen')}
                <TooltipWrapper>
                  <tooltip_1.default title={(0, locale_1.t)('When the most recent event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </tooltip_1.default>
                </TooltipWrapper>
              </span>}>
            <seenInfo_1.default organization={organization} projectId={projectId} projectSlug={projectSlug} date={(0, getDynamicText_1.default)({
                value: group.lastSeen,
                fixed: '2016-01-13T03:08:25Z',
            })} dateGlobal={allEnvironments.lastSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.lastRelease || null} title={(0, locale_1.t)('Last seen')}/>
          </sidebarSection_1.default>

          <sidebarSection_1.default secondary title={<span>
                {(0, locale_1.t)('First seen')}
                <TooltipWrapper>
                  <tooltip_1.default title={(0, locale_1.t)('When the first event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </tooltip_1.default>
                </TooltipWrapper>
              </span>}>
            <seenInfo_1.default organization={organization} projectId={projectId} projectSlug={projectSlug} date={(0, getDynamicText_1.default)({
                value: group.firstSeen,
                fixed: '2015-08-13T03:08:25Z',
            })} dateGlobal={allEnvironments.firstSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.firstRelease || null} title={(0, locale_1.t)('First seen')}/>
          </sidebarSection_1.default>
          {!hasRelease ? (<sidebarSection_1.default secondary title={(0, locale_1.t)('Releases not configured')}>
              <a href={releaseTrackingUrl}>{(0, locale_1.t)('Setup Releases')}</a>{' '}
              {(0, locale_1.t)(' to make issues easier to fix.')}
            </sidebarSection_1.default>) : null}
        </react_1.Fragment>)}
    </sidebarSection_1.default>);
};
exports.default = (0, react_1.memo)(GroupReleaseStats);
const TooltipWrapper = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
`;
const StyledIconQuest = (0, styled_1.default)(icons_1.IconQuestion) `
  position: relative;
  top: 2px;
`;
//# sourceMappingURL=releaseStats.jsx.map