Object.defineProperty(exports, "__esModule", { value: true });
exports.ReleasesList = exports.isProjectMobileForReleases = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_lazyload_1 = require("react-lazyload");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const tags_1 = require("app/actionCreators/tags");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const smartSearchBar_1 = (0, tslib_1.__importDefault)(require("app/components/smartSearchBar"));
const constants_1 = require("app/constants");
const globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
const platformCategories_1 = require("app/data/platformCategories");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const analytics_1 = require("app/utils/analytics");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const releaseArchivedNotice_1 = (0, tslib_1.__importDefault)(require("../detail/overview/releaseArchivedNotice"));
const releaseAdoptionChart_1 = (0, tslib_1.__importDefault)(require("./releaseAdoptionChart"));
const releaseCard_1 = (0, tslib_1.__importDefault)(require("./releaseCard"));
const releaseDisplayOptions_1 = (0, tslib_1.__importDefault)(require("./releaseDisplayOptions"));
const releaseListRequest_1 = (0, tslib_1.__importDefault)(require("./releaseListRequest"));
const releaseListSortOptions_1 = (0, tslib_1.__importDefault)(require("./releaseListSortOptions"));
const releaseListStatusOptions_1 = (0, tslib_1.__importDefault)(require("./releaseListStatusOptions"));
const releasePromo_1 = (0, tslib_1.__importDefault)(require("./releasePromo"));
const utils_2 = require("./utils");
const supportedTags = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    'release.stage': {
        key: 'release.stage',
        name: 'release.stage',
        predefined: true,
        values: constants_1.RELEASE_ADOPTION_STAGES,
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
const isProjectMobileForReleases = (projectPlatform) => [...platformCategories_1.mobile, ...platformCategories_1.desktop].includes(projectPlatform);
exports.isProjectMobileForReleases = isProjectMobileForReleases;
class ReleasesList extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
        this.shouldRenderBadRequests = true;
        this.handleSearch = (query) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query }) }));
        };
        this.handleSortBy = (sort) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, sort }) }));
        };
        this.handleDisplay = (display) => {
            const { location, router } = this.props;
            let sort = location.query.sort;
            if (sort === utils_2.SortOption.USERS_24_HOURS && display === utils_2.DisplayOption.SESSIONS)
                sort = utils_2.SortOption.SESSIONS_24_HOURS;
            else if (sort === utils_2.SortOption.SESSIONS_24_HOURS && display === utils_2.DisplayOption.USERS)
                sort = utils_2.SortOption.USERS_24_HOURS;
            else if (sort === utils_2.SortOption.CRASH_FREE_USERS && display === utils_2.DisplayOption.SESSIONS)
                sort = utils_2.SortOption.CRASH_FREE_SESSIONS;
            else if (sort === utils_2.SortOption.CRASH_FREE_SESSIONS && display === utils_2.DisplayOption.USERS)
                sort = utils_2.SortOption.CRASH_FREE_USERS;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, display, sort }) }));
        };
        this.handleStatus = (status) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, status }) }));
        };
        this.trackAddReleaseHealth = () => {
            const { organization, selection } = this.props;
            if (organization.id && selection.projects[0]) {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: `releases_list.click_add_release_health`,
                    eventName: `Releases List: Click Add Release Health`,
                    organization_id: parseInt(organization.id, 10),
                    project_id: selection.projects[0],
                });
            }
        };
        this.tagValueLoader = (key, search) => {
            const { location, organization } = this.props;
            const { project: projectId } = location.query;
            return (0, tags_1.fetchTagValues)(this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
        this.getTagValues = (tag, currentQuery) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const values = yield this.tagValueLoader(tag.key, currentQuery);
            return values.map(({ value }) => value);
        });
    }
    getTitle() {
        return (0, routeTitle_1.default)((0, locale_1.t)('Releases'), this.props.organization.slug, false);
    }
    getEndpoints() {
        const { organization, location } = this.props;
        const { statsPeriod } = location.query;
        const activeSort = this.getSort();
        const activeStatus = this.getStatus();
        const query = Object.assign(Object.assign({}, (0, pick_1.default)(location.query, ['project', 'environment', 'cursor', 'query', 'sort'])), { summaryStatsPeriod: statsPeriod, per_page: 20, flatten: activeSort === utils_2.SortOption.DATE ? 0 : 1, adoptionStages: 1, status: activeStatus === utils_2.StatusOption.ARCHIVED
                ? types_1.ReleaseStatus.Archived
                : types_1.ReleaseStatus.Active });
        const endpoints = [
            [
                'releases',
                `/organizations/${organization.slug}/releases/`,
                { query },
                { disableEntireQuery: true },
            ],
        ];
        return endpoints;
    }
    componentDidUpdate(prevProps, prevState) {
        super.componentDidUpdate(prevProps, prevState);
        if (prevState.releases !== this.state.releases) {
            /**
             * Manually trigger checking for elements in viewport.
             * Helpful when LazyLoad components enter the viewport without resize or scroll events,
             * https://github.com/twobin/react-lazyload#forcecheck
             *
             * HealthStatsCharts are being rendered only when they are scrolled into viewport.
             * This is how we re-check them without scrolling once releases change as this view
             * uses shouldReload=true and there is no reloading happening.
             */
            (0, react_lazyload_1.forceCheck)();
        }
    }
    getQuery() {
        const { query } = this.props.location.query;
        return typeof query === 'string' ? query : undefined;
    }
    getSort() {
        const { environments } = this.props.selection;
        const { sort } = this.props.location.query;
        // Require 1 environment for date adopted
        if (sort === utils_2.SortOption.ADOPTION && environments.length !== 1) {
            return utils_2.SortOption.DATE;
        }
        const sortExists = Object.values(utils_2.SortOption).includes(sort);
        if (sortExists) {
            return sort;
        }
        return utils_2.SortOption.DATE;
    }
    getDisplay() {
        const { display } = this.props.location.query;
        switch (display) {
            case utils_2.DisplayOption.USERS:
                return utils_2.DisplayOption.USERS;
            default:
                return utils_2.DisplayOption.SESSIONS;
        }
    }
    getStatus() {
        const { status } = this.props.location.query;
        switch (status) {
            case utils_2.StatusOption.ARCHIVED:
                return utils_2.StatusOption.ARCHIVED;
            default:
                return utils_2.StatusOption.ACTIVE;
        }
    }
    getSelectedProject() {
        const { selection, projects } = this.props;
        const selectedProjectId = selection.projects && selection.projects.length === 1 && selection.projects[0];
        return projects === null || projects === void 0 ? void 0 : projects.find(p => p.id === `${selectedProjectId}`);
    }
    get projectHasSessions() {
        var _a, _b;
        return (_b = (_a = this.getSelectedProject()) === null || _a === void 0 ? void 0 : _a.hasSessions) !== null && _b !== void 0 ? _b : null;
    }
    shouldShowLoadingIndicator() {
        const { loading, releases, reloading } = this.state;
        return (loading && !reloading) || (loading && !(releases === null || releases === void 0 ? void 0 : releases.length));
    }
    renderLoading() {
        return this.renderBody();
    }
    renderError() {
        return this.renderBody();
    }
    renderEmptyMessage() {
        const { location, organization, selection } = this.props;
        const { statsPeriod } = location.query;
        const searchQuery = this.getQuery();
        const activeSort = this.getSort();
        const activeStatus = this.getStatus();
        if (searchQuery && searchQuery.length) {
            return (<emptyStateWarning_1.default small>{`${(0, locale_1.t)('There are no releases that match')}: '${searchQuery}'.`}</emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.USERS_24_HOURS) {
            return (<emptyStateWarning_1.default small>
          {(0, locale_1.t)('There are no releases with active user data (users in the last 24 hours).')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.SESSIONS_24_HOURS) {
            return (<emptyStateWarning_1.default small>
          {(0, locale_1.t)('There are no releases with active session data (sessions in the last 24 hours).')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.BUILD || activeSort === utils_2.SortOption.SEMVER) {
            return (<emptyStateWarning_1.default small>
          {(0, locale_1.t)('There are no releases with semantic versioning.')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort !== utils_2.SortOption.DATE) {
            const relativePeriod = (0, utils_1.getRelativeSummary)(statsPeriod || constants_1.DEFAULT_STATS_PERIOD).toLowerCase();
            return (<emptyStateWarning_1.default small>
          {`${(0, locale_1.t)('There are no releases with data in the')} ${relativePeriod}.`}
        </emptyStateWarning_1.default>);
        }
        if (activeStatus === utils_2.StatusOption.ARCHIVED) {
            return (<emptyStateWarning_1.default small>
          {(0, locale_1.t)('There are no archived releases.')}
        </emptyStateWarning_1.default>);
        }
        return (<releasePromo_1.default organization={organization} projectId={selection.projects.filter(p => p !== globalSelectionHeader_2.ALL_ACCESS_PROJECTS)[0]}/>);
    }
    renderHealthCta() {
        const { organization } = this.props;
        const { releases } = this.state;
        const selectedProject = this.getSelectedProject();
        if (!selectedProject || this.projectHasSessions !== false || !(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return null;
        }
        return (<projects_1.default orgId={organization.slug} slugs={[selectedProject.slug]}>
        {({ projects, initiallyLoaded, fetchError }) => {
                const project = projects && projects.length === 1 && projects[0];
                const projectCanHaveReleases = project && project.platform && platformCategories_1.releaseHealth.includes(project.platform);
                if (!initiallyLoaded || fetchError || !projectCanHaveReleases) {
                    return null;
                }
                return (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
              <AlertText>
                <div>
                  {(0, locale_1.t)('To track user adoption, crash rates, session data and more, add Release Health to your current setup.')}
                </div>
                <externalLink_1.default href="https://docs.sentry.io/product/releases/health/setup/" onClick={this.trackAddReleaseHealth}>
                  {(0, locale_1.t)('Add Release Health')}
                </externalLink_1.default>
              </AlertText>
            </alert_1.default>);
            }}
      </projects_1.default>);
    }
    renderInnerBody(activeDisplay, showReleaseAdoptionStages) {
        const { location, selection, organization, router } = this.props;
        const { releases, reloading, releasesPageLinks } = this.state;
        if (this.shouldShowLoadingIndicator()) {
            return <loadingIndicator_1.default />;
        }
        if (!(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return this.renderEmptyMessage();
        }
        return (<releaseListRequest_1.default releases={releases.map(({ version }) => version)} organization={organization} selection={selection} location={location} display={[this.getDisplay()]} releasesReloading={reloading} healthStatsPeriod={location.query.healthStatsPeriod}>
        {({ isHealthLoading, getHealthData }) => {
                var _a;
                const singleProjectSelected = ((_a = selection.projects) === null || _a === void 0 ? void 0 : _a.length) === 1 &&
                    selection.projects[0] !== globalSelectionHeader_2.ALL_ACCESS_PROJECTS;
                const selectedProject = this.getSelectedProject();
                const isMobileProject = (selectedProject === null || selectedProject === void 0 ? void 0 : selectedProject.platform) &&
                    (0, exports.isProjectMobileForReleases)(selectedProject.platform);
                return (<react_1.Fragment>
              {singleProjectSelected && this.projectHasSessions && isMobileProject && (<feature_1.default features={['organizations:release-adoption-chart']}>
                  <releaseAdoptionChart_1.default organization={organization} selection={selection} location={location} router={router} activeDisplay={activeDisplay}/>
                </feature_1.default>)}

              {releases.map((release, index) => (<releaseCard_1.default key={`${release.version}-${release.projects[0].slug}`} activeDisplay={activeDisplay} release={release} organization={organization} location={location} selection={selection} reloading={reloading} showHealthPlaceholders={isHealthLoading} isTopRelease={index === 0} getHealthData={getHealthData} showReleaseAdoptionStages={showReleaseAdoptionStages}/>))}
              <pagination_1.default pageLinks={releasesPageLinks}/>
            </react_1.Fragment>);
            }}
      </releaseListRequest_1.default>);
    }
    renderBody() {
        const { organization, selection } = this.props;
        const { releases, reloading, error } = this.state;
        const activeSort = this.getSort();
        const activeStatus = this.getStatus();
        const activeDisplay = this.getDisplay();
        const hasSemver = organization.features.includes('semver');
        const hasReleaseStages = organization.features.includes('release-adoption-stage');
        const hasAnyMobileProject = selection.projects
            .map(id => `${id}`)
            .map(projectsStore_1.default.getById)
            .some(project => (project === null || project === void 0 ? void 0 : project.platform) && (0, exports.isProjectMobileForReleases)(project.platform));
        const showReleaseAdoptionStages = hasReleaseStages && hasAnyMobileProject && selection.environments.length === 1;
        const hasReleasesSetup = releases && releases.length > 0;
        return (<globalSelectionHeader_1.default showAbsolute={false} timeRangeHint={(0, locale_1.t)('Changing this date range will recalculate the release metrics.')}>
        <organization_1.PageContent>
          <noProjectMessage_1.default organization={organization}>
            <organization_1.PageHeader>
              <pageHeading_1.default>{(0, locale_1.t)('Releases')}</pageHeading_1.default>
            </organization_1.PageHeader>

            {this.renderHealthCta()}

            <SortAndFilterWrapper>
              {hasSemver ? (<guideAnchor_1.default target="releases_search" position="bottom" disabled={!hasReleasesSetup}>
                  <guideAnchor_1.default target="release_stages" position="bottom" disabled={!showReleaseAdoptionStages}>
                    <smartSearchBar_1.default searchSource="releases" query={this.getQuery()} placeholder={(0, locale_1.t)('Search by version, build, package, or stage')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={this.handleSearch} onGetTagValues={this.getTagValues}/>
                  </guideAnchor_1.default>
                </guideAnchor_1.default>) : (<searchBar_1.default placeholder={(0, locale_1.t)('Search')} onSearch={this.handleSearch} query={this.getQuery()}/>)}
              <DropdownsWrapper>
                <releaseListStatusOptions_1.default selected={activeStatus} onSelect={this.handleStatus}/>
                <releaseListSortOptions_1.default selected={activeSort} selectedDisplay={activeDisplay} onSelect={this.handleSortBy} environments={selection.environments} organization={organization}/>
                <releaseDisplayOptions_1.default selected={activeDisplay} onSelect={this.handleDisplay}/>
              </DropdownsWrapper>
            </SortAndFilterWrapper>

            {!reloading &&
                activeStatus === utils_2.StatusOption.ARCHIVED &&
                !!(releases === null || releases === void 0 ? void 0 : releases.length) && <releaseArchivedNotice_1.default multi/>}

            {error
                ? super.renderError(new Error('Unable to load all required endpoints'))
                : this.renderInnerBody(activeDisplay, showReleaseAdoptionStages)}
          </noProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    }
}
exports.ReleasesList = ReleasesList;
const AlertText = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  gap: ${(0, space_1.default)(2)};

  > *:nth-child(1) {
    flex: 1;
  }
  flex-direction: column;
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    flex-direction: row;
  }
`;
const SortAndFilterWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  justify-content: stretch;
  margin-bottom: ${(0, space_1.default)(2)};

  > *:nth-child(1) {
    flex: 1;
  }

  /* Below this width search bar needs its own row no to wrap placeholder text
   * Above this width search bar and controls can be on the same row */
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    flex-direction: row;
  }
`;
const DropdownsWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;

  & > * {
    margin-top: ${(0, space_1.default)(2)};
  }

  /* At the narrower widths wrapper is on its own in a row
   * Expand the dropdown controls to fill the empty space */
  & button {
    width: 100%;
  }

  /* At narrower widths space bar needs a separate row
   * Divide space evenly when 3 dropdowns are in their own row */
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    margin-top: ${(0, space_1.default)(2)};

    & > * {
      margin-top: ${(0, space_1.default)(0)};
      margin-left: ${(0, space_1.default)(2)};
    }

    & > *:nth-child(1) {
      margin-left: ${(0, space_1.default)(0)};
    }

    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }

  /* At wider widths everything is in 1 row
   * Auto space dropdowns when they are in the same row with search bar */
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    margin-top: ${(0, space_1.default)(0)};

    & > * {
      margin-left: ${(0, space_1.default)(2)} !important;
    }

    display: grid;
    grid-template-columns: auto auto auto;
  }
`;
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)((0, withGlobalSelection_1.default)(ReleasesList)));
//# sourceMappingURL=index.jsx.map