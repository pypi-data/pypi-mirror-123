Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const eventIdField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/modals/form/eventIdField"));
const types_1 = require("app/views/settings/components/dataScrubbing/types");
const handleUpdateEventId = jest.fn();
const eventIdValue = '887ab369df634e74aea708bcafe1a175';
function renderComponent({ value = eventIdValue, status, }) {
    return (0, enzyme_1.mountWithTheme)(<eventIdField_1.default onUpdateEventId={handleUpdateEventId} eventId={{ value, status }}/>);
}
describe('EventIdField', () => {
    it('default render', () => {
        const wrapper = renderComponent({ value: '', status: types_1.EventIdStatus.UNDEFINED });
        const eventIdField = wrapper.find('Field');
        expect(eventIdField.exists()).toBe(true);
        expect(eventIdField.find('FieldLabel').text()).toEqual('Event ID (Optional)');
        const eventIdFieldHelp = 'Providing an event ID will automatically provide you a list of suggested sources';
        expect(eventIdField.find('QuestionTooltip').prop('title')).toEqual(eventIdFieldHelp);
        expect(eventIdField.find('Tooltip').prop('title')).toEqual(eventIdFieldHelp);
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual('');
        expect(eventIdFieldInput.prop('placeholder')).toEqual('XXXXXXXXXXXXXX');
        eventIdFieldInput.simulate('change', {
            target: { value: '887ab369df634e74aea708bcafe1a175' },
        });
        eventIdFieldInput.simulate('blur');
        expect(handleUpdateEventId).toHaveBeenCalled();
    });
    it('LOADING status', () => {
        const wrapper = renderComponent({ status: types_1.EventIdStatus.LOADING });
        const eventIdField = wrapper.find('Field');
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        expect(eventIdField.find('FormSpinner')).toHaveLength(1);
    });
    it('LOADED status', () => {
        const wrapper = renderComponent({ status: types_1.EventIdStatus.LOADED });
        const eventIdField = wrapper.find('Field');
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        const iconCheckmark = eventIdField.find('IconCheckmark');
        expect(iconCheckmark).toHaveLength(1);
        const iconCheckmarkColor = iconCheckmark.prop('color');
        expect(theme_1.default[iconCheckmarkColor]).toBe(theme_1.default.green300);
    });
    it('ERROR status', () => {
        const wrapper = renderComponent({ status: types_1.EventIdStatus.ERROR });
        const eventIdField = wrapper.find('Field');
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        const closeIcon = eventIdField.find('CloseIcon');
        expect(closeIcon).toHaveLength(1);
        expect(closeIcon.find('Tooltip').prop('title')).toEqual('Clear event ID');
        const fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('An error occurred while fetching the suggestions based on this event ID.');
    });
    it('INVALID status', () => {
        const wrapper = renderComponent({ status: types_1.EventIdStatus.INVALID });
        const eventIdField = wrapper.find('Field');
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        const fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('This event ID is invalid.');
    });
    it('NOTFOUND status', () => {
        const wrapper = renderComponent({ status: types_1.EventIdStatus.NOT_FOUND });
        const eventIdField = wrapper.find('Field');
        const eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        const fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('The chosen event ID was not found in projects you have access to.');
    });
});
//# sourceMappingURL=eventIdField.spec.jsx.map