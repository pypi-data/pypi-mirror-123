Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const globalSelection_1 = require("app/actionCreators/globalSelection");
const backToIssues_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/backToIssues"));
const headerItemPosition_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/headerItemPosition"));
const headerSeparator_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/headerSeparator"));
const multipleEnvironmentSelector_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/multipleEnvironmentSelector"));
const multipleProjectSelector_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/multipleProjectSelector"));
const timeRangeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const PROJECTS_PER_PAGE = 50;
const defaultProps = {
    /**
     * Display Environment selector?
     */
    showEnvironmentSelector: true,
    /**
     * Display date selector?
     */
    showDateSelector: true,
    /**
     * Reset these URL params when we fire actions
     * (custom routing only)
     */
    resetParamsOnChange: [],
    /**
     * Remove ability to select multiple projects even if organization has feature 'global-views'
     */
    disableMultipleProjectSelection: false,
};
class GlobalSelectionHeader extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            projects: null,
            environments: null,
            searchQuery: '',
        };
        this.hasMultipleProjectSelection = () => new Set(this.props.organization.features).has('global-views');
        // Returns an options object for `update*` actions
        this.getUpdateOptions = () => ({
            save: true,
            resetParams: this.props.resetParamsOnChange,
        });
        this.handleChangeProjects = (projects) => {
            this.setState({
                projects,
            });
            (0, callIfFunction_1.callIfFunction)(this.props.onChangeProjects, projects);
        };
        this.handleChangeEnvironments = (environments) => {
            this.setState({
                environments,
            });
            (0, callIfFunction_1.callIfFunction)(this.props.onChangeEnvironments, environments);
        };
        this.handleChangeTime = ({ start, end, relative: period, utc }) => {
            (0, callIfFunction_1.callIfFunction)(this.props.onChangeTime, { start, end, period, utc });
        };
        this.handleUpdateTime = ({ relative: period, start, end, utc, } = {}) => {
            const newValueObj = {
                period,
                start,
                end,
                utc,
            };
            (0, globalSelection_1.updateDateTime)(newValueObj, this.props.router, this.getUpdateOptions());
            (0, callIfFunction_1.callIfFunction)(this.props.onUpdateTime, newValueObj);
        };
        this.handleUpdateEnvironmments = () => {
            const { environments } = this.state;
            (0, globalSelection_1.updateEnvironments)(environments, this.props.router, this.getUpdateOptions());
            this.setState({ environments: null });
            (0, callIfFunction_1.callIfFunction)(this.props.onUpdateEnvironments, environments);
        };
        this.handleUpdateProjects = () => {
            const { projects } = this.state;
            // Clear environments when switching projects
            (0, globalSelection_1.updateProjects)(projects || [], this.props.router, Object.assign(Object.assign({}, this.getUpdateOptions()), { environments: [] }));
            this.setState({ projects: null, environments: null });
            (0, callIfFunction_1.callIfFunction)(this.props.onUpdateProjects, projects);
        };
        this.getBackButton = () => {
            const { organization, location } = this.props;
            return (<BackButtonWrapper>
        <tooltip_1.default title={(0, locale_1.t)('Back to Issues Stream')} position="bottom">
          <backToIssues_1.default data-test-id="back-to-issues" to={`/organizations/${organization.slug}/issues/${location.search}`}>
            <icons_1.IconArrow direction="left" size="sm"/>
          </backToIssues_1.default>
        </tooltip_1.default>
      </BackButtonWrapper>);
        };
        this.scrollFetchDispatcher = (0, debounce_1.default)((onSearch, options) => {
            onSearch(this.state.searchQuery, options);
        }, 200, { leading: true, trailing: false });
        this.searchDispatcher = (0, debounce_1.default)((onSearch, searchQuery, options) => {
            // in the case that a user repeats a search query (because search is
            // debounced this is possible if the user types and then deletes what they
            // typed) we should switch to an append strategy to not override all results
            // with a new page.
            if (this.state.searchQuery === searchQuery) {
                options.append = true;
            }
            onSearch(searchQuery, options);
            this.setState({
                searchQuery,
            });
        }, 200);
    }
    render() {
        var _a;
        const { className, children, shouldForceProject, forceProject, isGlobalSelectionReady, loadingProjects, organization, showAbsolute, showRelative, showDateSelector, showEnvironmentSelector, memberProjects, nonMemberProjects, showIssueStreamLink, showProjectSettingsLink, lockedMessageSubject, timeRangeHint, specificProjectSlugs, disableMultipleProjectSelection, projectsFooterMessage, defaultSelection, } = this.props;
        const { period, start, end, utc } = this.props.selection.datetime || {};
        const defaultPeriod = ((_a = defaultSelection === null || defaultSelection === void 0 ? void 0 : defaultSelection.datetime) === null || _a === void 0 ? void 0 : _a.period) || constants_1.DEFAULT_STATS_PERIOD;
        const selectedProjects = forceProject
            ? [parseInt(forceProject.id, 10)]
            : this.props.selection.projects;
        return (<React.Fragment>
        <header_1.default className={className}>
          <headerItemPosition_1.default>
            {showIssueStreamLink && this.getBackButton()}
            <projects_1.default orgId={organization.slug} limit={PROJECTS_PER_PAGE} slugs={specificProjectSlugs}>
              {({ projects, hasMore, onSearch, fetching }) => {
                const paginatedProjectSelectorCallbacks = {
                    onScroll: ({ clientHeight, scrollHeight, scrollTop }) => {
                        // check if no new projects are being fetched and the user has
                        // scrolled far enough to fetch a new page of projects
                        if (!fetching &&
                            scrollTop + clientHeight >= scrollHeight - clientHeight &&
                            hasMore) {
                            this.scrollFetchDispatcher(onSearch, { append: true });
                        }
                    },
                    onFilterChange: event => {
                        this.searchDispatcher(onSearch, event.target.value, {
                            append: false,
                        });
                    },
                    searching: fetching,
                    paginated: true,
                };
                return (<multipleProjectSelector_1.default organization={organization} shouldForceProject={shouldForceProject} forceProject={forceProject} projects={loadingProjects ? projects : memberProjects} isGlobalSelectionReady={isGlobalSelectionReady} nonMemberProjects={nonMemberProjects} value={this.state.projects || this.props.selection.projects} onChange={this.handleChangeProjects} onUpdate={this.handleUpdateProjects} multi={!disableMultipleProjectSelection &&
                        this.hasMultipleProjectSelection()} {...(loadingProjects ? paginatedProjectSelectorCallbacks : {})} showIssueStreamLink={showIssueStreamLink} showProjectSettingsLink={showProjectSettingsLink} lockedMessageSubject={lockedMessageSubject} footerMessage={projectsFooterMessage}/>);
            }}
            </projects_1.default>
          </headerItemPosition_1.default>

          {showEnvironmentSelector && (<React.Fragment>
              <headerSeparator_1.default />
              <headerItemPosition_1.default>
                <multipleEnvironmentSelector_1.default organization={organization} projects={this.props.projects} loadingProjects={loadingProjects} selectedProjects={selectedProjects} value={this.props.selection.environments} onChange={this.handleChangeEnvironments} onUpdate={this.handleUpdateEnvironmments}/>
              </headerItemPosition_1.default>
            </React.Fragment>)}

          {showDateSelector && (<React.Fragment>
              <headerSeparator_1.default />
              <headerItemPosition_1.default>
                <timeRangeSelector_1.default key={`period:${period}-start:${start}-end:${end}-utc:${utc}-defaultPeriod:${defaultPeriod}`} showAbsolute={showAbsolute} showRelative={showRelative} relative={period} start={start} end={end} utc={utc} onChange={this.handleChangeTime} onUpdate={this.handleUpdateTime} organization={organization} defaultPeriod={defaultPeriod} hint={timeRangeHint}/>
              </headerItemPosition_1.default>
            </React.Fragment>)}

          {!showEnvironmentSelector && <headerItemPosition_1.default isSpacer/>}
          {!showDateSelector && <headerItemPosition_1.default isSpacer/>}
        </header_1.default>

        {isGlobalSelectionReady ? children : <organization_1.PageContent />}
      </React.Fragment>);
    }
}
GlobalSelectionHeader.defaultProps = defaultProps;
exports.default = (0, withGlobalSelection_1.default)(GlobalSelectionHeader);
const BackButtonWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  height: 100%;
  position: relative;
  left: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=globalSelectionHeader.jsx.map