Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../../utils");
const IssuesQuantity = ({ orgSlug, newGroups, projectId, releaseVersion, isCompact = false, }) => (<tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
    <link_1.default to={(0, utils_1.getReleaseNewIssuesUrl)(orgSlug, projectId, releaseVersion)}>
      {isCompact ? (<Issues>
          <StyledCount value={newGroups}/>
          <span>{(0, locale_1.tn)('issue', 'issues', newGroups)}</span>
        </Issues>) : (<count_1.default value={newGroups}/>)}
    </link_1.default>
  </tooltip_1.default>);
exports.default = IssuesQuantity;
const Issues = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: auto max-content;
  justify-content: flex-end;
  align-items: center;
  text-align: end;
`;
// overflowEllipsis is useful if the count's value is over 1000000000
const StyledCount = (0, styled_1.default)(count_1.default) `
  ${overflowEllipsis_1.default}
`;
//# sourceMappingURL=issuesQuantity.jsx.map