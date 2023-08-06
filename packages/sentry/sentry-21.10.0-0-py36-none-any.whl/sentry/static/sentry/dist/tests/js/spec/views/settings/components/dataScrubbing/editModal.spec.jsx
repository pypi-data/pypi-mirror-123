Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const modal_1 = require("sentry-test/modal");
const modal_2 = require("app/actionCreators/modal");
const convertRelayPiiConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/convertRelayPiiConfig"));
const edit_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/modals/edit"));
const submitRules_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/submitRules"));
const types_1 = require("app/views/settings/components/dataScrubbing/types");
const utils_1 = require("app/views/settings/components/dataScrubbing/utils");
// @ts-expect-error
const relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
const stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
const organizationSlug = 'sentry';
const convertedRules = (0, convertRelayPiiConfig_1.default)(stringRelayPiiConfig);
const rules = convertedRules;
const rule = rules[2];
const successfullySaved = jest.fn();
const projectId = 'foo';
const endpoint = `/projects/${organizationSlug}/${projectId}/`;
// @ts-expect-error
const api = new MockApiClient();
jest.mock('app/views/settings/components/dataScrubbing/submitRules');
function renderComponent() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const modal = yield (0, modal_1.mountGlobalModal)();
        (0, modal_2.openModal)(modalProps => (<edit_1.default {...modalProps} projectId={projectId} savedRules={rules} api={api} endpoint={endpoint} orgSlug={organizationSlug} onSubmitSuccess={successfullySaved} rule={rule}/>));
        // @ts-expect-error
        yield tick();
        modal.update();
        return modal;
    });
}
describe('Edit Modal', () => {
    it('open Edit Rule Modal', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = yield renderComponent();
        expect(wrapper.find('Header').text()).toEqual('Edit an advanced data scrubbing rule');
        const fieldGroup = wrapper.find('FieldGroup');
        expect(fieldGroup).toHaveLength(2);
        // Method Field
        const methodGroup = fieldGroup.at(0).find('Field');
        const methodField = methodGroup.at(0);
        expect(methodField.find('FieldLabel').text()).toEqual('Method');
        const methodFieldHelp = 'What to do';
        expect(methodField.find('QuestionTooltip').prop('title')).toEqual(methodFieldHelp);
        expect(methodField.find('Tooltip').prop('title')).toEqual(methodFieldHelp);
        const methodFieldSelect = methodField.find('SelectField');
        expect(methodFieldSelect.exists()).toBe(true);
        const methodFieldSelectProps = methodFieldSelect.props();
        expect(methodFieldSelectProps.value).toEqual(types_1.MethodType.REPLACE);
        const methodFieldSelectOptions = (0, sortBy_1.default)(Object.values(types_1.MethodType)).map(value => (Object.assign(Object.assign({}, (0, utils_1.getMethodLabel)(value)), { value })));
        expect(methodFieldSelectProps.options).toEqual(methodFieldSelectOptions);
        // Placeholder Field
        const placeholderField = methodGroup.at(1);
        expect(placeholderField.find('FieldLabel').text()).toEqual('Custom Placeholder (Optional)');
        const placeholderFieldHelp = 'It will replace the default placeholder [Filtered]';
        expect(placeholderField.find('QuestionTooltip').prop('title')).toEqual(placeholderFieldHelp);
        expect(placeholderField.find('Tooltip').prop('title')).toEqual(placeholderFieldHelp);
        if (rule.method === types_1.MethodType.REPLACE) {
            const placeholderInput = placeholderField.find('input');
            expect(placeholderInput.prop('value')).toEqual(rule.placeholder);
        }
        // Type Field
        const typeGroup = fieldGroup.at(1).find('Field');
        const typeField = typeGroup.at(0);
        expect(typeField.find('FieldLabel').text()).toEqual('Data Type');
        const typeFieldHelp = 'What to look for. Use an existing pattern or define your own using regular expressions.';
        expect(typeField.find('QuestionTooltip').prop('title')).toEqual(typeFieldHelp);
        expect(typeField.find('Tooltip').prop('title')).toEqual(typeFieldHelp);
        const typeFieldSelect = typeField.find('SelectField');
        expect(typeFieldSelect.exists()).toBe(true);
        const typeFieldSelectProps = typeFieldSelect.props();
        expect(typeFieldSelectProps.value).toEqual(types_1.RuleType.PATTERN);
        const typeFieldSelectOptions = (0, sortBy_1.default)(Object.values(types_1.RuleType)).map(value => ({
            label: (0, utils_1.getRuleLabel)(value),
            value,
        }));
        expect(typeFieldSelectProps.options).toEqual(typeFieldSelectOptions);
        // Regex matches Field
        const regexField = typeGroup.at(1);
        expect(regexField.find('FieldLabel').text()).toEqual('Regex matches');
        const regexFieldHelp = 'Custom regular expression (see documentation)';
        expect(regexField.find('QuestionTooltip').prop('title')).toEqual(regexFieldHelp);
        expect(regexField.find('Tooltip').prop('title')).toEqual(regexFieldHelp);
        if (rule.type === types_1.RuleType.PATTERN) {
            const regexFieldInput = regexField.find('input');
            expect(regexFieldInput.prop('value')).toEqual(rule.pattern);
        }
        // Event ID
        expect(wrapper.find('Toggle').text()).toEqual('Use event ID for auto-completion');
        // Source Field
        const sourceGroup = wrapper.find('SourceGroup');
        expect(sourceGroup.exists()).toBe(true);
        expect(sourceGroup.find('EventIdField')).toHaveLength(0);
        const sourceField = sourceGroup.find('Field');
        expect(sourceField.find('FieldLabel').text()).toEqual('Source');
        const sourceFieldHelp = 'Where to look. In the simplest case this can be an attribute name.';
        expect(sourceField.find('QuestionTooltip').prop('title')).toEqual(sourceFieldHelp);
        expect(sourceField.find('Tooltip').prop('title')).toEqual(sourceFieldHelp);
        const sourceFieldInput = sourceField.find('input');
        expect(sourceFieldInput.prop('value')).toEqual(rule.source);
        // Close Modal
        const cancelButton = wrapper.find('[aria-label="Cancel"]').hostNodes();
        expect(cancelButton.exists()).toBe(true);
        cancelButton.simulate('click');
        // @ts-expect-error
        yield tick();
        wrapper.update();
        expect(wrapper.find('GlobalModal[visible=true]').exists()).toBe(false);
    }));
    it('edit Rule Modal', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = yield renderComponent();
        // Method Field
        const methodField = wrapper.find('[data-test-id="method-field"]');
        const methodFieldInput = methodField.find('input').at(0);
        methodFieldInput.simulate('keyDown', { key: 'ArrowDown' });
        const methodFieldMenuOptions = wrapper.find('[data-test-id="method-field"] MenuList Option Wrapper');
        const maskOption = methodFieldMenuOptions.at(1);
        maskOption.simulate('click');
        // Placeholder Field should be now hidden
        const placeholderField = wrapper.find('[data-test-id="placeholder-field"]');
        expect(placeholderField).toHaveLength(0);
        // Type Field
        const typeField = wrapper.find('[data-test-id="type-field"]');
        const typeFieldInput = typeField.find('input').at(0);
        typeFieldInput.simulate('keyDown', { key: 'ArrowDown' });
        const typeFieldMenuOptions = wrapper.find('[data-test-id="type-field"] MenuList Option Wrapper');
        const anythingOption = typeFieldMenuOptions.at(0);
        anythingOption.simulate('click');
        // Regex Field should be now hidden
        const regexField = wrapper.find('[data-test-id="regex-field"]');
        expect(regexField).toHaveLength(0);
        // Source Field
        const sourceField = wrapper.find('[data-test-id="source-field"]');
        const sourceFieldInput = sourceField.find('input');
        sourceFieldInput.simulate('change', { target: { value: utils_1.valueSuggestions[2].value } });
        // Save rule
        const saveButton = wrapper.find('[aria-label="Save Rule"]').hostNodes();
        expect(saveButton.exists()).toBe(true);
        saveButton.simulate('click');
        expect(submitRules_1.default).toHaveBeenCalled();
        expect(submitRules_1.default).toHaveBeenCalledWith(api, endpoint, [
            {
                id: 0,
                method: 'replace',
                type: 'password',
                source: 'password',
                placeholder: 'Scrubbed',
            },
            { id: 1, method: 'mask', type: 'creditcard', source: '$message' },
            {
                id: 2,
                method: 'mask',
                pattern: '',
                placeholder: '',
                type: 'anything',
                source: '$error.value',
            },
        ]);
    }));
});
//# sourceMappingURL=editModal.spec.jsx.map