Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const miniGraph_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/miniGraph"));
describe('EventsV2 > MiniGraph', function () {
    const features = ['discover-basic', 'connect-discover-and-dashboards'];
    const location = {
        query: { query: 'tag:value' },
        pathname: '/',
    };
    let organization, eventView, initialData;
    beforeEach(() => {
        // @ts-expect-error
        organization = TestStubs.Organization({
            features,
            // @ts-expect-error
            projects: [TestStubs.Project()],
        });
        initialData = (0, initializeOrg_1.initializeOrg)({
            organization,
            router: {
                location,
            },
            project: 1,
            projects: [],
        });
        // @ts-expect-error
        eventView = eventView_1.default.fromSavedQueryOrLocation(undefined, location);
    });
    it('makes an EventsRequest with all selected multi y axis', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const yAxis = ['count()', 'failure_count()'];
            const wrapper = (0, enzyme_1.mountWithTheme)(<miniGraph_1.default 
            // @ts-expect-error
            location={location} eventView={eventView} organization={organization} yAxis={yAxis}/>, initialData.routerContext);
            const eventsRequestProps = wrapper.find('EventsRequest').props();
            expect(eventsRequestProps.yAxis).toEqual(yAxis);
        });
    });
});
//# sourceMappingURL=miniGraph.spec.jsx.map