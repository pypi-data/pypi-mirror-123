Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const content_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/content"));
const convertRelayPiiConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/dataScrubbing/convertRelayPiiConfig"));
// @ts-expect-error
const relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
const stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
const convertedRules = (0, convertRelayPiiConfig_1.default)(stringRelayPiiConfig);
const handleEditRule = jest.fn();
const handleDelete = jest.fn();
describe('Content', () => {
    it('default render - empty', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<content_1.default rules={[]} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.text()).toEqual('You have no data scrubbing rules');
    });
    it('render rules', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<content_1.default rules={convertedRules} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('List')).toHaveLength(1);
    });
});
//# sourceMappingURL=content.spec.jsx.map