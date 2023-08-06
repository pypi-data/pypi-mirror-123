Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const modal_1 = require("app/actionCreators/modal");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const parser_1 = require("app/components/arithmeticInput/parser");
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const banner_1 = (0, tslib_1.__importDefault)(require("app/components/banner"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = require("app/components/createAlertButton");
const dropdownControl_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownControl"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const urls_1 = require("app/utils/discover/urls");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const discoverQueryMenu_1 = (0, tslib_1.__importDefault)(require("./discoverQueryMenu"));
const utils_1 = require("./utils");
class SavedQueryButtonGroup extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            isNewQuery: true,
            isEditingQuery: false,
            queryName: '',
        };
        this.onBlurInput = (event) => {
            const target = event.target;
            this.setState({ queryName: target.value });
        };
        this.onChangeInput = (event) => {
            const target = event.target;
            this.setState({ queryName: target.value });
        };
        /**
         * There are two ways to create a query
         * 1) Creating a query from scratch and saving it
         * 2) Modifying an existing query and saving it
         */
        this.handleCreateQuery = (event) => {
            event.preventDefault();
            event.stopPropagation();
            const { api, organization, eventView, yAxis } = this.props;
            if (!this.state.queryName) {
                return;
            }
            const nextEventView = eventView.clone();
            nextEventView.name = this.state.queryName;
            // Checks if "Save as" button is clicked from a clean state, or it is
            // clicked while modifying an existing query
            const isNewQuery = !eventView.id;
            (0, utils_1.handleCreateQuery)(api, organization, nextEventView, yAxis, isNewQuery).then((savedQuery) => {
                const view = eventView_1.default.fromSavedQuery(savedQuery);
                banner_1.default.dismiss('discover');
                this.setState({ queryName: '' });
                react_router_1.browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
            });
        };
        this.handleUpdateQuery = (event) => {
            event.preventDefault();
            event.stopPropagation();
            const { api, organization, eventView, updateCallback, yAxis } = this.props;
            (0, utils_1.handleUpdateQuery)(api, organization, eventView, yAxis).then((savedQuery) => {
                const view = eventView_1.default.fromSavedQuery(savedQuery);
                this.setState({ queryName: '' });
                react_router_1.browserHistory.push(view.getResultsViewShortUrlTarget(organization.slug));
                updateCallback();
            });
        };
        this.handleDeleteQuery = (event) => {
            event.preventDefault();
            event.stopPropagation();
            const { api, organization, eventView } = this.props;
            (0, utils_1.handleDeleteQuery)(api, organization, eventView).then(() => {
                react_router_1.browserHistory.push({
                    pathname: (0, urls_1.getDiscoverLandingUrl)(organization),
                    query: {},
                });
            });
        };
        this.handleCreateAlertSuccess = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'success',
                organization_id: organization.id,
                url: window.location.href,
            });
        };
        this.handleAddDashboardWidget = () => {
            var _a;
            const { organization, eventView, savedQuery, yAxis } = this.props;
            // If a Y-Axis value is an equation, we need to check if functions used in the equation also exist in the Y-Axis list
            const validYAxis = yAxis.filter(field => {
                if ((0, fields_1.isEquation)(field)) {
                    const parsed = (0, parser_1.parseArithmetic)((0, fields_1.getEquation)(field));
                    return (!parsed.error &&
                        parsed.tc.functions.every(({ term }) => typeof term === 'string' && yAxis.includes(term)));
                }
                return true;
            });
            const defaultWidgetQuery = {
                name: '',
                fields: validYAxis && validYAxis.length > 0 ? validYAxis : ['count()'],
                conditions: eventView.query,
                orderby: '',
            };
            (0, trackAdvancedAnalyticsEvent_1.default)('discover_views.add_to_dashboard.modal_open', {
                organization,
                saved_query: !!savedQuery,
            });
            (0, modal_1.openAddDashboardWidgetModal)({
                organization,
                fromDiscover: true,
                defaultWidgetQuery,
                defaultTableColumns: eventView.fields.map(({ field }) => field),
                defaultTitle: (_a = savedQuery === null || savedQuery === void 0 ? void 0 : savedQuery.name) !== null && _a !== void 0 ? _a : (eventView.name !== 'All Events' ? eventView.name : undefined),
            });
        };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        const { eventView: nextEventView, savedQuery, savedQueryLoading, yAxis } = nextProps;
        // For a new unsaved query
        if (!savedQuery) {
            return {
                isNewQuery: true,
                isEditingQuery: false,
                queryName: prevState.queryName || '',
            };
        }
        if (savedQueryLoading) {
            return prevState;
        }
        const savedEventView = eventView_1.default.fromSavedQuery(savedQuery);
        // Switching from a SavedQuery to another SavedQuery
        if (savedEventView.id !== nextEventView.id) {
            return {
                isNewQuery: false,
                isEditingQuery: false,
                queryName: '',
            };
        }
        // For modifying a SavedQuery
        const isEqualQuery = nextEventView.isEqualTo(savedEventView);
        // undefined saved yAxis defaults to count() and string values are converted to array
        const isEqualYAxis = (0, isEqual_1.default)(yAxis, !savedQuery.yAxis
            ? ['count()']
            : typeof savedQuery.yAxis === 'string'
                ? [savedQuery.yAxis]
                : savedQuery.yAxis);
        return {
            isNewQuery: false,
            isEditingQuery: !isEqualQuery || !isEqualYAxis,
            // HACK(leedongwei): See comment at SavedQueryButtonGroup.onFocusInput
            queryName: prevState.queryName || '',
        };
    }
    renderButtonSaveAs(disabled) {
        const { queryName } = this.state;
        /**
         * For a great UX, we should focus on `ButtonSaveInput` when `ButtonSave`
         * is clicked. However, `DropdownControl` wraps them in a FunctionComponent
         * which breaks `React.createRef`.
         */
        return (<dropdownControl_1.default alignRight menuWidth="220px" priority="default" buttonProps={{
                'aria-label': (0, locale_1.t)('Save as'),
                showChevron: false,
                icon: <icons_1.IconStar />,
                disabled,
            }} label={`${(0, locale_1.t)('Save as')}\u{2026}`}>
        <ButtonSaveDropDown onClick={SavedQueryButtonGroup.stopEventPropagation}>
          <ButtonSaveInput type="text" name="query_name" placeholder={(0, locale_1.t)('Display name')} value={queryName || ''} onBlur={this.onBlurInput} onChange={this.onChangeInput} disabled={disabled}/>
          <button_1.default onClick={this.handleCreateQuery} priority="primary" disabled={disabled || !this.state.queryName} style={{ width: '100%' }}>
            {(0, locale_1.t)('Save for Org')}
          </button_1.default>
        </ButtonSaveDropDown>
      </dropdownControl_1.default>);
    }
    renderButtonSave(disabled) {
        const { isNewQuery, isEditingQuery } = this.state;
        // Existing query that hasn't been modified.
        if (!isNewQuery && !isEditingQuery) {
            return (<button_1.default icon={<icons_1.IconStar color="yellow100" isSolid size="sm"/>} disabled data-test-id="discover2-savedquery-button-saved">
          {(0, locale_1.t)('Saved for Org')}
        </button_1.default>);
        }
        // Existing query with edits, show save and save as.
        if (!isNewQuery && isEditingQuery) {
            return (<React.Fragment>
          <button_1.default onClick={this.handleUpdateQuery} data-test-id="discover2-savedquery-button-update" disabled={disabled}>
            <IconUpdate />
            {(0, locale_1.t)('Save Changes')}
          </button_1.default>
          {this.renderButtonSaveAs(disabled)}
        </React.Fragment>);
        }
        // Is a new query enable saveas
        return this.renderButtonSaveAs(disabled);
    }
    renderButtonDelete(disabled) {
        const { isNewQuery } = this.state;
        if (isNewQuery) {
            return null;
        }
        return (<button_1.default data-test-id="discover2-savedquery-button-delete" onClick={this.handleDeleteQuery} disabled={disabled} icon={<icons_1.IconDelete />}/>);
    }
    renderButtonCreateAlert() {
        const { eventView, organization, projects, onIncompatibleAlertQuery } = this.props;
        return (<guideAnchor_1.default target="create_alert_from_discover">
        <createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={onIncompatibleAlertQuery} onSuccess={this.handleCreateAlertSuccess} referrer="discover" data-test-id="discover2-create-from-discover"/>
      </guideAnchor_1.default>);
    }
    renderDiscoverQueryMenu() {
        const menuOptions = [];
        menuOptions.push(<StyledMenuItem key="add-dashboard-widget-from-discover" onClick={this.handleAddDashboardWidget}>
        {(0, locale_1.t)('Add to Dashboard')} <featureBadge_1.default type="beta" noTooltip/>
      </StyledMenuItem>);
        return <discoverQueryMenu_1.default>{menuOptions}</discoverQueryMenu_1.default>;
    }
    render() {
        const { organization } = this.props;
        const renderDisabled = p => (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={(0, locale_1.t)('Discover queries are disabled')} featureName={(0, locale_1.t)('Discover queries')}/>}>
        {p.children(p)}
      </hovercard_1.default>);
        const renderQueryButton = (renderFunc) => {
            return (<feature_1.default organization={organization} features={['discover-query']} hookName="feature-disabled:discover-saved-query-create" renderDisabled={renderDisabled}>
          {({ hasFeature }) => renderFunc(!hasFeature || this.props.disabled)}
        </feature_1.default>);
        };
        return (<ResponsiveButtonBar gap={1}>
        {renderQueryButton(disabled => this.renderButtonSave(disabled))}
        <feature_1.default organization={organization} features={['incidents']}>
          {({ hasFeature }) => hasFeature && this.renderButtonCreateAlert()}
        </feature_1.default>
        {renderQueryButton(disabled => this.renderButtonDelete(disabled))}
        <feature_1.default organization={organization} features={['connect-discover-and-dashboards', 'dashboards-edit']}>
          {({ hasFeature }) => hasFeature && this.renderDiscoverQueryMenu()}
        </feature_1.default>
      </ResponsiveButtonBar>);
    }
}
/**
 * Stop propagation for the input and container so people can interact with
 * the inputs in the dropdown.
 */
SavedQueryButtonGroup.stopEventPropagation = (event) => {
    const capturedElements = ['LI', 'INPUT'];
    if (event.target instanceof Element &&
        capturedElements.includes(event.target.nodeName)) {
        event.preventDefault();
        event.stopPropagation();
    }
};
SavedQueryButtonGroup.defaultProps = {
    disabled: false,
};
const ResponsiveButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-top: 0;
  }
`;
const ButtonSaveDropDown = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  padding: ${(0, space_1.default)(1)};
  gap: ${(0, space_1.default)(1)};
`;
const ButtonSaveInput = (0, styled_1.default)(input_1.default) `
  height: 40px;
`;
const IconUpdate = (0, styled_1.default)('div') `
  display: inline-block;
  width: 10px;
  height: 10px;

  margin-right: ${(0, space_1.default)(0.75)};
  border-radius: 5px;
  background-color: ${p => p.theme.yellow300};
`;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  white-space: nowrap;
  span {
    align-items: baseline;
  }
`;
exports.default = (0, withProjects_1.default)((0, withApi_1.default)(SavedQueryButtonGroup));
//# sourceMappingURL=index.jsx.map