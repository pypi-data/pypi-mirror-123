Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ReleaseStats = ({ release, withHeading = true }) => {
    const commitCount = release.commitCount || 0;
    const authorCount = (release.authors && release.authors.length) || 0;
    if (commitCount === 0) {
        return null;
    }
    const releaseSummary = [
        (0, locale_1.tn)('%s commit', '%s commits', commitCount),
        (0, locale_1.t)('by'),
        (0, locale_1.tn)('%s author', '%s authors', authorCount),
    ].join(' ');
    return (<div className="release-stats">
      {withHeading && <ReleaseSummaryHeading>{releaseSummary}</ReleaseSummaryHeading>}
      <span style={{ display: 'inline-block' }}>
        <avatarList_1.default users={release.authors} avatarSize={25} typeMembers="authors"/>
      </span>
    </div>);
};
const ReleaseSummaryHeading = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeSmall};
  line-height: 1.2;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
exports.default = ReleaseStats;
//# sourceMappingURL=releaseStats.jsx.map