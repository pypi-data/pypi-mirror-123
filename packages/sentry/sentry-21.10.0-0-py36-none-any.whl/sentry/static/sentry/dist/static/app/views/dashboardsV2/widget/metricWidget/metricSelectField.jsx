Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
function MetricSelectField({ metricMetas, metricMeta, aggregation, onChange }) {
    var _a, _b;
    const operations = (_a = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.operations) !== null && _a !== void 0 ? _a : [];
    return (<Wrapper>
      <StyledSelectField name="metric" options={metricMetas.map(metricMetaChoice => ({
            value: metricMetaChoice.name,
            label: metricMetaChoice.name,
        }))} placeholder={(0, locale_1.t)('Select metric')} onChange={value => {
            const newMetric = metricMetas.find(metricMetaChoice => metricMetaChoice.name === value);
            onChange('metricMeta', newMetric);
        }} value={(_b = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) !== null && _b !== void 0 ? _b : ''} components={{
            Option: (_a) => {
                var { label } = _a, optionProps = (0, tslib_1.__rest)(_a, ["label"]);
                const { selectProps } = optionProps;
                const { inputValue } = selectProps;
                return (<react_select_1.components.Option label={label} {...optionProps}>
                <highlight_1.default text={inputValue !== null && inputValue !== void 0 ? inputValue : ''}>{label}</highlight_1.default>
              </react_select_1.components.Option>);
            },
        }} styles={{
            control: provided => (Object.assign(Object.assign({}, provided), { borderTopRightRadius: 0, borderBottomRightRadius: 0, borderRight: 'none', boxShadow: 'none' })),
        }} inline={false} flexibleControlStateSize stacked allowClear/>
      <tooltip_1.default disabled={!!operations.length} title={(0, locale_1.t)('Please select a metric to enable this field')}>
        <selectControl_1.default name="aggregation" placeholder={(0, locale_1.t)('Aggr')} disabled={!operations.length} options={operations.map(operation => ({
            label: operation === 'count_unique' ? 'unique' : operation,
            value: operation,
        }))} value={aggregation !== null && aggregation !== void 0 ? aggregation : ''} onChange={({ value }) => onChange('aggregation', value)} styles={{
            control: provided => (Object.assign(Object.assign({}, provided), { borderTopLeftRadius: 0, borderBottomLeftRadius: 0, boxShadow: 'none' })),
        }}/>
      </tooltip_1.default>
    </Wrapper>);
}
exports.default = MetricSelectField;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  padding-right: 0;
  padding-bottom: 0;
`;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 0.5fr;
`;
//# sourceMappingURL=metricSelectField.jsx.map