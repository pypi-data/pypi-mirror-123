Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const optionCheckboxSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionCheckboxSelector"));
const locale_1 = require("app/locale");
describe('EventsV2 > OptionCheckboxSelector', function () {
    const features = ['discover-basic'];
    const yAxisValue = ['count()', 'failure_count()'];
    const yAxisOptions = [
        { label: 'count()', value: 'count()' },
        { label: 'failure_count()', value: 'failure_count()' },
        { label: 'count_unique(user)', value: 'count_unique(user)' },
        { label: 'avg(transaction.duration)', value: 'avg(transaction.duration)' },
    ];
    let organization, initialData, selected, wrapper, onChangeStub, dropdownItem;
    beforeEach(() => {
        // @ts-expect-error
        organization = TestStubs.Organization({
            features: [...features, 'connect-discover-and-dashboards'],
        });
        // Start off with an invalid view (empty is invalid)
        initialData = (0, initializeOrg_1.initializeOrg)({
            organization,
            router: {
                location: { query: { query: 'tag:value' } },
            },
            project: 1,
            projects: [],
        });
        selected = [...yAxisValue];
        wrapper = (0, enzyme_1.mountWithTheme)(<optionCheckboxSelector_1.default title={(0, locale_1.t)('Y-Axis')} selected={selected} options={yAxisOptions} onChange={() => undefined}/>, initialData.routerContext);
        // Parent component usually handles the new selected state but we don't have one in this test so we update props ourselves
        onChangeStub = jest.fn(newSelected => wrapper.setProps({ selected: newSelected }));
        wrapper.setProps({ onChange: onChangeStub });
        dropdownItem = wrapper.find('StyledDropdownItem');
    });
    it('renders yAxisOptions with yAxisValue selected', function () {
        expect(dropdownItem.at(0).find('span').last().children().html()).toEqual('count()');
        expect(dropdownItem.at(1).find('span').last().children().html()).toEqual('failure_count()');
        expect(dropdownItem.at(2).find('span').last().children().html()).toEqual('count_unique(user)');
        expect(dropdownItem.at(0).props().isChecked).toEqual(true);
        expect(dropdownItem.at(1).props().isChecked).toEqual(true);
        expect(dropdownItem.at(2).props().isChecked).toEqual(false);
    });
    it('calls onChange prop with new checkbox option state', function () {
        dropdownItem.at(0).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['failure_count()']);
        dropdownItem.at(0).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['failure_count()', 'count()']);
        dropdownItem.at(1).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['count()']);
        dropdownItem.at(1).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['count()', 'failure_count()']);
        dropdownItem.at(2).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith([
            'count()',
            'failure_count()',
            'count_unique(user)',
        ]);
    });
    it('does not uncheck options when clicked if only one option is currently selected', function () {
        dropdownItem.at(0).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['failure_count()']);
        dropdownItem.at(1).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['failure_count()']);
    });
    it('only allows up to 3 options to be checked at one time', function () {
        dropdownItem.at(2).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith([
            'count()',
            'failure_count()',
            'count_unique(user)',
        ]);
        dropdownItem.at(3).find('div').first().simulate('click');
        expect(onChangeStub).not.toHaveBeenCalledWith([
            'count()',
            'failure_count()',
            'count_unique(user)',
            'avg(transaction.duration)',
        ]);
        dropdownItem.at(2).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['count()', 'failure_count()']);
        dropdownItem.at(3).find('div').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith([
            'count()',
            'failure_count()',
            'avg(transaction.duration)',
        ]);
    });
    it('calls onChange prop with a single selected value when clicking on the row instead of the checkbox', function () {
        dropdownItem.at(0).find('span').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['count()']);
        dropdownItem.at(1).find('span').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['failure_count()']);
        dropdownItem.at(2).find('span').first().simulate('click');
        expect(onChangeStub).toHaveBeenCalledWith(['count_unique(user)']);
    });
});
//# sourceMappingURL=optionCheckboxSelector.spec.jsx.map