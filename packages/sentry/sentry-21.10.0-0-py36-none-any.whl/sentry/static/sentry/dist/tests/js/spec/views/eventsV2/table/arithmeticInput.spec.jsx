Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const fields_1 = require("app/utils/discover/fields");
const arithmeticInput_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/table/arithmeticInput"));
describe('ArithmeticInput', function () {
    let wrapper;
    let query;
    let handleQueryChange;
    let numericColumns;
    let columns;
    const operators = ['+', '-', '*', '/', '(', ')'];
    beforeEach(function () {
        query = '';
        handleQueryChange = q => {
            query = q;
        };
        numericColumns = [
            { kind: 'field', field: 'transaction.duration' },
            { kind: 'field', field: 'measurements.lcp' },
            { kind: 'field', field: 'spans.http' },
            { kind: 'function', function: ['p50', '', undefined, undefined] },
            {
                kind: 'function',
                function: ['percentile', 'transaction.duration', '0.25', undefined],
            },
            { kind: 'function', function: ['count', '', undefined, undefined] },
        ];
        columns = [
            ...numericColumns,
            // these columns will not be rendered in the dropdown
            { kind: 'function', function: ['any', 'transaction.duration', undefined, undefined] },
            { kind: 'field', field: 'transaction' },
            { kind: 'function', function: ['failure_rate', '', undefined, undefined] },
            { kind: 'equation', field: 'transaction.duration+measurements.lcp' },
        ];
        wrapper = (0, enzyme_1.mountWithTheme)(<arithmeticInput_1.default name="refinement" key="parameter:text" type="text" required value={query} onUpdate={handleQueryChange} options={columns}/>);
    });
    afterEach(function () {
        wrapper === null || wrapper === void 0 ? void 0 : wrapper.unmount();
    });
    it('can toggle autocomplete dropdown on focus and blur', function () {
        expect(wrapper.find('TermDropdown').props().isOpen).toBeFalsy();
        // focus the input
        wrapper.find('input').simulate('focus');
        expect(wrapper.find('TermDropdown').props().isOpen).toBeTruthy();
        // blur the input
        wrapper.find('input').simulate('blur');
        expect(wrapper.find('TermDropdown').props().isOpen).toBeFalsy();
    });
    it('renders only numeric options in autocomplete', function () {
        wrapper.find('input').simulate('focus');
        const options = wrapper.find('DropdownListItem');
        expect(options).toHaveLength(numericColumns.length + operators.length);
        options.forEach((option, i) => {
            if (i < numericColumns.length) {
                expect(option.text()).toEqual((0, fields_1.generateFieldAsString)(numericColumns[i]));
            }
            else {
                expect(option.text()).toEqual(operators[i - numericColumns.length]);
            }
        });
    });
    it('can use keyboard to select an option', function () {
        const input = wrapper.find('input');
        input.simulate('focus');
        expect(wrapper.find('DropdownListItem .active').exists()).toBeFalsy();
        for (const column of numericColumns) {
            input.simulate('keydown', { key: 'ArrowDown' });
            expect(wrapper.find('DropdownListItem .active').text()).toEqual((0, fields_1.generateFieldAsString)(column));
        }
        for (const operator of operators) {
            input.simulate('keydown', { key: 'ArrowDown' });
            expect(wrapper.find('DropdownListItem .active').text()).toEqual(operator);
        }
        // wrap around to the first option again
        input.simulate('keydown', { key: 'ArrowDown' });
        for (const operator of [...operators].reverse()) {
            input.simulate('keydown', { key: 'ArrowUp' });
            expect(wrapper.find('DropdownListItem .active').text()).toEqual(operator);
        }
        for (const column of [...numericColumns].reverse()) {
            input.simulate('keydown', { key: 'ArrowUp' });
            expect(wrapper.find('DropdownListItem .active').text()).toEqual((0, fields_1.generateFieldAsString)(column));
        }
        // the update is buffered until blur happens
        input.simulate('keydown', { key: 'Enter' });
        expect(query).toEqual('');
        input.simulate('blur');
        expect(query).toEqual(`${(0, fields_1.generateFieldAsString)(numericColumns[0])} `);
    });
    it('can use mouse to select an option', function () {
        const input = wrapper.find('input');
        input.simulate('focus');
        // the update is buffered until blur happens
        wrapper.find('DropdownListItem').first().simulate('click');
        input.simulate('blur');
        expect(query).toEqual(`${(0, fields_1.generateFieldAsString)(numericColumns[0])} `);
    });
    it('autocompletes the current term when it is in the front', function () {
        const input = wrapper.find('input');
        input.simulate('focus');
        const value = 'lcp + transaction.duration';
        input.simulate('change', { target: { value } });
        const inputElem = input.getDOMNode();
        inputElem.selectionStart = 2;
        inputElem.selectionEnd = 2;
        input.simulate('change');
        const option = wrapper.find('DropdownListItem');
        expect(option).toHaveLength(1);
        expect(option.text()).toEqual((0, fields_1.generateFieldAsString)({
            kind: 'field',
            field: 'measurements.lcp',
        }));
        option.simulate('click');
        input.simulate('blur');
        expect(query).toEqual(`measurements.lcp  + transaction.duration`);
    });
    it('autocompletes the current term when it is in the end', function () {
        const input = wrapper.find('input');
        input.simulate('focus');
        const value = 'transaction.duration + lcp';
        input.simulate('change', { target: { value } });
        const inputElem = input.getDOMNode();
        inputElem.selectionStart = value.length - 1;
        inputElem.selectionEnd = value.length - 1;
        input.simulate('change');
        const option = wrapper.find('DropdownListItem');
        expect(option).toHaveLength(1);
        const column = numericColumns.find(c => c.kind === 'field' && c.field.includes('lcp'));
        expect(option.text()).toEqual((0, fields_1.generateFieldAsString)(column));
        option.simulate('click');
        input.simulate('blur');
        expect(query).toEqual(`transaction.duration + measurements.lcp `);
    });
    it('handles autocomplete on invalid term', function () {
        const input = wrapper.find('input');
        input.simulate('focus');
        const value = 'foo + bar';
        input.simulate('change', { target: { value } });
        input.simulate('keydown', { key: 'ArrowDown' });
        const option = wrapper.find('DropdownListItem');
        expect(option).toHaveLength(0);
    });
});
//# sourceMappingURL=arithmeticInput.spec.jsx.map