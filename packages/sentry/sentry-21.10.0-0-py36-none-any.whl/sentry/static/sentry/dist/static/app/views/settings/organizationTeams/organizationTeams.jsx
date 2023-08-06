Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const allTeamsList_1 = (0, tslib_1.__importDefault)(require("./allTeamsList"));
const organizationAccessRequests_1 = (0, tslib_1.__importDefault)(require("./organizationAccessRequests"));
function OrganizationTeams({ organization, access, features, routes, params, requestList, onRemoveAccessRequest, }) {
    if (!organization) {
        return null;
    }
    const canCreateTeams = access.has('project:admin');
    const action = (<button_1.default priority="primary" size="small" disabled={!canCreateTeams} title={!canCreateTeams ? (0, locale_1.t)('You do not have permission to create teams') : undefined} onClick={() => (0, modal_1.openCreateTeamModal)({
            organization,
        })} icon={<icons_1.IconAdd size="xs" isCircled/>}>
      {(0, locale_1.t)('Create Team')}
    </button_1.default>);
    const teamRoute = routes.find(({ path }) => path === 'teams/');
    const urlPrefix = teamRoute
        ? (0, recreateRoute_1.default)(teamRoute, { routes, params, stepBack: -2 })
        : '';
    const title = (0, locale_1.t)('Teams');
    const [teamQuery, setTeamQuery] = (0, react_1.useState)('');
    const { initiallyLoaded } = (0, useTeams_1.default)({ provideUserTeams: true });
    const { teams, onSearch } = (0, useTeams_1.default)();
    const debouncedSearch = (0, debounce_1.default)(onSearch, constants_1.DEFAULT_DEBOUNCE_DURATION);
    function handleSearch(query) {
        setTeamQuery(query);
        debouncedSearch(query);
    }
    const filteredTeams = teams.filter(team => `#${team.slug}`.toLowerCase().includes(teamQuery.toLowerCase()));
    const [userTeams, otherTeams] = (0, partition_1.default)(filteredTeams, team => team.isMember);
    return (<div data-test-id="team-list">
      <sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}/>
      <settingsPageHeader_1.default title={title} action={action}/>

      <organizationAccessRequests_1.default orgId={params.orgId} requestList={requestList} onRemoveAccessRequest={onRemoveAccessRequest}/>
      <StyledSearchBar placeholder={(0, locale_1.t)('Search teams')} onChange={handleSearch} query={teamQuery}/>
      <panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Your Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          {initiallyLoaded ? (<allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={userTeams.filter(team => team.slug.includes(teamQuery))} access={access} openMembership={false}/>) : (<loadingIndicator_1.default />)}
        </panels_1.PanelBody>
      </panels_1.Panel>
      <panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Other Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={otherTeams} access={access} openMembership={!!(features.has('open-membership') || access.has('org:write'))}/>
        </panels_1.PanelBody>
      </panels_1.Panel>
    </div>);
}
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = OrganizationTeams;
//# sourceMappingURL=organizationTeams.jsx.map