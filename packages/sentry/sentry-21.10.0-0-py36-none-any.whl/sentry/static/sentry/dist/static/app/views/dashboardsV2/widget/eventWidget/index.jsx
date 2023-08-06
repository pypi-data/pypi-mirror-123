Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const dashboards_1 = require("app/actionCreators/dashboards");
const indicator_1 = require("app/actionCreators/indicator");
const widgetQueryFields_1 = (0, tslib_1.__importDefault)(require("app/components/dashboards/widgetQueryFields"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const fields_1 = require("app/utils/discover/fields");
const measurements_1 = (0, tslib_1.__importDefault)(require("app/utils/measurements/measurements"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTags_1 = (0, tslib_1.__importDefault)(require("app/utils/withTags"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const widgetCard_1 = (0, tslib_1.__importDefault)(require("app/views/dashboardsV2/widgetCard"));
const utils_2 = require("app/views/eventsV2/utils");
const types_1 = require("../../types");
const buildStep_1 = (0, tslib_1.__importDefault)(require("../buildStep"));
const buildSteps_1 = (0, tslib_1.__importDefault)(require("../buildSteps"));
const choseDataStep_1 = (0, tslib_1.__importDefault)(require("../choseDataStep"));
const header_1 = (0, tslib_1.__importDefault)(require("../header"));
const utils_3 = require("../utils");
const queries_1 = (0, tslib_1.__importDefault)(require("./queries"));
const utils_4 = require("./utils");
const newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
class EventWidget extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleFieldChange = (field, value) => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                if (field === 'displayType') {
                    (0, set_1.default)(newState, 'queries', (0, utils_4.normalizeQueries)(value, state.queries));
                    if (state.title === (0, locale_1.t)('Custom %s Widget', state.displayType) ||
                        state.title === (0, locale_1.t)('Custom %s Widget', types_1.DisplayType.AREA)) {
                        return Object.assign(Object.assign({}, newState), { title: (0, locale_1.t)('Custom %s Widget', utils_3.displayTypes[value]), widgetErrors: undefined });
                    }
                    (0, set_1.default)(newState, field, value);
                }
                return Object.assign(Object.assign({}, newState), { widgetErrors: undefined });
            });
        };
        this.handleRemoveQuery = (index) => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                newState.queries.splice(index, 1);
                return Object.assign(Object.assign({}, newState), { widgetErrors: undefined });
            });
        };
        this.handleAddQuery = () => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                newState.queries.push((0, cloneDeep_1.default)(newQuery));
                return newState;
            });
        };
        this.handleChangeQuery = (index, query) => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                (0, set_1.default)(newState, `queries.${index}`, query);
                return Object.assign(Object.assign({}, newState), { widgetErrors: undefined });
            });
        };
        this.handleSave = (event) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            event.preventDefault();
            this.setState({ loading: true });
            const { organization, onAdd, isEditing, onUpdate, widget } = this.props;
            try {
                const widgetData = (0, pick_1.default)(this.state, [
                    'title',
                    'displayType',
                    'interval',
                    'queries',
                ]);
                yield (0, dashboards_1.validateWidget)(this.api, organization.slug, widgetData);
                if (isEditing) {
                    onUpdate(Object.assign({ id: widget.id }, widgetData));
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Updated widget'));
                    return;
                }
                onAdd(widgetData);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Added widget'));
            }
            catch (err) {
                const widgetErrors = (0, utils_4.mapErrors)((_a = err === null || err === void 0 ? void 0 : err.responseJSON) !== null && _a !== void 0 ? _a : {}, {});
                this.setState({ widgetErrors });
            }
            finally {
                this.setState({ loading: false });
            }
        });
    }
    getDefaultState() {
        const { widget } = this.props;
        if (!widget) {
            return Object.assign(Object.assign({}, super.getDefaultState()), { title: (0, locale_1.t)('Custom %s Widget', utils_3.displayTypes[types_1.DisplayType.AREA]), displayType: types_1.DisplayType.AREA, interval: '5m', queries: [Object.assign({}, newQuery)] });
        }
        return Object.assign(Object.assign({}, super.getDefaultState()), { title: widget.title, displayType: widget.displayType, interval: widget.interval, queries: (0, utils_4.normalizeQueries)(widget.displayType, widget.queries), widgetErrors: undefined });
    }
    getFirstQueryError(field) {
        var _a;
        const { widgetErrors } = this.state;
        if (!widgetErrors) {
            return undefined;
        }
        const [key, value] = (_a = Object.entries(widgetErrors).find((widgetErrorKey, _) => String(widgetErrorKey) === field)) !== null && _a !== void 0 ? _a : [];
        if ((0, utils_1.defined)(key) && (0, utils_1.defined)(value)) {
            return { [key]: value };
        }
        return undefined;
    }
    renderBody() {
        const { organization, onChangeDataSet, selection, tags, isEditing, goBackLocation, dashboardTitle, onDelete, } = this.props;
        const { title, displayType, queries, interval, widgetErrors } = this.state;
        const orgSlug = organization.slug;
        const explodedFields = queries[0].fields.map(field => (0, fields_1.explodeField)({ field }));
        function fieldOptions(measurementKeys) {
            return (0, utils_2.generateFieldOptions)({
                organization,
                tagKeys: Object.values(tags).map(({ key }) => key),
                measurementKeys,
            });
        }
        return (<StyledPageContent>
        <header_1.default dashboardTitle={dashboardTitle} orgSlug={orgSlug} title={title} isEditing={isEditing} onChangeTitle={newTitle => this.handleFieldChange('title', newTitle)} onSave={this.handleSave} onDelete={onDelete} goBackLocation={goBackLocation}/>
        <Layout.Body>
          <buildSteps_1.default>
            <buildStep_1.default title={(0, locale_1.t)('Choose your visualization')} description={(0, locale_1.t)('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <selectControl_1.default name="displayType" options={Object.keys(utils_3.displayTypes).map(value => ({
                label: utils_3.displayTypes[value],
                value,
            }))} value={displayType} onChange={(option) => {
                this.handleFieldChange('displayType', option.value);
            }} error={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.displayType}/>
                <widgetCard_1.default api={this.api} organization={organization} selection={selection} widget={{ title, queries, displayType, interval }} isEditing={false} onDelete={() => undefined} onEdit={() => undefined} renderErrorMessage={errorMessage => typeof errorMessage === 'string' && (<panels_1.PanelAlert type="error">{errorMessage}</panels_1.PanelAlert>)} isSorting={false} currentWidgetDragging={false}/>
              </VisualizationWrapper>
            </buildStep_1.default>
            <choseDataStep_1.default value={utils_3.DataSet.EVENTS} onChange={onChangeDataSet}/>
            <buildStep_1.default title={(0, locale_1.t)('Begin your search')} description={(0, locale_1.t)('Add another query to compare projects, tags, etc.')}>
              <queries_1.default queries={queries} selectedProjectIds={selection.projects} organization={organization} displayType={displayType} onRemoveQuery={this.handleRemoveQuery} onAddQuery={this.handleAddQuery} onChangeQuery={this.handleChangeQuery} errors={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.queries}/>
            </buildStep_1.default>
            <measurements_1.default organization={organization}>
              {({ measurements }) => {
                const measurementKeys = Object.values(measurements).map(({ key }) => key);
                const amendedFieldOptions = fieldOptions(measurementKeys);
                const buildStepContent = (<widgetQueryFields_1.default style={{ padding: 0 }} errors={this.getFirstQueryError('fields')} displayType={displayType} fieldOptions={amendedFieldOptions} fields={explodedFields} organization={organization} onChange={fields => {
                        const fieldStrings = fields.map(field => (0, fields_1.generateFieldAsString)(field));
                        queries.forEach((query, queryIndex) => {
                            const clonedQuery = (0, cloneDeep_1.default)(query);
                            clonedQuery.fields = fieldStrings;
                            this.handleChangeQuery(queryIndex, clonedQuery);
                        });
                    }}/>);
                return (<buildStep_1.default title={displayType === types_1.DisplayType.TABLE
                        ? (0, locale_1.t)('Choose your columns')
                        : (0, locale_1.t)('Choose your y-axis')} description={(0, locale_1.t)('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
                    {buildStepContent}
                  </buildStep_1.default>);
            }}
            </measurements_1.default>
          </buildSteps_1.default>
        </Layout.Body>
      </StyledPageContent>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withGlobalSelection_1.default)((0, withTags_1.default)(EventWidget)));
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const VisualizationWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
`;
//# sourceMappingURL=index.jsx.map