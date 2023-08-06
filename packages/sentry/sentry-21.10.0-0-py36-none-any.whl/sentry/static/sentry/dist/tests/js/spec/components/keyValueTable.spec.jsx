Object.defineProperty(exports, "__esModule", { value: true });
const enzyme_1 = require("sentry-test/enzyme");
const keyValueTable_1 = require("app/components/keyValueTable");
describe('KeyValueTable', function () {
    it('basic', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<keyValueTable_1.KeyValueTable>
        <keyValueTable_1.KeyValueTableRow keyName="Coffee" value="Black hot drink"/>
        <keyValueTable_1.KeyValueTableRow keyName="Milk" value={<a href="#">White cold drink</a>}/>
      </keyValueTable_1.KeyValueTable>);
        expect(wrapper.find('dl').exists()).toBeTruthy();
        expect(wrapper.find('dt').at(0).text()).toBe('Coffee');
        expect(wrapper.find('dd').at(0).text()).toBe('Black hot drink');
        expect(wrapper.find('dt').at(1).text()).toBe('Milk');
        expect(wrapper.find('dd a').text()).toBe('White cold drink');
    });
});
//# sourceMappingURL=keyValueTable.spec.jsx.map