Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const utils_1 = require("../utils");
function Queries({ queries, selectedProjectIds, organization, displayType, onRemoveQuery, onAddQuery, onChangeQuery, errors, }) {
    function handleFieldChange(queryIndex, field) {
        const widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            const newQuery = Object.assign(Object.assign({}, widgetQuery), { [field]: value });
            onChangeQuery(queryIndex, newQuery);
        };
    }
    function canAddNewQuery() {
        const rightDisplayType = [
            utils_1.DisplayType.LINE,
            utils_1.DisplayType.AREA,
            utils_1.DisplayType.STACKED_AREA,
            utils_1.DisplayType.BAR,
        ].includes(displayType);
        const underQueryLimit = queries.length < 3;
        return rightDisplayType && underQueryLimit;
    }
    const hideLegendAlias = [
        utils_1.DisplayType.TABLE,
        utils_1.DisplayType.WORLD_MAP,
        utils_1.DisplayType.BIG_NUMBER,
    ].includes(displayType);
    return (<div>
      {queries.map((query, queryIndex) => {
            const displayDeleteButton = queries.length > 1;
            const displayLegendAlias = !hideLegendAlias;
            return (<StyledField key={queryIndex} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors[queryIndex].conditions}>
            <Fields displayDeleteButton={displayDeleteButton} displayLegendAlias={displayLegendAlias}>
              <searchBar_1.default organization={organization} projectIds={selectedProjectIds} query={query.conditions} fields={[]} onSearch={handleFieldChange(queryIndex, 'conditions')} onBlur={handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false}/>
              {displayLegendAlias && (<input_1.default type="text" name="name" required value={query.name} placeholder={(0, locale_1.t)('Legend Alias')} onChange={event => handleFieldChange(queryIndex, 'name')(event.target.value)}/>)}
              {displayDeleteButton && (<button_1.default size="zero" borderless onClick={event => {
                        event.preventDefault();
                        onRemoveQuery(queryIndex);
                    }} icon={<icons_1.IconDelete />} title={(0, locale_1.t)('Remove query')} label={(0, locale_1.t)('Remove query')}/>)}
            </Fields>
          </StyledField>);
        })}
      {canAddNewQuery() && (<button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={(event) => {
                event.preventDefault();
                onAddQuery();
            }}>
          {(0, locale_1.t)('Add Query')}
        </button_1.default>)}
    </div>);
}
exports.default = Queries;
const fieldsColumns = (p) => {
    if (!p.displayDeleteButton && !p.displayLegendAlias) {
        return '1fr';
    }
    if (!p.displayDeleteButton) {
        return '1fr 33%';
    }
    if (!p.displayLegendAlias) {
        return '1fr max-content';
    }
    return '1fr 33% max-content';
};
const Fields = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: ${fieldsColumns};
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const StyledField = (0, styled_1.default)(field_1.default) `
  padding-right: 0;
`;
//# sourceMappingURL=queries.jsx.map