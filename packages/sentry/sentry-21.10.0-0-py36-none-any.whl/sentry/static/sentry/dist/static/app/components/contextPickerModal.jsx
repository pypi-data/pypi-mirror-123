Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
const integrationIcon_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationIcon"));
const selectStyles = {
    menu: provided => (Object.assign(Object.assign({}, provided), { position: 'initial', boxShadow: 'none', marginBottom: 0 })),
    option: (provided, state) => (Object.assign(Object.assign({}, provided), { opacity: state.isDisabled ? 0.6 : 1, cursor: state.isDisabled ? 'not-allowed' : 'pointer', pointerEvents: state.isDisabled ? 'none' : 'auto' })),
};
class ContextPickerModal extends react_1.Component {
    constructor() {
        super(...arguments);
        // TODO(ts) The various generics in react-select types make getting this
        // right hard.
        this.orgSelect = null;
        this.projectSelect = null;
        this.configSelect = null;
        // Performs checks to see if we need to prompt user
        // i.e. When there is only 1 org and no project is needed or
        // there is only 1 org and only 1 project (which should be rare)
        this.navigateIfFinish = (organizations, projects, latestOrg = this.props.organization) => {
            var _a;
            const { needProject, onFinish, nextPath, integrationConfigs } = this.props;
            const { isSuperuser } = configStore_1.default.get('user') || {};
            // If no project is needed and theres only 1 org OR
            // if we need a project and there's only 1 project
            // then return because we can't navigate anywhere yet
            if ((!needProject && organizations.length !== 1) ||
                (needProject && projects.length !== 1) ||
                (integrationConfigs.length && isSuperuser)) {
                return;
            }
            // If there is only one org and we don't need a project slug, then call finish callback
            if (!needProject) {
                onFinish((0, replaceRouterParams_1.default)(nextPath, {
                    orgId: organizations[0].slug,
                }));
                return;
            }
            // Use latest org or if only 1 org, use that
            let org = latestOrg;
            if (!org && organizations.length === 1) {
                org = organizations[0].slug;
            }
            onFinish((0, replaceRouterParams_1.default)(nextPath, {
                orgId: org,
                projectId: projects[0].slug,
                project: (_a = this.props.projects.find(p => p.slug === projects[0].slug)) === null || _a === void 0 ? void 0 : _a.id,
            }));
        };
        this.doFocus = (ref) => {
            if (!ref || this.props.loading) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            const el = react_dom_1.default.findDOMNode(ref);
            if (el !== null) {
                const input = el.querySelector('input');
                input && input.focus();
            }
        };
        this.handleSelectOrganization = ({ value }) => {
            // If we do not need to select a project, we can early return after selecting an org
            // No need to fetch org details
            if (!this.props.needProject) {
                this.navigateIfFinish([{ slug: value }], []);
                return;
            }
            this.props.onSelectOrganization(value);
        };
        this.handleSelectProject = ({ value }) => {
            const { organization } = this.props;
            if (!value || !organization) {
                return;
            }
            this.navigateIfFinish([{ slug: organization }], [{ slug: value }]);
        };
        this.handleSelectConfiguration = ({ value }) => {
            const { onFinish, nextPath } = this.props;
            if (!value) {
                return;
            }
            onFinish(`${nextPath}${value}/`);
            return;
        };
        this.getMemberProjects = () => {
            const { projects } = this.props;
            const nonMemberProjects = [];
            const memberProjects = [];
            projects.forEach(project => project.isMember ? memberProjects.push(project) : nonMemberProjects.push(project));
            return [memberProjects, nonMemberProjects];
        };
        this.onMenuOpen = (ref, listItems, valueKey, currentSelected = '') => {
            // Hacky way to pre-focus to an item with newer versions of react select
            // See https://github.com/JedWatson/react-select/issues/3648
            setTimeout(() => {
                if (ref) {
                    const choices = ref.select.state.menuOptions.focusable;
                    const toBeFocused = listItems.find(({ id }) => id === currentSelected);
                    const selectedIndex = toBeFocused
                        ? choices.findIndex(option => option.value === toBeFocused[valueKey])
                        : 0;
                    if (selectedIndex >= 0 && toBeFocused) {
                        // Focusing selected option only if it exists
                        ref.select.scrollToFocusedOptionOnUpdate = true;
                        ref.select.inputIsHiddenAfterUpdate = false;
                        ref.select.setState({
                            focusedValue: null,
                            focusedOption: choices[selectedIndex],
                        });
                    }
                }
            });
        };
        // TODO(TS): Fix typings
        this.customOptionProject = (_a) => {
            var { label } = _a, props = (0, tslib_1.__rest)(_a, ["label"]);
            const project = this.props.projects.find(({ slug }) => props.value === slug);
            if (!project) {
                return null;
            }
            return (<react_select_1.components.Option label={label} {...props}>
        <idBadge_1.default project={project} avatarSize={20} displayName={label} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.Option>);
        };
    }
    componentDidMount() {
        const { organization, projects, organizations } = this.props;
        // Don't make any assumptions if there are multiple organizations
        if (organizations.length !== 1) {
            return;
        }
        // If there is an org in context (and there's only 1 org available),
        // attempt to see if we need more info from user and redirect otherwise
        if (organization) {
            // This will handle if we can intelligently move the user forward
            this.navigateIfFinish([{ slug: organization }], projects);
            return;
        }
    }
    componentDidUpdate(prevProps) {
        // Component may be mounted before projects is fetched, check if we can finish when
        // component is updated with projects
        if (JSON.stringify(prevProps.projects) !== JSON.stringify(this.props.projects)) {
            this.navigateIfFinish(this.props.organizations, this.props.projects);
        }
    }
    get headerText() {
        const { needOrg, needProject, integrationConfigs } = this.props;
        if (needOrg && needProject) {
            return (0, locale_1.t)('Select an organization and a project to continue');
        }
        if (needOrg) {
            return (0, locale_1.t)('Select an organization to continue');
        }
        if (needProject) {
            return (0, locale_1.t)('Select a project to continue');
        }
        if (integrationConfigs.length) {
            return (0, locale_1.t)('Select a configuration to continue');
        }
        // if neither project nor org needs to be selected, nothing will render anyways
        return '';
    }
    renderProjectSelectOrMessage() {
        const { organization, projects, comingFromProjectId } = this.props;
        const [memberProjects, nonMemberProjects] = this.getMemberProjects();
        const { isSuperuser } = configStore_1.default.get('user') || {};
        const projectOptions = [
            {
                label: (0, locale_1.t)('My Projects'),
                options: memberProjects.map(p => ({
                    value: p.slug,
                    label: (0, locale_1.t)(`${p.slug}`),
                    isDisabled: false,
                })),
            },
            {
                label: (0, locale_1.t)('All Projects'),
                options: nonMemberProjects.map(p => ({
                    value: p.slug,
                    label: (0, locale_1.t)(`${p.slug}`),
                    isDisabled: isSuperuser ? false : true,
                })),
            },
        ];
        if (!projects.length) {
            return (<div>
          {(0, locale_1.tct)('You have no projects. Click [link] to make one.', {
                    link: (<link_1.default to={`/organizations/${organization}/projects/new/`}>{(0, locale_1.t)('here')}</link_1.default>),
                })}
        </div>);
        }
        return (<StyledSelectControl ref={(ref) => {
                this.projectSelect = ref;
                this.doFocus(this.projectSelect);
            }} placeholder={(0, locale_1.t)('Select a Project to continue')} name="project" options={projectOptions} onChange={this.handleSelectProject} onMenuOpen={() => this.onMenuOpen(this.projectSelect, projects, 'slug', comingFromProjectId)} components={{ Option: this.customOptionProject, DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>);
    }
    renderIntegrationConfigs() {
        const { integrationConfigs } = this.props;
        const { isSuperuser } = configStore_1.default.get('user') || {};
        const options = [
            {
                label: (0, locale_1.tct)('[providerName] Configurations', {
                    providerName: integrationConfigs[0].provider.name,
                }),
                options: integrationConfigs.map(config => ({
                    value: config.id,
                    label: (<StyledIntegrationItem>
              <integrationIcon_1.default size={22} integration={config}/>
              <span>{config.domainName}</span>
            </StyledIntegrationItem>),
                    isDisabled: isSuperuser ? false : true,
                })),
            },
        ];
        return (<StyledSelectControl ref={(ref) => {
                this.configSelect = ref;
                this.doFocus(this.configSelect);
            }} placeholder={(0, locale_1.t)('Select a configuration to continue')} name="configurations" options={options} onChange={this.handleSelectConfiguration} onMenuOpen={() => this.onMenuOpen(this.configSelect, integrationConfigs, 'id')} components={{ DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>);
    }
    render() {
        const { needOrg, needProject, organization, organizations, loading, Header, Body, integrationConfigs, } = this.props;
        const { isSuperuser } = configStore_1.default.get('user') || {};
        const shouldShowProjectSelector = organization && needProject && !loading;
        const shouldShowConfigSelector = integrationConfigs.length > 0 && isSuperuser;
        const orgChoices = organizations
            .filter(({ status }) => status.id !== 'pending_deletion')
            .map(({ slug }) => ({ label: slug, value: slug }));
        const shouldShowPicker = needOrg || needProject || shouldShowConfigSelector;
        if (!shouldShowPicker) {
            return null;
        }
        return (<react_1.Fragment>
        <Header closeButton>{this.headerText}</Header>
        <Body>
          {loading && <StyledLoadingIndicator overlay/>}
          {needOrg && (<StyledSelectControl ref={(ref) => {
                    this.orgSelect = ref;
                    if (shouldShowProjectSelector) {
                        return;
                    }
                    this.doFocus(this.orgSelect);
                }} placeholder={(0, locale_1.t)('Select an Organization')} name="organization" options={orgChoices} value={organization} onChange={this.handleSelectOrganization} components={{ DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>)}

          {shouldShowProjectSelector && this.renderProjectSelectOrMessage()}
          {shouldShowConfigSelector && this.renderIntegrationConfigs()}
        </Body>
      </react_1.Fragment>);
    }
}
class ContextPickerModalContainer extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.unlistener = organizationsStore_1.default.listen((organizations) => this.setState({ organizations }), undefined);
        this.handleSelectOrganization = (organizationSlug) => {
            this.setState({ selectedOrganization: organizationSlug });
        };
    }
    getDefaultState() {
        var _a;
        const storeState = organizationStore_1.default.get();
        return Object.assign(Object.assign({}, super.getDefaultState()), { organizations: organizationsStore_1.default.getAll(), selectedOrganization: (_a = storeState.organization) === null || _a === void 0 ? void 0 : _a.slug });
    }
    getEndpoints() {
        const { configUrl } = this.props;
        if (configUrl) {
            return [['integrationConfigs', configUrl]];
        }
        return [];
    }
    componentWillUnmount() {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    renderModal({ projects, initiallyLoaded, integrationConfigs, }) {
        return (<ContextPickerModal {...this.props} projects={projects || []} loading={!initiallyLoaded} organizations={this.state.organizations} organization={this.state.selectedOrganization} onSelectOrganization={this.handleSelectOrganization} integrationConfigs={integrationConfigs || []}/>);
    }
    render() {
        var _a;
        const { projectSlugs, configUrl } = this.props;
        if (configUrl && this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        if ((_a = this.state.integrationConfigs) === null || _a === void 0 ? void 0 : _a.length) {
            return this.renderModal({
                integrationConfigs: this.state.integrationConfigs,
                initiallyLoaded: !this.state.loading,
            });
        }
        if (this.state.selectedOrganization) {
            return (<projects_1.default orgId={this.state.selectedOrganization} allProjects={!(projectSlugs === null || projectSlugs === void 0 ? void 0 : projectSlugs.length)} slugs={projectSlugs}>
          {({ projects, initiallyLoaded }) => this.renderModal({ projects: projects, initiallyLoaded })}
        </projects_1.default>);
        }
        return this.renderModal({});
    }
}
exports.default = ContextPickerModalContainer;
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  margin-top: ${(0, space_1.default)(1)};
`;
const StyledLoadingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  z-index: 1;
`;
const StyledIntegrationItem = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: ${(0, space_1.default)(4)} auto;
  grid-template-rows: 1fr;
`;
//# sourceMappingURL=contextPickerModal.jsx.map