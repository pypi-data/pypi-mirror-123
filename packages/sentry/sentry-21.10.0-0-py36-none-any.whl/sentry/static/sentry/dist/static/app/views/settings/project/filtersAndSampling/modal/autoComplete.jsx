Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const tags_1 = require("app/actionCreators/tags");
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const utils_1 = require("./utils");
function AutoComplete({ orgSlug, projectId, category, onChange, value }) {
    const api = (0, useApi_1.default)();
    const [tagValues, setTagValues] = (0, react_1.useState)([]);
    (0, react_1.useEffect)(() => {
        tagValueLoader();
    }, []);
    function getTagKey() {
        switch (category) {
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
                return 'release';
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
                return 'environment';
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION:
                return 'transaction';
            default:
                Sentry.captureException(new Error('Unknown dynamic sampling condition inner name'));
                return ''; // this shall never happen
        }
    }
    function getAriaLabel() {
        switch (category) {
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
                return (0, locale_1.t)('Search or add a release');
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
                return (0, locale_1.t)('Search or add an environment');
            case dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION:
            case dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION:
                return (0, locale_1.t)('Search or add a transaction');
            default:
                Sentry.captureException(new Error('Unknown dynamic sampling condition inner name'));
                return ''; // this shall never happen
        }
    }
    const key = getTagKey();
    function tagValueLoader() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!key) {
                return;
            }
            try {
                const response = yield (0, tags_1.fetchTagValues)(api, orgSlug, key, null, [projectId]);
                setTagValues(response);
            }
            catch (_a) {
                // Do nothing. No results will be suggested
            }
        });
    }
    // react-select doesn't seem to work very well when its value contains
    // a created item that isn't listed in the options
    const createdOptions = !value
        ? []
        : value
            .split(',')
            .filter(v => !tagValues.some(tagValue => tagValue.value === v))
            .map(v => ({ value: v }));
    return (<StyledSelectField name="match" aria-label={getAriaLabel()} options={[...createdOptions, ...tagValues].map(tagValue => ({
            value: tagValue.value,
            label: tagValue.value,
        }))} value={value === null || value === void 0 ? void 0 : value.split(',')} onChange={newValue => {
            onChange(newValue === null || newValue === void 0 ? void 0 : newValue.join(','));
        }} styles={{
            menu: provided => (Object.assign(Object.assign({}, provided), { wordBreak: 'break-all' })),
        }} components={{
            SelectContainer: (containerProps) => (<react_select_1.components.SelectContainer {...containerProps} innerProps={Object.assign(Object.assign({}, containerProps.innerProps), { 'data-test-id': `autocomplete-${key}` })}/>),
            MultiValue: (multiValueProps) => (<react_select_1.components.MultiValue {...multiValueProps} innerProps={Object.assign(Object.assign({}, multiValueProps.innerProps), { 'data-test-id': 'multivalue' })}/>),
            Option: (optionProps) => (<react_select_1.components.Option {...optionProps} innerProps={Object.assign(Object.assign({}, optionProps.innerProps), { 'data-test-id': 'option' })}/>),
        }} formatCreateLabel={label => (0, locale_1.tct)('Add "[newLabel]"', { newLabel: label })} placeholder={(0, utils_1.getMatchFieldPlaceholder)(category)} inline={false} multiple hideControlState flexibleControlStateSize required stacked creatable allowClear/>);
}
exports.default = AutoComplete;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  width: 100%;
`;
//# sourceMappingURL=autoComplete.jsx.map