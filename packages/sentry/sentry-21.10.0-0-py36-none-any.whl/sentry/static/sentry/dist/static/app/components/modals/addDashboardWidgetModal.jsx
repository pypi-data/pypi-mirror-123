Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_select_1 = require("react-select");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const dashboards_1 = require("app/actionCreators/dashboards");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const widgetQueriesForm_1 = (0, tslib_1.__importDefault)(require("app/components/dashboards/widgetQueriesForm"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const measurements_1 = (0, tslib_1.__importDefault)(require("app/utils/measurements/measurements"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withTags_1 = (0, tslib_1.__importDefault)(require("app/utils/withTags"));
const data_1 = require("app/views/dashboardsV2/data");
const types_1 = require("app/views/dashboardsV2/types");
const utils_1 = require("app/views/dashboardsV2/widget/eventWidget/utils");
const widgetCard_1 = (0, tslib_1.__importDefault)(require("app/views/dashboardsV2/widgetCard"));
const utils_2 = require("app/views/eventsV2/utils");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("../tooltip"));
const newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
class AddDashboardWidgetModal extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = (event) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            event.preventDefault();
            const { api, closeModal, organization, onAddWidget, onUpdateWidget, widget: previousWidget, fromDiscover, } = this.props;
            this.setState({ loading: true });
            let errors = {};
            const widgetData = (0, pick_1.default)(this.state, [
                'title',
                'displayType',
                'interval',
                'queries',
            ]);
            try {
                yield (0, dashboards_1.validateWidget)(api, organization.slug, widgetData);
                if (typeof onUpdateWidget === 'function' && !!previousWidget) {
                    onUpdateWidget(Object.assign({ id: previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.id }, widgetData));
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Updated widget.'));
                }
                else if (onAddWidget) {
                    onAddWidget(widgetData);
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Added widget.'));
                }
                if (!fromDiscover) {
                    closeModal();
                }
            }
            catch (err) {
                errors = (0, utils_1.mapErrors)((_a = err === null || err === void 0 ? void 0 : err.responseJSON) !== null && _a !== void 0 ? _a : {}, {});
                this.setState({ errors });
            }
            finally {
                this.setState({ loading: false });
                if (fromDiscover) {
                    this.handleSubmitFromDiscover(errors, widgetData);
                }
            }
        });
        this.handleSubmitFromDiscover = (errors, widgetData) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { closeModal, organization } = this.props;
            const { selectedDashboard, dashboards } = this.state;
            // Validate that a dashboard was selected since api call to /dashboards/widgets/ does not check for dashboard
            if (!selectedDashboard ||
                !(dashboards.find(({ title, id }) => {
                    return title === (selectedDashboard === null || selectedDashboard === void 0 ? void 0 : selectedDashboard.label) && id === (selectedDashboard === null || selectedDashboard === void 0 ? void 0 : selectedDashboard.value);
                }) || selectedDashboard.value === 'new')) {
                errors.dashboard = (0, locale_1.t)('This field may not be blank');
                this.setState({ errors });
            }
            if (!Object.keys(errors).length && selectedDashboard) {
                closeModal();
                const queryData = {
                    queryNames: [],
                    queryConditions: [],
                    queryFields: widgetData.queries[0].fields,
                    queryOrderby: widgetData.queries[0].orderby,
                };
                widgetData.queries.forEach(query => {
                    queryData.queryNames.push(query.name);
                    queryData.queryConditions.push(query.conditions);
                });
                const pathQuery = Object.assign({ displayType: widgetData.displayType, interval: widgetData.interval, title: widgetData.title }, queryData);
                (0, trackAdvancedAnalyticsEvent_1.default)('discover_views.add_to_dashboard.confirm', {
                    organization,
                });
                if (selectedDashboard.value === 'new') {
                    react_router_1.browserHistory.push({
                        pathname: `/organizations/${organization.slug}/dashboards/new/`,
                        query: pathQuery,
                    });
                }
                else {
                    react_router_1.browserHistory.push({
                        pathname: `/organizations/${organization.slug}/dashboard/${selectedDashboard.value}/`,
                        query: pathQuery,
                    });
                }
            }
        });
        this.handleFieldChange = (field) => (value) => {
            const { defaultWidgetQuery, defaultTableColumns, fromDiscover, organization } = this.props;
            this.setState(prevState => {
                const newState = (0, cloneDeep_1.default)(prevState);
                (0, set_1.default)(newState, field, value);
                if (field === 'displayType') {
                    const displayType = value;
                    const normalized = (0, utils_1.normalizeQueries)(displayType, prevState.queries);
                    // If switching to Table visualization, use saved query fields for Y-Axis if user has not made query changes
                    if (defaultWidgetQuery && defaultTableColumns && !prevState.userHasModified) {
                        if (displayType === types_1.DisplayType.TABLE) {
                            normalized.forEach(query => {
                                query.fields = [...defaultTableColumns];
                            });
                        }
                        else {
                            normalized.forEach(query => {
                                query.fields = [...defaultWidgetQuery.fields];
                            });
                        }
                    }
                    (0, set_1.default)(newState, 'queries', normalized);
                    if (fromDiscover) {
                        (0, trackAdvancedAnalyticsEvent_1.default)('dashboards_views.add_widget_modal.change', {
                            from: 'discoverv2',
                            field,
                            value: displayType,
                            organization,
                        });
                    }
                }
                return Object.assign(Object.assign({}, newState), { errors: undefined });
            });
        };
        this.handleQueryChange = (widgetQuery, index) => {
            this.setState(prevState => {
                const newState = (0, cloneDeep_1.default)(prevState);
                (0, set_1.default)(newState, `queries.${index}`, widgetQuery);
                (0, set_1.default)(newState, 'userHasModified', true);
                return Object.assign(Object.assign({}, newState), { errors: undefined });
            });
        };
        this.handleQueryRemove = (index) => {
            this.setState(prevState => {
                const newState = (0, cloneDeep_1.default)(prevState);
                newState.queries.splice(index, 1);
                return Object.assign(Object.assign({}, newState), { errors: undefined });
            });
        };
        this.handleAddSearchConditions = () => {
            this.setState(prevState => {
                const newState = (0, cloneDeep_1.default)(prevState);
                const query = (0, cloneDeep_1.default)(newQuery);
                query.fields = this.state.queries[0].fields;
                newState.queries.push(query);
                return newState;
            });
        };
        const { widget, defaultWidgetQuery, defaultTitle, fromDiscover } = props;
        if (!widget) {
            this.state = {
                title: defaultTitle !== null && defaultTitle !== void 0 ? defaultTitle : '',
                displayType: types_1.DisplayType.LINE,
                interval: '5m',
                queries: [defaultWidgetQuery ? Object.assign({}, defaultWidgetQuery) : Object.assign({}, newQuery)],
                errors: undefined,
                loading: !!fromDiscover,
                dashboards: [],
                userHasModified: false,
            };
            return;
        }
        this.state = {
            title: widget.title,
            displayType: widget.displayType,
            interval: widget.interval,
            queries: (0, utils_1.normalizeQueries)(widget.displayType, widget.queries),
            errors: undefined,
            loading: false,
            dashboards: [],
            userHasModified: false,
        };
    }
    componentDidMount() {
        const { fromDiscover } = this.props;
        if (fromDiscover)
            this.fetchDashboards();
    }
    canAddSearchConditions() {
        const rightDisplayType = ['line', 'area', 'stacked_area', 'bar'].includes(this.state.displayType);
        const underQueryLimit = this.state.queries.length < 3;
        return rightDisplayType && underQueryLimit;
    }
    fetchDashboards() {
        var _a;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            const promise = api.requestPromise(`/organizations/${organization.slug}/dashboards/`, {
                method: 'GET',
                query: { sort: 'myDashboardsAndRecentlyViewed' },
            });
            try {
                const dashboards = yield promise;
                this.setState({
                    dashboards,
                });
            }
            catch (error) {
                const errorResponse = (_a = error === null || error === void 0 ? void 0 : error.responseJSON) !== null && _a !== void 0 ? _a : null;
                if (errorResponse) {
                    (0, indicator_1.addErrorMessage)(errorResponse);
                }
                else {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to fetch dashboards'));
                }
            }
            this.setState({ loading: false });
        });
    }
    handleDashboardChange(option) {
        this.setState({ selectedDashboard: option });
    }
    renderDashboardSelector() {
        const { errors, loading, dashboards } = this.state;
        const dashboardOptions = dashboards.map(d => {
            return {
                label: d.title,
                value: d.id,
                isDisabled: d.widgetDisplay.length >= types_1.MAX_WIDGETS,
            };
        });
        return (<React.Fragment>
        <p>
          {(0, locale_1.t)(`Choose which dashboard you'd like to add this query to. It will appear as a widget.`)}
        </p>
        <field_1.default label={(0, locale_1.t)('Custom Dashboard')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.dashboard} style={{ marginBottom: (0, space_1.default)(1), position: 'relative' }} required>
          <selectControl_1.default name="dashboard" options={[
                { label: (0, locale_1.t)('+ Create New Dashboard'), value: 'new' },
                ...dashboardOptions,
            ]} onChange={(option) => this.handleDashboardChange(option)} disabled={loading} components={{
                Option: (_a) => {
                    var { label, data } = _a, optionProps = (0, tslib_1.__rest)(_a, ["label", "data"]);
                    return (<tooltip_1.default disabled={!!!data.isDisabled} title={(0, locale_1.tct)('Max widgets ([maxWidgets]) per dashboard reached.', {
                            maxWidgets: types_1.MAX_WIDGETS,
                        })} containerDisplayMode="block" position="right">
                  <react_select_1.components.Option label={label} data={data} {...optionProps}/>
                </tooltip_1.default>);
                },
            }}/>
        </field_1.default>
      </React.Fragment>);
    }
    render() {
        const { Footer, Body, Header, api, organization, selection, tags, fromDiscover, onUpdateWidget, widget: previousWidget, start, end, statsPeriod, } = this.props;
        const state = this.state;
        const errors = state.errors;
        // Construct GlobalSelection object using statsPeriod/start/end props so we can render widget graph using saved timeframe from Saved/Prebuilt Query
        const querySelection = statsPeriod
            ? Object.assign(Object.assign({}, selection), { datetime: { start: null, end: null, period: statsPeriod, utc: null } }) : start && end
            ? Object.assign(Object.assign({}, selection), { datetime: { start, end, period: '', utc: null } }) : selection;
        const fieldOptions = (measurementKeys) => (0, utils_2.generateFieldOptions)({
            organization,
            tagKeys: Object.values(tags).map(({ key }) => key),
            measurementKeys,
        });
        const topNFieldOptions = (measurementKeys) => (0, utils_2.generateFieldOptions)({
            organization,
            tagKeys: Object.values(tags).map(({ key }) => key),
            measurementKeys,
            aggregations: {},
        });
        const isUpdatingWidget = typeof onUpdateWidget === 'function' && !!previousWidget;
        return (<React.Fragment>
        <Header closeButton>
          <h4>
            {fromDiscover
                ? (0, locale_1.t)('Add Widget to Dashboard')
                : isUpdatingWidget
                    ? (0, locale_1.t)('Edit Widget')
                    : (0, locale_1.t)('Add Widget')}
          </h4>
        </Header>
        <Body>
          {fromDiscover && this.renderDashboardSelector()}
          <DoubleFieldWrapper>
            <StyledField data-test-id="widget-name" label={(0, locale_1.t)('Widget Name')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.title} required>
              <input_1.default type="text" name="title" maxLength={255} required value={state.title} onChange={(event) => {
                this.handleFieldChange('title')(event.target.value);
            }} disabled={state.loading}/>
            </StyledField>
            <StyledField data-test-id="chart-type" label={(0, locale_1.t)('Visualization Display')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.displayType} required>
              <selectControl_1.default options={data_1.DISPLAY_TYPE_CHOICES.slice()} name="displayType" value={state.displayType} onChange={option => this.handleFieldChange('displayType')(option.value)} disabled={state.loading}/>
            </StyledField>
          </DoubleFieldWrapper>
          <measurements_1.default organization={organization}>
            {({ measurements }) => {
                const measurementKeys = Object.values(measurements).map(({ key }) => key);
                let amendedFieldOptions;
                if (state.displayType === 'top_n') {
                    amendedFieldOptions = topNFieldOptions(measurementKeys);
                }
                else {
                    amendedFieldOptions = fieldOptions(measurementKeys);
                }
                return (<widgetQueriesForm_1.default organization={organization} selection={querySelection} fieldOptions={amendedFieldOptions} displayType={state.displayType} queries={state.queries} errors={errors === null || errors === void 0 ? void 0 : errors.queries} onChange={(queryIndex, widgetQuery) => this.handleQueryChange(widgetQuery, queryIndex)} canAddSearchConditions={this.canAddSearchConditions()} handleAddSearchConditions={this.handleAddSearchConditions} handleDeleteQuery={this.handleQueryRemove}/>);
            }}
          </measurements_1.default>
          <widgetCard_1.default api={api} organization={organization} selection={querySelection} widget={this.state} isEditing={false} onDelete={() => undefined} onEdit={() => undefined} renderErrorMessage={errorMessage => typeof errorMessage === 'string' && (<panels_1.PanelAlert type="error">{errorMessage}</panels_1.PanelAlert>)} isSorting={false} currentWidgetDragging={false}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default external href="https://docs.sentry.io/product/dashboards/custom-dashboards/#widget-builder">
              {(0, locale_1.t)('Read the docs')}
            </button_1.default>
            <button_1.default data-test-id="add-widget" priority="primary" type="button" onClick={this.handleSubmit} disabled={state.loading} busy={state.loading}>
              {isUpdatingWidget ? (0, locale_1.t)('Update Widget') : (0, locale_1.t)('Add Widget')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    }
}
const DoubleFieldWrapper = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-template-columns: repeat(2, 1fr);
  grid-column-gap: ${(0, space_1.default)(1)};
  width: 100%;
`;
exports.modalCss = (0, react_1.css) `
  width: 100%;
  max-width: 700px;
  margin: 70px auto;
`;
const StyledField = (0, styled_1.default)(field_1.default) `
  position: relative;
`;
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)((0, withTags_1.default)(AddDashboardWidgetModal)));
//# sourceMappingURL=addDashboardWidgetModal.jsx.map