Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const modal_1 = require("sentry-test/modal");
const modal_2 = require("app/actionCreators/modal");
const modalActions_1 = (0, tslib_1.__importDefault)(require("app/actions/modalActions"));
// @ts-expect-error
const group = TestStubs.Group({
    id: '1337',
    pluginActions: [],
    pluginIssues: [],
});
// @ts-expect-error
const organization = TestStubs.Organization({
    id: '4660',
    slug: 'org',
    features: ['reprocessing-v2'],
});
function renderComponent() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const modal = yield (0, modal_1.mountGlobalModal)();
        (0, modal_2.openReprocessEventModal)({ organization, groupId: group.id });
        // @ts-expect-error
        yield tick();
        // @ts-expect-error
        yield tick();
        modal.update();
        return modal;
    });
}
describe('ReprocessEventModal', function () {
    let wrapper;
    beforeAll(function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            wrapper = yield renderComponent();
        });
    });
    it('modal is open', () => {
        expect(wrapper.find('Header').text()).toEqual('Reprocess Events');
    });
    it('form fields & info', () => {
        // some info about reprocessing
        const introduction = wrapper.find('Introduction');
        expect(introduction).toBeTruthy();
        expect(introduction).toHaveLength(2);
        // Reprocess impacts
        expect(introduction.at(0).text()).toEqual('Reprocessing applies new debug files and grouping enhancements to this Issue. Please consider these impacts:');
        const impacts = wrapper.find('StyledList');
        expect(impacts).toBeTruthy();
        expect(impacts.length).toBeGreaterThan(0);
        // Docs info
        expect(introduction.at(1).text()).toEqual('For more information, please refer to the documentation.');
        // Form
        const form = wrapper.find('Form');
        expect(form).toBeTruthy();
        // Number of events to be reprocessed field
        const reprocessQuantityField = form.find('NumberField');
        expect(reprocessQuantityField).toBeTruthy();
        // Remaining events action field
        const remainingEventsActionField = form.find('RadioField');
        expect(remainingEventsActionField).toBeTruthy();
    });
    it('reprocess all events', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: `/organizations/${organization.slug}/issues/${group.id}/reprocessing/`,
            method: 'POST',
            body: [],
        });
        jest.spyOn(window.location, 'reload').mockImplementation(() => { });
        const closeModalFunc = jest.spyOn(modalActions_1.default, 'closeModal');
        // Number of events to be reprocessed field
        const reprocessQuantityField = wrapper.find('NumberField input');
        expect(reprocessQuantityField.props().placeholder).toEqual('Reprocess all events');
        expect(reprocessQuantityField.props().value).toEqual(undefined);
        const submitButton = wrapper.find('[data-test-id="form-submit"]').hostNodes();
        submitButton.simulate('submit');
        // @ts-expect-error
        yield tick();
        wrapper.update();
        expect(window.location.reload).toHaveBeenCalled();
        expect(closeModalFunc).toHaveBeenCalled();
    }));
});
//# sourceMappingURL=reprocessEventModal.spec.jsx.map