Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const createListeners_1 = require("sentry-test/createListeners");
const enzyme_1 = require("sentry-test/enzyme");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const editableText_1 = (0, tslib_1.__importDefault)(require("app/components/editableText"));
const currentValue = 'foo';
function renderedComponent(onChange, newValue = 'bar') {
    const wrapper = (0, enzyme_1.mountWithTheme)(<editableText_1.default value={currentValue} onChange={onChange}/>);
    let label = wrapper.find('Label');
    expect(label.text()).toEqual(currentValue);
    let inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper.length).toEqual(0);
    const styledIconEdit = wrapper.find('IconEdit');
    expect(styledIconEdit.length).toEqual(1);
    label.simulate('click');
    label = wrapper.find('Label');
    expect(inputWrapper.length).toEqual(0);
    inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper.length).toEqual(1);
    const styledInput = wrapper.find('StyledInput');
    expect(styledInput.length).toEqual(1);
    styledInput.simulate('change', { target: { value: newValue } });
    const inputLabel = wrapper.find('InputLabel');
    expect(inputLabel.text()).toEqual(newValue);
    return wrapper;
}
describe('EditableText', function () {
    const newValue = 'bar';
    it('edit value and click outside of the component', function () {
        const fireEvent = (0, createListeners_1.createListeners)('document');
        const handleChange = jest.fn();
        const wrapper = renderedComponent(handleChange);
        (0, reactTestingLibrary_1.act)(() => {
            // Click outside of the component
            fireEvent.mouseDown(document.body);
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        const updatedLabel = wrapper.find('Label');
        expect(updatedLabel.length).toEqual(1);
        expect(updatedLabel.text()).toEqual(newValue);
    });
    it('edit value and press enter', function () {
        const fireEvent = (0, createListeners_1.createListeners)('window');
        const handleChange = jest.fn();
        const wrapper = renderedComponent(handleChange);
        (0, reactTestingLibrary_1.act)(() => {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        const updatedLabel = wrapper.find('Label');
        expect(updatedLabel.length).toEqual(1);
        expect(updatedLabel.text()).toEqual(newValue);
    });
    it('clear value and show error message', function () {
        const fireEvent = (0, createListeners_1.createListeners)('window');
        const handleChange = jest.fn();
        const wrapper = renderedComponent(handleChange, '');
        (0, reactTestingLibrary_1.act)(() => {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalledTimes(0);
        wrapper.update();
    });
    it('displays a disabled value', function () {
        const handleChange = jest.fn();
        const wrapper = (0, enzyme_1.mountWithTheme)(<editableText_1.default value={currentValue} onChange={handleChange} isDisabled/>);
        let label = wrapper.find('Label');
        expect(label.text()).toEqual(currentValue);
        label.simulate('click');
        const inputWrapper = wrapper.find('InputWrapper');
        expect(inputWrapper.length).toEqual(0);
        label = wrapper.find('Label');
        expect(label.length).toEqual(1);
    });
    describe('revert value and close editor', function () {
        it('prop value changes', function () {
            const handleChange = jest.fn();
            const newPropValue = 'new-prop-value';
            const wrapper = renderedComponent(handleChange, '');
            wrapper.setProps({ value: newPropValue });
            wrapper.update();
            const updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(newPropValue);
        });
        it('prop isDisabled changes', function () {
            const handleChange = jest.fn();
            const wrapper = renderedComponent(handleChange, '');
            wrapper.setProps({ isDisabled: true });
            wrapper.update();
            const updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(currentValue);
        });
        it('edit value and press escape', function () {
            const fireEvent = (0, createListeners_1.createListeners)('window');
            const handleChange = jest.fn();
            const wrapper = renderedComponent(handleChange);
            (0, reactTestingLibrary_1.act)(() => {
                // Press escape
                fireEvent.keyDown('Escape');
            });
            expect(handleChange).toHaveBeenCalledTimes(0);
            wrapper.update();
            const updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(currentValue);
        });
    });
});
//# sourceMappingURL=editableText.spec.jsx.map