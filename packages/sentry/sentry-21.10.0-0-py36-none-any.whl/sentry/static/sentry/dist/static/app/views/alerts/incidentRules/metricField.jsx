Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const options_1 = require("app/views/alerts/wizard/options");
const queryField_1 = require("app/views/eventsV2/table/queryField");
const types_1 = require("app/views/eventsV2/table/types");
const utils_1 = require("app/views/eventsV2/utils");
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const constants_1 = require("./constants");
const presets_1 = require("./presets");
const types_2 = require("./types");
const getFieldOptionConfig = ({ dataset, alertType, }) => {
    let config;
    let hidePrimarySelector = false;
    let hideParameterSelector = false;
    if (alertType) {
        config = (0, constants_1.getWizardAlertFieldConfig)(alertType, dataset);
        hidePrimarySelector = options_1.hidePrimarySelectorSet.has(alertType);
        hideParameterSelector = options_1.hideParameterSelectorSet.has(alertType);
    }
    else {
        config = dataset === types_2.Dataset.ERRORS ? constants_1.errorFieldConfig : constants_1.transactionFieldConfig;
    }
    const aggregations = Object.fromEntries(config.aggregations.map(key => {
        // TODO(scttcper): Temporary hack for default value while we handle the translation of user
        if (key === 'count_unique') {
            const agg = fields_1.AGGREGATIONS[key];
            agg.getFieldOverrides = () => {
                return { defaultValue: 'tags[sentry:user]' };
            };
            return [key, agg];
        }
        return [key, fields_1.AGGREGATIONS[key]];
    }));
    const fields = Object.fromEntries(config.fields.map(key => {
        // XXX(epurkhiser): Temporary hack while we handle the translation of user ->
        // tags[sentry:user].
        if (key === 'user') {
            return ['tags[sentry:user]', 'string'];
        }
        return [key, fields_1.FIELDS[key]];
    }));
    const { measurementKeys } = config;
    return {
        fieldOptionsConfig: { aggregations, fields, measurementKeys },
        hidePrimarySelector,
        hideParameterSelector,
    };
};
const help = ({ name, model }) => {
    const aggregate = model.getValue(name);
    const presets = presets_1.PRESET_AGGREGATES.filter(preset => preset.validDataset.includes(model.getValue('dataset')))
        .map(preset => (Object.assign(Object.assign({}, preset), { selected: preset.match.test(aggregate) })))
        .map((preset, i, list) => (<react_1.Fragment key={preset.name}>
        <tooltip_1.default title={(0, locale_1.t)('This preset is selected')} disabled={!preset.selected}>
          <PresetButton type="button" onClick={() => model.setValue(name, preset.default)} disabled={preset.selected}>
            {preset.name}
          </PresetButton>
        </tooltip_1.default>
        {i + 1 < list.length && ', '}
      </react_1.Fragment>));
    return (0, locale_1.tct)('Choose an aggregate function. Not sure what to select, try a preset: [presets]', { presets });
};
const MetricField = (_a) => {
    var { organization, columnWidth, inFieldLabels, alertType } = _a, props = (0, tslib_1.__rest)(_a, ["organization", "columnWidth", "inFieldLabels", "alertType"]);
    return (<formField_1.default help={help} {...props}>
    {({ onChange, value, model, disabled }) => {
            var _a;
            const dataset = model.getValue('dataset');
            const { fieldOptionsConfig, hidePrimarySelector, hideParameterSelector } = getFieldOptionConfig({
                dataset: dataset,
                alertType,
            });
            const fieldOptions = (0, utils_1.generateFieldOptions)(Object.assign({ organization }, fieldOptionsConfig));
            const fieldValue = (0, fields_1.explodeFieldString)(value !== null && value !== void 0 ? value : '');
            const fieldKey = (fieldValue === null || fieldValue === void 0 ? void 0 : fieldValue.kind) === types_1.FieldValueKind.FUNCTION
                ? `function:${fieldValue.function[0]}`
                : '';
            const selectedField = (_a = fieldOptions[fieldKey]) === null || _a === void 0 ? void 0 : _a.value;
            const numParameters = (selectedField === null || selectedField === void 0 ? void 0 : selectedField.kind) === types_1.FieldValueKind.FUNCTION
                ? selectedField.meta.parameters.length
                : 0;
            const parameterColumns = numParameters - (hideParameterSelector ? 1 : 0) - (hidePrimarySelector ? 1 : 0);
            return (<react_1.Fragment>
          <StyledQueryField filterPrimaryOptions={option => option.value.kind === types_1.FieldValueKind.FUNCTION} fieldOptions={fieldOptions} fieldValue={fieldValue} onChange={v => onChange((0, fields_1.generateFieldAsString)(v), {})} columnWidth={columnWidth} gridColumns={parameterColumns + 1} inFieldLabels={inFieldLabels} shouldRenderTag={false} disabled={disabled} hideParameterSelector={hideParameterSelector} hidePrimarySelector={hidePrimarySelector}/>
        </react_1.Fragment>);
        }}
  </formField_1.default>);
};
const StyledQueryField = (0, styled_1.default)(queryField_1.QueryField) `
  ${p => p.columnWidth &&
    (0, react_2.css) `
      width: ${p.gridColumns * p.columnWidth}px;
    `}
`;
const PresetButton = (0, styled_1.default)(button_1.default) `
  ${p => p.disabled &&
    (0, react_2.css) `
      color: ${p.theme.textColor};
      &:hover,
      &:focus {
        color: ${p.theme.textColor};
      }
    `}
`;
PresetButton.defaultProps = {
    priority: 'link',
    borderless: true,
};
exports.default = MetricField;
//# sourceMappingURL=metricField.jsx.map