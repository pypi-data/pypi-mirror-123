Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const headerItem_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/headerItem"));
const platformList_1 = (0, tslib_1.__importDefault)(require("app/components/platformList"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const projectSelector_1 = (0, tslib_1.__importDefault)(require("./projectSelector"));
class MultipleProjectSelector extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            hasChanges: false,
        };
        // Reset "hasChanges" state and call `onUpdate` callback
        this.doUpdate = () => {
            this.setState({ hasChanges: false }, this.props.onUpdate);
        };
        /**
         * Handler for when an explicit update call should be made.
         * e.g. an "Update" button
         *
         * Should perform an "update" callback
         */
        this.handleUpdate = (actions) => {
            actions.close();
            this.doUpdate();
        };
        /**
         * Handler for when a dropdown item was selected directly (and not via multi select)
         *
         * Should perform an "update" callback
         */
        this.handleQuickSelect = (selected) => {
            (0, analytics_1.analytics)('projectselector.direct_selection', {
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            const value = selected.id === null ? [] : [parseInt(selected.id, 10)];
            this.props.onChange(value);
            this.doUpdate();
        };
        /**
         * Handler for when dropdown menu closes
         *
         * Should perform an "update" callback
         */
        this.handleClose = () => {
            // Only update if there are changes
            if (!this.state.hasChanges) {
                return;
            }
            const { value, multi } = this.props;
            (0, analytics_1.analytics)('projectselector.update', {
                count: value.length,
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
                multi,
            });
            this.doUpdate();
        };
        /**
         * Handler for clearing the current value
         *
         * Should perform an "update" callback
         */
        this.handleClear = () => {
            (0, analytics_1.analytics)('projectselector.clear', {
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            this.props.onChange([]);
            // Update on clear
            this.doUpdate();
        };
        /**
         * Handler for selecting multiple items, should NOT call update
         */
        this.handleMultiSelect = (selected) => {
            const { onChange, value } = this.props;
            (0, analytics_1.analytics)('projectselector.toggle', {
                action: selected.length > value.length ? 'added' : 'removed',
                path: (0, getRouteStringFromRoutes_1.default)(this.props.router.routes),
                org_id: parseInt(this.props.organization.id, 10),
            });
            const selectedList = selected.map(({ id }) => parseInt(id, 10)).filter(i => i);
            onChange(selectedList);
            this.setState({ hasChanges: true });
        };
    }
    renderProjectName() {
        const { forceProject, location, multi, organization, showIssueStreamLink } = this.props;
        if (showIssueStreamLink && forceProject && multi) {
            return (<tooltip_1.default title={(0, locale_1.t)('Issues Stream')} position="bottom">
          <StyledLink to={{
                    pathname: `/organizations/${organization.slug}/issues/`,
                    query: Object.assign(Object.assign({}, location.query), { project: forceProject.id }),
                }}>
            {forceProject.slug}
          </StyledLink>
        </tooltip_1.default>);
        }
        if (forceProject) {
            return forceProject.slug;
        }
        return '';
    }
    getLockedMessage() {
        const { forceProject, lockedMessageSubject } = this.props;
        if (forceProject) {
            return (0, locale_1.tct)('This [subject] is unique to the [projectSlug] project', {
                subject: lockedMessageSubject,
                projectSlug: forceProject.slug,
            });
        }
        return (0, locale_1.tct)('This [subject] is unique to a project', { subject: lockedMessageSubject });
    }
    render() {
        const { value, projects, isGlobalSelectionReady, nonMemberProjects, multi, organization, shouldForceProject, forceProject, showProjectSettingsLink, footerMessage, } = this.props;
        const selectedProjectIds = new Set(value);
        const allProjects = [...projects, ...nonMemberProjects];
        const selected = allProjects.filter(project => selectedProjectIds.has(parseInt(project.id, 10)));
        // `forceProject` can be undefined if it is loading the project
        // We are intentionally using an empty string as its "loading" state
        return shouldForceProject ? (<StyledHeaderItem data-test-id="global-header-project-selector" icon={forceProject && (<platformList_1.default platforms={forceProject.platform ? [forceProject.platform] : []} max={1}/>)} locked lockedMessage={this.getLockedMessage()} settingsLink={(forceProject &&
                showProjectSettingsLink &&
                `/settings/${organization.slug}/projects/${forceProject.slug}/`) ||
                undefined}>
        {this.renderProjectName()}
      </StyledHeaderItem>) : !isGlobalSelectionReady ? (<StyledHeaderItem data-test-id="global-header-project-selector-loading" icon={<icons_1.IconProject />} loading>
        {(0, locale_1.t)('Loading\u2026')}
      </StyledHeaderItem>) : (<react_1.ClassNames>
        {({ css }) => (<StyledProjectSelector {...this.props} multi={!!multi} selectedProjects={selected} multiProjects={projects} onSelect={this.handleQuickSelect} onClose={this.handleClose} onMultiSelect={this.handleMultiSelect} rootClassName={css `
              display: flex;
            `} menuFooter={({ actions }) => (<SelectorFooterControls selected={selectedProjectIds} multi={multi} organization={organization} hasChanges={this.state.hasChanges} onApply={() => this.handleUpdate(actions)} onShowAllProjects={() => {
                        this.handleQuickSelect({ id: globalSelectionHeader_1.ALL_ACCESS_PROJECTS.toString() });
                        actions.close();
                    }} onShowMyProjects={() => {
                        this.handleClear();
                        actions.close();
                    }} message={footerMessage}/>)}>
            {({ getActorProps, selectedProjects, isOpen }) => {
                    var _a;
                    const hasSelected = !!selectedProjects.length;
                    const title = hasSelected
                        ? selectedProjects.map(({ slug }) => slug).join(', ')
                        : selectedProjectIds.has(globalSelectionHeader_1.ALL_ACCESS_PROJECTS)
                            ? (0, locale_1.t)('All Projects')
                            : (0, locale_1.t)('My Projects');
                    const icon = hasSelected ? (<platformList_1.default platforms={selectedProjects.map(p => { var _a; return (_a = p.platform) !== null && _a !== void 0 ? _a : 'other'; }).reverse()} max={5}/>) : (<icons_1.IconProject />);
                    return (<StyledHeaderItem data-test-id="global-header-project-selector" icon={icon} hasSelected={hasSelected} hasChanges={this.state.hasChanges} isOpen={isOpen} onClear={this.handleClear} allowClear={multi} settingsLink={selectedProjects.length === 1
                            ? `/settings/${organization.slug}/projects/${(_a = selected[0]) === null || _a === void 0 ? void 0 : _a.slug}/`
                            : ''} {...getActorProps()}>
                  {title}
                </StyledHeaderItem>);
                }}
          </StyledProjectSelector>)}
      </react_1.ClassNames>);
    }
}
MultipleProjectSelector.defaultProps = {
    multi: true,
    lockedMessageSubject: (0, locale_1.t)('page'),
};
const SelectorFooterControls = ({ selected, multi, hasChanges, onApply, onShowAllProjects, onShowMyProjects, organization, message, }) => {
    let showMyProjects = false;
    let showAllProjects = false;
    if (multi) {
        showMyProjects = true;
        const hasGlobalRole = organization.role === 'owner' || organization.role === 'manager';
        const hasOpenMembership = organization.features.includes('open-membership');
        const allSelected = selected && selected.has(globalSelectionHeader_1.ALL_ACCESS_PROJECTS);
        if ((hasGlobalRole || hasOpenMembership) && !allSelected) {
            showAllProjects = true;
            showMyProjects = false;
        }
    }
    // Nothing to show.
    if (!(showAllProjects || showMyProjects || hasChanges || message)) {
        return null;
    }
    return (<FooterContainer>
      {message && <FooterMessage>{message}</FooterMessage>}

      <FooterActions>
        {showAllProjects && (<button_1.default onClick={onShowAllProjects} priority="default" size="xsmall">
            {(0, locale_1.t)('View All Projects')}
          </button_1.default>)}
        {showMyProjects && (<button_1.default onClick={onShowMyProjects} priority="default" size="xsmall">
            {(0, locale_1.t)('View My Projects')}
          </button_1.default>)}
        {hasChanges && (<SubmitButton onClick={onApply} size="xsmall" priority="primary">
            {(0, locale_1.t)('Apply Filter')}
          </SubmitButton>)}
      </FooterActions>
    </FooterContainer>);
};
exports.default = (0, react_router_1.withRouter)(MultipleProjectSelector);
const FooterContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)} 0;
`;
const FooterActions = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  & > * {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const SubmitButton = (0, styled_1.default)(button_1.default) `
  animation: 0.1s ${animations_1.growIn} ease-in;
`;
const FooterMessage = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  padding: 0 ${(0, space_1.default)(0.5)};
`;
const StyledProjectSelector = (0, styled_1.default)(projectSelector_1.default) `
  background-color: ${p => p.theme.background};
  color: ${p => p.theme.textColor};
  margin: 1px 0 0 -1px;
  border-radius: ${p => p.theme.borderRadiusBottom};
  width: 100%;
`;
const StyledHeaderItem = (0, styled_1.default)(headerItem_1.default) `
  height: 100%;
  width: 100%;
  ${p => p.locked && 'cursor: default'};
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.subText};

  &:hover {
    color: ${p => p.theme.subText};
  }
`;
//# sourceMappingURL=multipleProjectSelector.jsx.map