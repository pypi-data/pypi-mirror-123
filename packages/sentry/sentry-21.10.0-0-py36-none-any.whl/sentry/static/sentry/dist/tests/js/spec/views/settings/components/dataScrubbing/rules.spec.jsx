Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const convertRelayPiiConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/convertRelayPiiConfig"));
const rules_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/rules"));
// @ts-expect-error
const relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
const stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
const convertedRules = (0, convertRelayPiiConfig_1.default)(stringRelayPiiConfig);
const rules = convertedRules;
const handleShowEditRule = jest.fn();
const handleDelete = jest.fn();
describe('Rules', () => {
    it('default render', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules}/>);
        expect(wrapper.find('ListItem')).toHaveLength(3);
    });
    it('render correct description', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules}/>);
        const listItems = wrapper.find('ListItem');
        expect(listItems.at(1).text()).toEqual('[Mask] [Credit card numbers] from [$message]');
        expect(listItems.at(0).text()).toEqual('[Replace] [Password fields]  with [Scrubbed] from [password]');
    });
    it('render disabled list', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules} disabled/>);
        expect(wrapper.find('List').prop('isDisabled')).toEqual(true);
    });
    it('render edit and delete buttons', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules} onEditRule={handleShowEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes()).toHaveLength(3);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes()).toHaveLength(3);
    });
    it('render disabled edit and delete buttons', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules} onEditRule={handleShowEditRule} onDeleteRule={handleDelete} disabled/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes().at(0).prop('aria-disabled')).toEqual(true);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes().at(0).prop('aria-disabled')).toEqual(true);
    });
    it('render edit button only', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules} onEditRule={handleShowEditRule}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes()).toHaveLength(3);
        expect(wrapper.find('[aria-label="Delete Rule"]')).toHaveLength(0);
    });
    it('render delete button only', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<rules_1.default rules={rules} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]')).toHaveLength(0);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes()).toHaveLength(3);
    });
});
//# sourceMappingURL=rules.spec.jsx.map