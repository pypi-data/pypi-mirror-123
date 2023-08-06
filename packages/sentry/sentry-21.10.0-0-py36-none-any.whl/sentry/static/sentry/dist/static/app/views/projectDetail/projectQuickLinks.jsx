Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_1 = require("app/views/performance/trends/utils");
const utils_2 = require("app/views/performance/utils");
const styles_2 = require("./styles");
function ProjectQuickLinks({ organization, project, location }) {
    function getTrendsLink() {
        const queryString = (0, queryString_1.decodeScalar)(location.query.query);
        const conditions = new tokenizeSearch_1.MutableSearch(queryString || '');
        conditions.setFilterValues('tpm()', ['>0.01']);
        conditions.setFilterValues('transaction.duration', [
            '>0',
            `<${utils_1.DEFAULT_MAX_DURATION}`,
        ]);
        return {
            pathname: (0, utils_2.getPerformanceTrendsUrl)(organization),
            query: {
                project: project === null || project === void 0 ? void 0 : project.id,
                cursor: undefined,
                query: conditions.formatString(),
            },
        };
    }
    const quickLinks = [
        {
            title: (0, locale_1.t)('User Feedback'),
            to: {
                pathname: `/organizations/${organization.slug}/user-feedback/`,
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
        },
        {
            title: (0, locale_1.t)('View Transactions'),
            to: {
                pathname: (0, utils_2.getPerformanceLandingUrl)(organization),
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
            disabled: !organization.features.includes('performance-view'),
        },
        {
            title: (0, locale_1.t)('Most Improved/Regressed Transactions'),
            to: getTrendsLink(),
            disabled: !organization.features.includes('performance-view'),
        },
    ];
    return (<styles_2.SidebarSection>
      <styles_1.SectionHeading>{(0, locale_1.t)('Quick Links')}</styles_1.SectionHeading>
      {quickLinks
            // push disabled links to the bottom
            .sort((link1, link2) => Number(!!link1.disabled) - Number(!!link2.disabled))
            .map(({ title, to, disabled }) => (<div key={title}>
            <tooltip_1.default title={(0, locale_1.t)("You don't have access to this feature")} disabled={!disabled}>
              <QuickLink to={to} disabled={disabled}>
                <icons_1.IconLink />
                <QuickLinkText>{title}</QuickLinkText>
              </QuickLink>
            </tooltip_1.default>
          </div>))}
    </styles_2.SidebarSection>);
}
const QuickLink = (0, styled_1.default)(p => p.disabled ? (<span className={p.className}>{p.children}</span>) : (<globalSelectionLink_1.default {...p}/>)) `
  margin-bottom: ${(0, space_1.default)(1)};
  display: grid;
  align-items: center;
  gap: ${(0, space_1.default)(1)};
  grid-template-columns: auto 1fr;

  ${p => p.disabled &&
    `
    color: ${p.theme.gray200};
    cursor: not-allowed;
  `}
`;
const QuickLinkText = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeMedium};
  ${overflowEllipsis_1.default}
`;
exports.default = ProjectQuickLinks;
//# sourceMappingURL=projectQuickLinks.jsx.map