Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const integrations_1 = require("app/actionCreators/integrations");
const repositoryActions_1 = (0, tslib_1.__importDefault)(require("app/actions/repositoryActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const repositoryRow_1 = (0, tslib_1.__importDefault)(require("app/components/repositoryRow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class IntegrationRepos extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        // Called by row to signal repository change.
        this.onRepositoryChange = data => {
            const itemList = this.state.itemList;
            itemList.forEach(item => {
                if (item.id === data.id) {
                    item.status = data.status;
                    // allow for custom scm repositories to be updated, and
                    // url is optional and therefore can be an empty string
                    item.url = data.url === undefined ? item.url : data.url;
                    item.name = data.name || item.name;
                }
            });
            this.setState({ itemList });
            repositoryActions_1.default.resetRepositories();
        };
        this.debouncedSearchRepositoriesRequest = (0, debounce_1.default)(query => this.searchRepositoriesRequest(query), 200);
        this.searchRepositoriesRequest = (searchQuery) => {
            const orgId = this.props.organization.slug;
            const query = { search: searchQuery };
            const endpoint = `/organizations/${orgId}/integrations/${this.props.integration.id}/repos/`;
            return this.api.request(endpoint, {
                method: 'GET',
                query,
                success: data => {
                    this.setState({ integrationRepos: data, dropdownBusy: false });
                },
                error: () => {
                    this.setState({ dropdownBusy: false });
                },
            });
        };
        this.handleSearchRepositories = (e) => {
            this.setState({ dropdownBusy: true });
            this.debouncedSearchRepositoriesRequest(e.target.value);
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { adding: false, itemList: [], integrationRepos: { repos: [], searchable: false }, dropdownBusy: false });
    }
    getEndpoints() {
        const orgId = this.props.organization.slug;
        return [
            ['itemList', `/organizations/${orgId}/repos/`, { query: { status: '' } }],
            [
                'integrationRepos',
                `/organizations/${orgId}/integrations/${this.props.integration.id}/repos/`,
            ],
        ];
    }
    getIntegrationRepos() {
        const integrationId = this.props.integration.id;
        return this.state.itemList.filter(repo => repo.integrationId === integrationId);
    }
    addRepo(selection) {
        const { integration } = this.props;
        const { itemList } = this.state;
        const orgId = this.props.organization.slug;
        this.setState({ adding: true });
        const migratableRepo = itemList.filter(item => {
            if (!(selection.value && item.externalSlug)) {
                return false;
            }
            return selection.value === item.externalSlug;
        })[0];
        let promise;
        if (migratableRepo) {
            promise = (0, integrations_1.migrateRepository)(this.api, orgId, migratableRepo.id, integration);
        }
        else {
            promise = (0, integrations_1.addRepository)(this.api, orgId, selection.value, integration);
        }
        promise.then((repo) => {
            this.setState({ adding: false, itemList: itemList.concat(repo) });
            repositoryActions_1.default.resetRepositories();
        }, () => this.setState({ adding: false }));
    }
    renderDropdown() {
        const access = new Set(this.props.organization.access);
        if (!access.has('org:integrations')) {
            return (<dropdownButton_1.default disabled title={(0, locale_1.t)('You must be an organization owner, manager or admin to add repositories')} isOpen={false} size="xsmall">
          {(0, locale_1.t)('Add Repository')}
        </dropdownButton_1.default>);
        }
        const repositories = new Set(this.state.itemList.filter(item => item.integrationId).map(i => i.externalSlug));
        const repositoryOptions = (this.state.integrationRepos.repos || []).filter(repo => !repositories.has(repo.identifier));
        const items = repositoryOptions.map(repo => ({
            searchKey: repo.name,
            value: repo.identifier,
            label: (<StyledListElement>
          <StyledName>{repo.name}</StyledName>
        </StyledListElement>),
        }));
        const menuHeader = <StyledReposLabel>{(0, locale_1.t)('Repositories')}</StyledReposLabel>;
        const onChange = this.state.integrationRepos.searchable
            ? this.handleSearchRepositories
            : undefined;
        return (<dropdownAutoComplete_1.default items={items} onSelect={this.addRepo.bind(this)} onChange={onChange} menuHeader={menuHeader} emptyMessage={(0, locale_1.t)('No repositories available')} noResultsMessage={(0, locale_1.t)('No repositories found')} busy={this.state.dropdownBusy} alignMenu="right">
        {({ isOpen }) => (<dropdownButton_1.default isOpen={isOpen} size="xsmall" busy={this.state.adding}>
            {(0, locale_1.t)('Add Repository')}
          </dropdownButton_1.default>)}
      </dropdownAutoComplete_1.default>);
    }
    renderError(error) {
        const badRequest = Object.values(this.state.errors).find(resp => resp && resp.status === 400);
        if (badRequest) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.t)('We were unable to fetch repositories for this integration. Try again later. If this error continues, please reconnect this integration by uninstalling and then reinstalling.')}
        </alert_1.default>);
        }
        return super.renderError(error);
    }
    renderBody() {
        const { itemListPageLinks } = this.state;
        const orgId = this.props.organization.slug;
        const itemList = this.getIntegrationRepos() || [];
        const header = (<panels_1.PanelHeader disablePadding hasButtons>
        <HeaderText>{(0, locale_1.t)('Repositories')}</HeaderText>
        <DropdownWrapper>{this.renderDropdown()}</DropdownWrapper>
      </panels_1.PanelHeader>);
        return (<React.Fragment>
        <panels_1.Panel>
          {header}
          <panels_1.PanelBody>
            {itemList.length === 0 && (<emptyMessage_1.default icon={<icons_1.IconCommit />} title={(0, locale_1.t)('Sentry is better with commit data')} description={(0, locale_1.t)('Add a repository to begin tracking its commit data. Then, set up release tracking to unlock features like suspect commits, suggested issue owners, and deploy emails.')} action={<button_1.default href="https://docs.sentry.io/product/releases/">
                    {(0, locale_1.t)('Learn More')}
                  </button_1.default>}/>)}
            {itemList.map(repo => (<repositoryRow_1.default key={repo.id} repository={repo} orgId={orgId} api={this.api} onRepositoryChange={this.onRepositoryChange}/>))}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {itemListPageLinks && (<pagination_1.default pageLinks={itemListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(IntegrationRepos);
const HeaderText = (0, styled_1.default)('div') `
  padding-left: ${(0, space_1.default)(2)};
  flex: 1;
`;
const DropdownWrapper = (0, styled_1.default)('div') `
  padding-right: ${(0, space_1.default)(1)};
  text-transform: none;
`;
const StyledReposLabel = (0, styled_1.default)('div') `
  width: 250px;
  font-size: 0.875em;
  padding: ${(0, space_1.default)(1)} 0;
  text-transform: uppercase;
`;
const StyledListElement = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(0.5)};
`;
const StyledName = (0, styled_1.default)('div') `
  flex-shrink: 1;
  min-width: 0;
  ${overflowEllipsis_1.default};
`;
//# sourceMappingURL=integrationRepos.jsx.map