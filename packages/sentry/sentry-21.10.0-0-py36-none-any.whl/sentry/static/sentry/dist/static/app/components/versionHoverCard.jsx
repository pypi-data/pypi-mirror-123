Object.defineProperty(exports, "__esModule", { value: true });
exports.VersionHoverCard = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const lastCommit_1 = (0, tslib_1.__importDefault)(require("app/components/lastCommit"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const repoLabel_1 = (0, tslib_1.__importDefault)(require("app/components/repoLabel"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withRelease_1 = (0, tslib_1.__importDefault)(require("app/utils/withRelease"));
const withRepositories_1 = (0, tslib_1.__importDefault)(require("app/utils/withRepositories"));
class VersionHoverCard extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            visible: false,
        };
    }
    toggleHovercard() {
        this.setState({
            visible: true,
        });
    }
    getRepoLink() {
        const { organization } = this.props;
        const orgSlug = organization.slug;
        return {
            header: null,
            body: (<ConnectRepo>
          <h5>{(0, locale_1.t)('Releases are better with commit data!')}</h5>
          <p>
            {(0, locale_1.t)('Connect a repository to see commit info, files changed, and authors involved in future releases.')}
          </p>
          <button_1.default href={`/organizations/${orgSlug}/repos/`} priority="primary">
            {(0, locale_1.t)('Connect a repository')}
          </button_1.default>
        </ConnectRepo>),
        };
    }
    getBody() {
        const { releaseVersion, release, deploys } = this.props;
        if (release === undefined || !(0, utils_1.defined)(deploys)) {
            return { header: null, body: null };
        }
        const { lastCommit } = release;
        const recentDeploysByEnvironment = deploys.reduce(function (dbe, deploy) {
            const { dateFinished, environment } = deploy;
            if (!dbe.hasOwnProperty(environment)) {
                dbe[environment] = dateFinished;
            }
            return dbe;
        }, {});
        let mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment);
        if (Object.keys(recentDeploysByEnvironment).length > 3) {
            mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment).slice(0, 3);
        }
        return {
            header: (<HeaderWrapper>
          {(0, locale_1.t)('Release')}
          <VersionWrapper>
            <StyledVersion version={releaseVersion} truncate anchor={false}/>

            <clipboard_1.default value={releaseVersion}>
              <ClipboardIconWrapper>
                <icons_1.IconCopy size="xs"/>
              </ClipboardIconWrapper>
            </clipboard_1.default>
          </VersionWrapper>
        </HeaderWrapper>),
            body: (<div>
          <div className="row row-flex">
            <div className="col-xs-4">
              <h6>{(0, locale_1.t)('New Issues')}</h6>
              <div className="count-since">{release.newGroups}</div>
            </div>
            <div className="col-xs-8">
              <h6 style={{ textAlign: 'right' }}>
                {release.commitCount}{' '}
                {release.commitCount !== 1 ? (0, locale_1.t)('commits ') : (0, locale_1.t)('commit ')} {(0, locale_1.t)('by ')}{' '}
                {release.authors.length}{' '}
                {release.authors.length !== 1 ? (0, locale_1.t)('authors') : (0, locale_1.t)('author')}{' '}
              </h6>
              <avatarList_1.default users={release.authors} avatarSize={25} tooltipOptions={{ container: 'body' }} typeMembers="authors"/>
            </div>
          </div>
          {lastCommit && <lastCommit_1.default commit={lastCommit} headerClass="commit-heading"/>}
          {deploys.length > 0 && (<div>
              <div className="divider">
                <h6 className="deploy-heading">{(0, locale_1.t)('Deploys')}</h6>
              </div>
              {mostRecentDeploySlice.map((env, idx) => {
                        const dateFinished = recentDeploysByEnvironment[env];
                        return (<div className="deploy" key={idx}>
                    <div className="deploy-meta" style={{ position: 'relative' }}>
                      <VersionRepoLabel>{env}</VersionRepoLabel>
                      {dateFinished && <StyledTimeSince date={dateFinished}/>}
                    </div>
                  </div>);
                    })}
            </div>)}
        </div>),
        };
    }
    render() {
        var _a;
        const { deploysLoading, deploysError, release, releaseLoading, releaseError, repositories, repositoriesLoading, repositoriesError, } = this.props;
        let header = null;
        let body = null;
        const loading = !!(deploysLoading || releaseLoading || repositoriesLoading);
        const error = (_a = deploysError !== null && deploysError !== void 0 ? deploysError : releaseError) !== null && _a !== void 0 ? _a : repositoriesError;
        const hasRepos = repositories && repositories.length > 0;
        if (loading) {
            body = <loadingIndicator_1.default mini/>;
        }
        else if (error) {
            body = <loadingError_1.default />;
        }
        else {
            const renderObj = hasRepos && release ? this.getBody() : this.getRepoLink();
            header = renderObj.header;
            body = renderObj.body;
        }
        return (<hovercard_1.default {...this.props} header={header} body={body}>
        {this.props.children}
      </hovercard_1.default>);
    }
}
exports.VersionHoverCard = VersionHoverCard;
exports.default = (0, withApi_1.default)((0, withRelease_1.default)((0, withRepositories_1.default)(VersionHoverCard)));
const ConnectRepo = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  text-align: center;
`;
const VersionRepoLabel = (0, styled_1.default)(repoLabel_1.default) `
  width: 86px;
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: ${p => p.theme.gray300};
  position: absolute;
  left: 98px;
  width: 50%;
  padding: 3px 0;
`;
const HeaderWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const VersionWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: flex-end;
`;
const StyledVersion = (0, styled_1.default)(version_1.default) `
  margin-right: ${(0, space_1.default)(0.5)};
  max-width: 190px;
`;
const ClipboardIconWrapper = (0, styled_1.default)('span') `
  &:hover {
    cursor: pointer;
  }
`;
//# sourceMappingURL=versionHoverCard.jsx.map