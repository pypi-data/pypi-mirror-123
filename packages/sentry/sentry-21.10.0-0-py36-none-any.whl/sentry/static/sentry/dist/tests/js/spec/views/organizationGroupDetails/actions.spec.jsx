Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const modalActions_1 = (0, tslib_1.__importDefault)(require("app/actions/modalActions"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const actions_1 = (0, tslib_1.__importDefault)(require("app/views/organizationGroupDetails/actions"));
// @ts-expect-error
const group = TestStubs.Group({
    id: '1337',
    pluginActions: [],
    pluginIssues: [],
});
// @ts-expect-error
const project = TestStubs.ProjectDetails({
    id: '2448',
    name: 'project name',
    slug: 'project',
});
// @ts-expect-error
const organization = TestStubs.Organization({
    id: '4660',
    slug: 'org',
    features: ['reprocessing-v2'],
});
function renderComponent(event) {
    return (0, enzyme_1.mountWithTheme)(<actions_1.default group={group} project={project} organization={organization} event={event} disabled={false}/>);
}
describe('GroupActions', function () {
    beforeEach(function () {
        jest.spyOn(configStore_1.default, 'get').mockImplementation(() => []);
    });
    describe('render()', function () {
        it('renders correctly', function () {
            const wrapper = renderComponent();
            expect(wrapper).toSnapshot();
        });
    });
    describe('subscribing', function () {
        let issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isSubscribed: false }),
            });
        });
        it('can subscribe', function () {
            const wrapper = renderComponent();
            const btn = wrapper.find('button[aria-label="Subscribe"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isSubscribed: true },
            }));
        });
    });
    describe('bookmarking', function () {
        let issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isBookmarked: false }),
            });
        });
        it('can bookmark', function () {
            const wrapper = renderComponent();
            const btn = wrapper.find('button[aria-label="Bookmark"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isBookmarked: true },
            }));
        });
    });
    describe('reprocessing', function () {
        it('renders ReprocessAction component if org has feature flag reprocessing-v2', function () {
            const wrapper = renderComponent();
            const reprocessActionButton = wrapper.find('ReprocessAction');
            expect(reprocessActionButton).toBeTruthy();
        });
        it('open dialog by clicking on the ReprocessAction component', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                const event = TestStubs.EventStacktraceException({
                    platform: 'native',
                });
                const onReprocessEventFunc = jest.spyOn(modalActions_1.default, 'openModal');
                const wrapper = renderComponent(event);
                const reprocessActionButton = wrapper.find('ReprocessAction');
                expect(reprocessActionButton).toBeTruthy();
                reprocessActionButton.simulate('click');
                // @ts-expect-error
                yield tick();
                expect(onReprocessEventFunc).toHaveBeenCalled();
            });
        });
    });
});
//# sourceMappingURL=actions.spec.jsx.map