Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const globalSelectionHeaderRow_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionHeaderRow"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const headerItem_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/headerItem"));
const multipleSelectorSubmitRow_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/multipleSelectorSubmitRow"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const analytics_1 = require("app/utils/analytics");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
/**
 * Environment Selector
 *
 * Note we only fetch environments when this component is mounted
 */
class MultipleEnvironmentSelector extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            selectedEnvs: new Set(this.props.value),
            hasChanges: false,
        };
        this.syncSelectedStateFromProps = () => this.setState({ selectedEnvs: new Set(this.props.value) });
        /**
         * If value in state is different than value from props, propagate changes
         */
        this.doChange = (environments) => {
            this.props.onChange(environments);
        };
        /**
         * Checks if "onUpdate" is callable. Only calls if there are changes
         */
        this.doUpdate = () => {
            this.setState({ hasChanges: false }, this.props.onUpdate);
        };
        /**
         * Toggle selected state of an environment
         */
        this.toggleSelected = (environment) => {
            this.setState(state => {
                const selectedEnvs = new Set(state.selectedEnvs);
                if (selectedEnvs.has(environment)) {
                    selectedEnvs.delete(environment);
                }
                else {
                    selectedEnvs.add(environment);
                }
                (0, analytics_1.analytics)('environmentselector.toggle', {
                    action: selectedEnvs.has(environment) ? 'added' : 'removed',
                    path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                    org_id: parseInt(this.props.organization.id, 10),
                });
                this.doChange(Array.from(selectedEnvs.values()));
                return {
                    selectedEnvs,
                    hasChanges: true,
                };
            });
        };
        /**
         * Calls "onUpdate" callback and closes the dropdown menu
         */
        this.handleUpdate = (actions) => {
            actions.close();
            this.doUpdate();
        };
        this.handleClose = () => {
            // Only update if there are changes
            if (!this.state.hasChanges) {
                return;
            }
            (0, analytics_1.analytics)('environmentselector.update', {
                count: this.state.selectedEnvs.size,
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            this.doUpdate();
        };
        /**
         * Clears all selected environments and updates
         */
        this.handleClear = () => {
            (0, analytics_1.analytics)('environmentselector.clear', {
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            this.setState({
                hasChanges: false,
                selectedEnvs: new Set(),
            }, () => {
                this.doChange([]);
                this.doUpdate();
            });
        };
        /**
         * Selects an environment, should close menu and initiate an update
         */
        this.handleSelect = (item) => {
            const { value: environment } = item;
            (0, analytics_1.analytics)('environmentselector.direct_selection', {
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            this.setState(() => {
                this.doChange([environment]);
                return {
                    selectedEnvs: new Set([environment]),
                };
            }, this.doUpdate);
        };
        /**
         * Handler for when an environment is selected by the multiple select component
         * Does not initiate an "update"
         */
        this.handleMultiSelect = (environment) => {
            this.toggleSelected(environment);
        };
    }
    componentDidUpdate(prevProps) {
        // Need to sync state
        if (this.props.value !== prevProps.value) {
            this.syncSelectedStateFromProps();
        }
    }
    getEnvironments() {
        const { projects, selectedProjects } = this.props;
        const config = configStore_1.default.getConfig();
        let environments = [];
        projects.forEach(function (project) {
            const projectId = parseInt(project.id, 10);
            // Include environments from:
            // - all projects if the user is a superuser
            // - the requested projects
            // - all member projects if 'my projects' (empty list) is selected.
            // - all projects if -1 is the only selected project.
            if ((selectedProjects.length === 1 &&
                selectedProjects[0] === globalSelectionHeader_1.ALL_ACCESS_PROJECTS &&
                project.hasAccess) ||
                (selectedProjects.length === 0 &&
                    (project.isMember || config.user.isSuperuser)) ||
                selectedProjects.includes(projectId)) {
                environments = environments.concat(project.environments);
            }
        });
        return (0, uniq_1.default)(environments);
    }
    render() {
        const { value, loadingProjects } = this.props;
        const environments = this.getEnvironments();
        const validatedValue = value.filter(env => environments.includes(env));
        const summary = validatedValue.length
            ? `${validatedValue.join(', ')}`
            : (0, locale_1.t)('All Environments');
        return loadingProjects ? (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<icons_1.IconWindow />} loading={loadingProjects} hasChanges={false} hasSelected={false} isOpen={false} locked={false}>
        {(0, locale_1.t)('Loading\u2026')}
      </StyledHeaderItem>) : (<react_1.ClassNames>
        {({ css }) => (<StyledDropdownAutoComplete alignMenu="left" allowActorToggle closeOnSelect blendCorner={false} searchPlaceholder={(0, locale_1.t)('Filter environments')} onSelect={this.handleSelect} onClose={this.handleClose} maxHeight={500} rootClassName={css `
              position: relative;
              display: flex;
              left: -1px;
            `} inputProps={{ style: { padding: 8, paddingLeft: 14 } }} emptyMessage={(0, locale_1.t)('You have no environments')} noResultsMessage={(0, locale_1.t)('No environments found')} virtualizedHeight={theme_1.default.headerSelectorRowHeight} emptyHidesInput menuFooter={({ actions }) => this.state.hasChanges ? (<multipleSelectorSubmitRow_1.default onSubmit={() => this.handleUpdate(actions)}/>) : null} items={environments.map(env => ({
                    value: env,
                    searchKey: env,
                    label: ({ inputValue }) => (<EnvironmentSelectorItem environment={env} inputValue={inputValue} isChecked={this.state.selectedEnvs.has(env)} onMultiSelect={this.handleMultiSelect}/>),
                }))}>
            {({ isOpen, getActorProps }) => (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<icons_1.IconWindow />} isOpen={isOpen} hasSelected={value && !!value.length} onClear={this.handleClear} hasChanges={false} locked={false} loading={false} {...getActorProps()}>
                {summary}
              </StyledHeaderItem>)}
          </StyledDropdownAutoComplete>)}
      </react_1.ClassNames>);
    }
}
MultipleEnvironmentSelector.defaultProps = {
    value: [],
};
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)(MultipleEnvironmentSelector));
const StyledHeaderItem = (0, styled_1.default)(headerItem_1.default) `
  height: 100%;
`;
const StyledDropdownAutoComplete = (0, styled_1.default)(dropdownAutoComplete_1.default) `
  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  position: absolute;
  top: 100%;
  box-shadow: ${p => p.theme.dropShadowLight};
  border-radius: ${p => p.theme.borderRadiusBottom};
  margin-top: 0;
  min-width: 100%;
`;
class EnvironmentSelectorItem extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.handleMultiSelect = () => {
            const { environment, onMultiSelect } = this.props;
            onMultiSelect(environment);
        };
        this.handleClick = (e) => {
            e.stopPropagation();
            this.handleMultiSelect();
        };
    }
    render() {
        const { environment, inputValue, isChecked } = this.props;
        return (<globalSelectionHeaderRow_1.default data-test-id={`environment-${environment}`} checked={isChecked} onCheckClick={this.handleClick}>
        <highlight_1.default text={inputValue}>{environment}</highlight_1.default>
      </globalSelectionHeaderRow_1.default>);
    }
}
//# sourceMappingURL=multipleEnvironmentSelector.jsx.map