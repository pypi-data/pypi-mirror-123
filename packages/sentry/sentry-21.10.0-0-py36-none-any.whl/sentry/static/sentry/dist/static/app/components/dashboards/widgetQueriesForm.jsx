Object.defineProperty(exports, "__esModule", { value: true });
exports.SearchConditionsWrapper = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const widgetQueryFields_1 = (0, tslib_1.__importDefault)(require("./widgetQueryFields"));
const generateOrderOptions = (fields) => {
    const options = [];
    fields.forEach(field => {
        const alias = (0, fields_1.getAggregateAlias)(field);
        options.push({ label: (0, locale_1.t)('%s asc', field), value: alias });
        options.push({ label: (0, locale_1.t)('%s desc', field), value: `-${alias}` });
    });
    return options;
};
/**
 * Contain widget queries interactions and signal changes via the onChange
 * callback. This component's state should live in the parent.
 */
class WidgetQueriesForm extends React.Component {
    constructor() {
        super(...arguments);
        // Handle scalar field values changing.
        this.handleFieldChange = (queryIndex, field) => {
            const { queries, onChange } = this.props;
            const widgetQuery = queries[queryIndex];
            return function handleChange(value) {
                const newQuery = Object.assign(Object.assign({}, widgetQuery), { [field]: value });
                onChange(queryIndex, newQuery);
            };
        };
    }
    getFirstQueryError(key) {
        const { errors } = this.props;
        if (!errors) {
            return undefined;
        }
        return errors.find(queryError => queryError && queryError[key]);
    }
    render() {
        var _a;
        const { organization, selection, errors, queries, canAddSearchConditions, handleAddSearchConditions, handleDeleteQuery, displayType, fieldOptions, onChange, } = this.props;
        const hideLegendAlias = ['table', 'world_map', 'big_number'].includes(displayType);
        const explodedFields = queries[0].fields.map(field => (0, fields_1.explodeField)({ field }));
        return (<QueryWrapper>
        {queries.map((widgetQuery, queryIndex) => {
                return (<field_1.default key={queryIndex} label={queryIndex === 0 ? (0, locale_1.t)('Query') : null} inline={false} style={{ paddingBottom: `8px` }} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors[queryIndex].conditions}>
              <exports.SearchConditionsWrapper>
                <StyledSearchBar searchSource="widget_builder" organization={organization} projectIds={selection.projects} query={widgetQuery.conditions} fields={[]} onSearch={this.handleFieldChange(queryIndex, 'conditions')} onBlur={this.handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
                {!hideLegendAlias && (<LegendAliasInput type="text" name="name" required value={widgetQuery.name} placeholder={(0, locale_1.t)('Legend Alias')} onChange={event => this.handleFieldChange(queryIndex, 'name')(event.target.value)}/>)}
                {queries.length > 1 && (<button_1.default size="zero" borderless onClick={event => {
                            event.preventDefault();
                            handleDeleteQuery(queryIndex);
                        }} icon={<icons_1.IconDelete />} title={(0, locale_1.t)('Remove query')} label={(0, locale_1.t)('Remove query')}/>)}
              </exports.SearchConditionsWrapper>
            </field_1.default>);
            })}
        {canAddSearchConditions && (<button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={(event) => {
                    event.preventDefault();
                    handleAddSearchConditions();
                }}>
            {(0, locale_1.t)('Add Query')}
          </button_1.default>)}
        <widgetQueryFields_1.default displayType={displayType} fieldOptions={fieldOptions} errors={this.getFirstQueryError('fields')} fields={explodedFields} organization={organization} onChange={fields => {
                const fieldStrings = fields.map(field => (0, fields_1.generateFieldAsString)(field));
                queries.forEach((widgetQuery, queryIndex) => {
                    const newQuery = (0, cloneDeep_1.default)(widgetQuery);
                    newQuery.fields = fieldStrings;
                    onChange(queryIndex, newQuery);
                });
            }}/>
        {['table', 'top_n'].includes(displayType) && (<field_1.default label={(0, locale_1.t)('Sort by')} inline={false} flexibleControlStateSize stacked error={(_a = this.getFirstQueryError('orderby')) === null || _a === void 0 ? void 0 : _a.orderby} style={{ marginBottom: (0, space_1.default)(1) }}>
            <selectControl_1.default value={queries[0].orderby} name="orderby" options={generateOrderOptions(queries[0].fields)} onChange={(option) => this.handleFieldChange(0, 'orderby')(option.value)}/>
          </field_1.default>)}
      </QueryWrapper>);
    }
}
const QueryWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
exports.SearchConditionsWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;

  > * + * {
    margin-left: ${(0, space_1.default)(1)};
  }
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const LegendAliasInput = (0, styled_1.default)(input_1.default) `
  width: 33%;
`;
exports.default = WidgetQueriesForm;
//# sourceMappingURL=widgetQueriesForm.jsx.map