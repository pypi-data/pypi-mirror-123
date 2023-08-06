Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const enzyme_1 = require("sentry-test/enzyme");
const modal_1 = require("app/actionCreators/modal");
const globalModal_1 = (0, tslib_1.__importDefault)(require("app/components/globalModal"));
const convertRelayPiiConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/convertRelayPiiConfig"));
const add_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/modals/add"));
const types_1 = require("app/views/settings/components/dataScrubbing/types");
const utils_1 = require("app/views/settings/components/dataScrubbing/utils");
// @ts-expect-error
const relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
const stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
const organizationSlug = 'sentry';
const convertedRules = (0, convertRelayPiiConfig_1.default)(stringRelayPiiConfig);
const rules = convertedRules;
const successfullySaved = jest.fn();
const projectId = 'foo';
const endpoint = `/projects/${organizationSlug}/${projectId}/`;
// @ts-expect-error
const api = new MockApiClient();
function renderComponent() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<globalModal_1.default />);
        (0, modal_1.openModal)(modalProps => (<add_1.default {...modalProps} projectId={projectId} savedRules={rules} api={api} endpoint={endpoint} orgSlug={organizationSlug} onSubmitSuccess={successfullySaved}/>));
        // @ts-expect-error
        yield tick();
        wrapper.update();
        return wrapper;
    });
}
describe('Add Modal', () => {
    it('open Add Rule Modal', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = yield renderComponent();
        expect(wrapper.find('Header').text()).toEqual('Add an advanced data scrubbing rule');
        const fieldGroup = wrapper.find('FieldGroup');
        expect(fieldGroup).toHaveLength(2);
        // Method Field
        const methodGroup = fieldGroup.at(0).find('Field');
        expect(methodGroup.find('FieldLabel').text()).toEqual('Method');
        const methodFieldHelp = 'What to do';
        expect(methodGroup.find('QuestionTooltip').prop('title')).toEqual(methodFieldHelp);
        expect(methodGroup.find('Tooltip').prop('title')).toEqual(methodFieldHelp);
        const methodField = methodGroup.find('SelectField');
        expect(methodField.exists()).toBe(true);
        const methodFieldProps = methodField.props();
        expect(methodFieldProps.value).toEqual(types_1.MethodType.MASK);
        const methodFieldOptions = (0, sortBy_1.default)(Object.values(types_1.MethodType)).map(value => (Object.assign(Object.assign({}, (0, utils_1.getMethodLabel)(value)), { value })));
        expect(methodFieldProps.options).toEqual(methodFieldOptions);
        // Type Field
        const typeGroup = fieldGroup.at(1).find('Field');
        expect(typeGroup.find('FieldLabel').text()).toEqual('Data Type');
        const typeFieldHelp = 'What to look for. Use an existing pattern or define your own using regular expressions.';
        expect(typeGroup.find('QuestionTooltip').prop('title')).toEqual(typeFieldHelp);
        expect(typeGroup.find('Tooltip').prop('title')).toEqual(typeFieldHelp);
        const typeField = typeGroup.find('SelectField');
        expect(typeField.exists()).toBe(true);
        const typeFieldProps = typeField.props();
        expect(typeFieldProps.value).toEqual(types_1.RuleType.CREDITCARD);
        const typeFieldOptions = (0, sortBy_1.default)(Object.values(types_1.RuleType)).map(value => ({
            label: (0, utils_1.getRuleLabel)(value),
            value,
        }));
        expect(typeFieldProps.options).toEqual(typeFieldOptions);
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
        // Close Modal
        const cancelButton = wrapper.find('[aria-label="Cancel"]').hostNodes();
        expect(cancelButton.exists()).toBe(true);
        cancelButton.simulate('click');
        // @ts-expect-error
        yield tick();
        wrapper.update();
        expect(wrapper.find('GlobalModal[visible=true]').exists()).toBe(false);
    }));
    it('Display placeholder field', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = yield renderComponent();
        const fieldGroup = wrapper.find('FieldGroup');
        expect(fieldGroup).toHaveLength(2);
        // Method Field
        const methodGroup = fieldGroup.at(0).find('Field');
        expect(methodGroup).toHaveLength(1);
        const methodField = methodGroup.find('[data-test-id="method-field"]');
        const methodFieldInput = methodField.find('input').at(1);
        methodFieldInput.simulate('keyDown', { key: 'ArrowDown' });
        const methodFieldMenuOptions = wrapper.find('[data-test-id="method-field"] MenuList Option Wrapper');
        expect(methodFieldMenuOptions).toHaveLength(4);
        const replaceOption = methodFieldMenuOptions.at(3);
        expect(replaceOption.find('[data-test-id="label"]').text()).toEqual('Replace');
        expect(replaceOption.find('Description').text()).toEqual('(Replace with Placeholder)');
        // After the click the placeholder field MUST be in the DOM
        replaceOption.simulate('click');
        wrapper.update();
        expect(wrapper.find('[data-test-id="method-field"] input').at(1).prop('value')).toEqual(types_1.MethodType.REPLACE);
        const updatedMethodGroup = wrapper.find('FieldGroup').at(0).find('Field');
        expect(updatedMethodGroup).toHaveLength(2);
        const placeholderField = updatedMethodGroup.at(1);
        expect(placeholderField.find('FieldLabel').text()).toEqual('Custom Placeholder (Optional)');
        const placeholderFieldHelp = 'It will replace the default placeholder [Filtered]';
        expect(placeholderField.find('QuestionTooltip').prop('title')).toEqual(placeholderFieldHelp);
        expect(placeholderField.find('Tooltip').prop('title')).toEqual(placeholderFieldHelp);
        // After the click, the placeholder field MUST NOT be in the DOM
        wrapper
            .find('[data-test-id="method-field"]')
            .find('input')
            .at(1)
            .simulate('keyDown', { key: 'ArrowDown' });
        const hashOption = wrapper
            .find('[data-test-id="method-field"] MenuList Option Wrapper')
            .at(0);
        hashOption.simulate('click');
        expect(wrapper.find('[data-test-id="method-field"] input').at(1).prop('value')).toBe(types_1.MethodType.HASH);
        expect(wrapper.find('FieldGroup').at(0).find('Field')).toHaveLength(1);
    }));
    it('Display regex field', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = yield renderComponent();
        const fieldGroup = wrapper.find('FieldGroup');
        expect(fieldGroup).toHaveLength(2);
        // Type Field
        const typeGroup = fieldGroup.at(1).find('Field');
        expect(typeGroup).toHaveLength(1);
        const typeField = typeGroup.find('[data-test-id="type-field"]');
        const typeFieldInput = typeField.find('input').at(1);
        typeFieldInput.simulate('keyDown', { key: 'ArrowDown' });
        const typeFieldMenuOptions = wrapper.find('[data-test-id="type-field"] MenuList Option Wrapper');
        expect(typeFieldMenuOptions).toHaveLength(13);
        const regexOption = typeFieldMenuOptions.at(7);
        expect(regexOption.find('[data-test-id="label"]').text()).toEqual('Regex matches');
        // After the click, the regex matches field MUST be in the DOM
        regexOption.simulate('click');
        wrapper.update();
        expect(wrapper.find('[data-test-id="type-field"] input').at(1).prop('value')).toEqual(types_1.RuleType.PATTERN);
        const updatedTypeGroup = wrapper.find('FieldGroup').at(1).find('Field');
        expect(updatedTypeGroup).toHaveLength(2);
        const regexField = updatedTypeGroup.at(1);
        expect(regexField.find('FieldLabel').text()).toEqual('Regex matches');
        const regexFieldHelp = 'Custom regular expression (see documentation)';
        expect(regexField.find('QuestionTooltip').prop('title')).toEqual(regexFieldHelp);
        expect(regexField.find('Tooltip').prop('title')).toEqual(regexFieldHelp);
        // After the click, the regex matches field MUST NOT be in the DOM
        wrapper
            .find('[data-test-id="type-field"]')
            .find('input')
            .at(1)
            .simulate('keyDown', { key: 'ArrowDown' });
        const creditCardOption = wrapper
            .find('[data-test-id="type-field"] MenuList Option Wrapper')
            .at(1);
        creditCardOption.simulate('click');
        expect(wrapper.find('[data-test-id="type-field"] input').at(1).prop('value')).toBe(types_1.RuleType.CREDITCARD);
        expect(wrapper.find('FieldGroup').at(1).find('Field')).toHaveLength(1);
    }));
    it('Display Event Id', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const eventId = '12345678901234567890123456789012';
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: `/organizations/${organizationSlug}/data-scrubbing-selector-suggestions/`,
            body: {
                suggestions: [
                    { type: 'value', examples: ['34359738368'], value: "extra.'system.cpu.memory'" },
                    { type: 'value', value: '$frame.abs_path' },
                ],
            },
        });
        const wrapper = yield renderComponent();
        const eventIdToggle = wrapper.find('Toggle');
        eventIdToggle.simulate('click');
        const eventIdFieldInput = wrapper.find('[data-test-id="event-id-field"] input');
        eventIdFieldInput.simulate('change', {
            target: { value: eventId },
        });
        eventIdFieldInput.simulate('blur');
        // @ts-expect-error
        yield tick();
        // Loading
        expect(wrapper.find('[data-test-id="event-id-field"] FormSpinner')).toHaveLength(1);
        wrapper.update();
        // Fetched new suggestions successfully through the informed event ID
        expect(wrapper.find('[data-test-id="event-id-field"] IconCheckmark')).toHaveLength(1);
    }));
});
//# sourceMappingURL=addModal.spec.jsx.map