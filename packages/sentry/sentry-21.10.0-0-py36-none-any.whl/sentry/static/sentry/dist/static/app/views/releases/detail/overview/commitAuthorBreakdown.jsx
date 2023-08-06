Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const collapsible_1 = (0, tslib_1.__importDefault)(require("app/components/collapsible"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const styles_1 = require("./styles");
class CommitAuthorBreakdown extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
    }
    getEndpoints() {
        const { orgId, projectSlug, version } = this.props;
        const commitsEndpoint = `/projects/${orgId}/${projectSlug}/releases/${encodeURIComponent(version)}/commits/`;
        return [['commits', commitsEndpoint]];
    }
    componentDidUpdate(prevProps) {
        if (prevProps.version !== this.props.version) {
            this.remountComponent();
        }
    }
    getDisplayPercent(authorCommitCount) {
        const { commits } = this.state;
        const calculatedPercent = Math.round((0, utils_1.percent)(authorCommitCount, commits.length));
        return `${calculatedPercent < 1 ? '<1' : calculatedPercent}%`;
    }
    renderBody() {
        var _a;
        // group commits by author
        const groupedAuthorCommits = (_a = this.state.commits) === null || _a === void 0 ? void 0 : _a.reduce((authorCommitsAccumulator, commit) => {
            var _a, _b;
            const email = (_b = (_a = commit.author) === null || _a === void 0 ? void 0 : _a.email) !== null && _b !== void 0 ? _b : 'unknown';
            if (authorCommitsAccumulator.hasOwnProperty(email)) {
                authorCommitsAccumulator[email].commitCount += 1;
            }
            else {
                authorCommitsAccumulator[email] = {
                    commitCount: 1,
                    author: commit.author,
                };
            }
            return authorCommitsAccumulator;
        }, {});
        // sort authors by number of commits
        const sortedAuthorsByNumberOfCommits = Object.values(groupedAuthorCommits).sort((a, b) => b.commitCount - a.commitCount);
        if (!sortedAuthorsByNumberOfCommits.length) {
            return null;
        }
        return (<styles_1.Wrapper>
        <styles_1.SectionHeading>{(0, locale_1.t)('Commit Author Breakdown')}</styles_1.SectionHeading>
        <collapsible_1.default expandButton={({ onExpand, numberOfHiddenItems }) => (<button_1.default priority="link" onClick={onExpand}>
              {(0, locale_1.tn)('Show %s collapsed author', 'Show %s collapsed authors', numberOfHiddenItems)}
            </button_1.default>)}>
          {sortedAuthorsByNumberOfCommits.map(({ commitCount, author }, index) => {
                var _a;
                return (<AuthorLine key={(_a = author === null || author === void 0 ? void 0 : author.email) !== null && _a !== void 0 ? _a : index}>
              <userAvatar_1.default user={author} size={20} hasTooltip/>
              <AuthorName>{(0, formatters_1.userDisplayName)(author || {}, false)}</AuthorName>
              <Commits>{(0, locale_1.tn)('%s commit', '%s commits', commitCount)}</Commits>
              <Percent>{this.getDisplayPercent(commitCount)}</Percent>
            </AuthorLine>);
            })}
        </collapsible_1.default>
      </styles_1.Wrapper>);
    }
}
const AuthorLine = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-template-columns: 30px 2fr 1fr 40px;
  width: 100%;
  margin-bottom: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const AuthorName = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default};
`;
const Commits = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  text-align: right;
`;
const Percent = (0, styled_1.default)('div') `
  min-width: 40px;
  text-align: right;
`;
exports.default = CommitAuthorBreakdown;
//# sourceMappingURL=commitAuthorBreakdown.jsx.map