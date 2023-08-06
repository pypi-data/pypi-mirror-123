Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const utils_1 = require("sentry-test/utils");
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const types_1 = require("app/types");
// @ts-expect-error
const group = TestStubs.Group({
    level: 'error',
    metadata: {
        type: 'metadata type',
        directive: 'metadata directive',
        uri: 'metadata uri',
        value: 'metadata value',
        message: 'metadata message',
    },
    culprit: 'culprit',
});
// @ts-expect-error
const event = TestStubs.Event({
    id: 'id',
    eventID: 'eventID',
    groupID: 'groupID',
    culprit: undefined,
    metadata: {
        type: 'metadata type',
        directive: 'metadata directive',
        uri: 'metadata uri',
        value: 'metadata value',
        message: 'metadata message',
    },
});
describe('EventOrGroupHeader', function () {
    const { organization, router, routerContext } = (0, initializeOrg_1.initializeOrg)({
        router: { orgId: 'orgId' },
    });
    describe('Group', function () {
        it('renders with `type = error`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={group} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('renders with `type = csp`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, group), { type: types_1.EventOrGroupType.CSP })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('renders with `type = default`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, group), { type: types_1.EventOrGroupType.DEFAULT, metadata: Object.assign(Object.assign({}, group.metadata), { title: 'metadata title' }) })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('renders metadata values in message for error events', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, group), { type: types_1.EventOrGroupType.ERROR })} {...router}/>, { context: routerContext });
            expect(reactTestingLibrary_1.screen.getByText('metadata value')).toBeTruthy();
        });
        it('renders location', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, group), { metadata: {
                            filename: 'path/to/file.swift',
                        }, platform: 'swift', type: types_1.EventOrGroupType.ERROR })} {...router}/>, { context: routerContext });
                expect(yield (0, utils_1.findByTextContent)(component, 'in path/to/file.swift')).toBeTruthy();
            });
        });
    });
    describe('Event', function () {
        it('renders with `type = error`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.ERROR })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('renders with `type = csp`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.CSP })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('renders with `type = default`', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.DEFAULT, metadata: Object.assign(Object.assign({}, event.metadata), { title: 'metadata title' }) })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('hides level tag', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default projectId="projectId" hideLevel organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.DEFAULT, metadata: Object.assign(Object.assign({}, event.metadata), { title: 'metadata title' }) })} {...router}/>, { context: routerContext });
            expect(container).toSnapshot();
        });
        it('keeps sort in link when query has sort', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.DEFAULT })} {...router} location={Object.assign(Object.assign({}, router.location), { query: Object.assign(Object.assign({}, router.location.query), { sort: 'freq' }) })}/>);
            expect(reactTestingLibrary_1.screen.getByRole('link')).toHaveAttribute('href', '/organizations/org-slug/issues/groupID/events/eventID/?_allp=1&sort=freq');
        });
        it('lack of project adds allp parameter', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<eventOrGroupHeader_1.default organization={organization} data={Object.assign(Object.assign({}, event), { type: types_1.EventOrGroupType.DEFAULT })} {...router} location={Object.assign(Object.assign({}, router.location), { query: {} })}/>);
            expect(reactTestingLibrary_1.screen.getByRole('link')).toHaveAttribute('href', '/organizations/org-slug/issues/groupID/events/eventID/?_allp=1');
        });
    });
});
//# sourceMappingURL=eventOrGroupHeader.spec.jsx.map