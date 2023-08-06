Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const test_utils_1 = require("react-dom/test-utils");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventEntries_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventEntries"));
const event_1 = require("app/types/event");
const { organization, project } = (0, initializeOrg_1.initializeOrg)();
// @ts-expect-error
const api = new MockApiClient();
function renderComponent(event, errors) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<eventEntries_1.default organization={organization} event={Object.assign(Object.assign({}, event), { errors: errors !== null && errors !== void 0 ? errors : event.errors })} project={project} location={location} api={api}/>);
        // @ts-expect-error
        yield tick();
        wrapper.update();
        const eventErrors = wrapper.find('Errors');
        const bannerSummary = eventErrors.find('BannerSummary');
        const bannerSummaryInfo = bannerSummary.find('span[data-test-id="errors-banner-summary-info"]');
        const toggleButton = bannerSummary
            .find('[data-test-id="event-error-toggle"]')
            .hostNodes();
        toggleButton.simulate('click');
        // @ts-expect-error
        yield tick();
        wrapper.update();
        const errorItem = wrapper.find('ErrorItem');
        return { bannerSummaryInfoText: bannerSummaryInfo.text(), errorItem };
    });
}
describe('GroupEventEntries', function () {
    // @ts-expect-error
    const event = TestStubs.Event();
    beforeEach(() => {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: `/projects/${organization.slug}/${project.slug}/events/${event.id}/grouping-info/`,
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: `/projects/${organization.slug}/${project.slug}/files/dsyms/`,
            body: [],
        });
    });
    describe('EventError', function () {
        it('renders', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const errors = [
                    {
                        type: 'invalid_data',
                        data: {
                            name: 'logentry',
                        },
                        message: 'no message present',
                    },
                    {
                        type: 'invalid_data',
                        data: {
                            name: 'breadcrumbs.values.2.data',
                        },
                        message: 'expected an object',
                    },
                ];
                const { bannerSummaryInfoText, errorItem } = yield renderComponent(event, errors);
                expect(bannerSummaryInfoText).toEqual(`There were ${errors.length} problems processing this event`);
                expect(errorItem.length).toBe(2);
                expect(errorItem.at(0).props().error).toEqual(errors[0]);
                expect(errorItem.at(1).props().error).toEqual(errors[1]);
            });
        });
        describe('Proguard erros', function () {
            const proGuardUuid = 'a59c8fcc-2f27-49f8-af9e-02661fc3e8d7';
            it('Missing mapping file', function () {
                return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                    const newEvent = Object.assign(Object.assign({}, event), { platform: 'java', entries: [
                            {
                                type: event_1.EntryType.DEBUGMETA,
                                data: {
                                    images: [{ type: 'proguard', uuid: proGuardUuid }],
                                },
                            },
                        ] });
                    yield (0, test_utils_1.act)(() => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                        const { errorItem, bannerSummaryInfoText } = yield renderComponent(newEvent);
                        expect(bannerSummaryInfoText).toEqual('There was 1 problem processing this event');
                        expect(errorItem.length).toBe(1);
                        expect(errorItem.at(0).props().error).toEqual({
                            type: 'proguard_missing_mapping',
                            message: 'A proguard mapping file was missing.',
                            data: { mapping_uuid: proGuardUuid },
                        });
                    }));
                });
            });
            it("Don't display extra proguard errors, if the entry error of an event has an error of type 'proguard_missing_mapping'", function () {
                return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                    const newEvent = Object.assign(Object.assign({}, event), { platform: 'java', entries: [
                            {
                                type: event_1.EntryType.DEBUGMETA,
                                data: {
                                    images: [{ type: 'proguard', uuid: proGuardUuid }],
                                },
                            },
                        ], errors: [
                            {
                                type: 'proguard_missing_mapping',
                                message: 'A proguard mapping file was missing.',
                                data: { mapping_uuid: proGuardUuid },
                            },
                        ] });
                    const { bannerSummaryInfoText, errorItem } = yield renderComponent(newEvent);
                    expect(bannerSummaryInfoText).toEqual('There was 1 problem processing this event');
                    expect(errorItem.length).toBe(1);
                    expect(errorItem.at(0).props().error).toEqual({
                        type: 'proguard_missing_mapping',
                        message: 'A proguard mapping file was missing.',
                        data: { mapping_uuid: proGuardUuid },
                    });
                });
            });
            describe('ProGuard Plugin seems to not be correctly configured', function () {
                it('find minified data in the exception entry', function () {
                    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                        const newEvent = Object.assign(Object.assign({}, event), { platform: 'java', entries: [
                                {
                                    type: 'exception',
                                    data: {
                                        values: [
                                            {
                                                stacktrace: {
                                                    frames: [
                                                        {
                                                            function: null,
                                                            colNo: null,
                                                            vars: {},
                                                            symbol: null,
                                                            module: 'a.$a.a.a',
                                                        },
                                                    ],
                                                    framesOmitted: null,
                                                    registers: null,
                                                    hasSystemFrames: false,
                                                },
                                                module: null,
                                                rawStacktrace: null,
                                                mechanism: null,
                                                threadId: null,
                                                value: 'Unexpected token else',
                                                type: 'SyntaxError',
                                            },
                                        ],
                                        excOmitted: null,
                                        hasSystemFrames: false,
                                    },
                                },
                            ] });
                        const { bannerSummaryInfoText, errorItem } = yield renderComponent(newEvent);
                        expect(bannerSummaryInfoText).toEqual('There was 1 problem processing this event');
                        expect(errorItem.length).toBe(1);
                        const { type, message } = errorItem.at(0).props().error;
                        expect(type).toEqual('proguard_potentially_misconfigured_plugin');
                        expect(message).toBeTruthy();
                    });
                });
                it('find minified data in the threads entry', function () {
                    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                        const newEvent = Object.assign(Object.assign({}, event), { platform: 'java', entries: [
                                {
                                    type: 'exception',
                                    data: {
                                        values: [
                                            {
                                                stacktrace: {
                                                    frames: [
                                                        {
                                                            function: null,
                                                            colNo: null,
                                                            vars: {},
                                                            symbol: null,
                                                            module: 'a.$a.a.a',
                                                        },
                                                    ],
                                                    framesOmitted: null,
                                                    registers: null,
                                                    hasSystemFrames: false,
                                                },
                                                module: null,
                                                rawStacktrace: null,
                                                mechanism: null,
                                                threadId: null,
                                                value: 'Unexpected token else',
                                                type: 'SyntaxError',
                                            },
                                        ],
                                        excOmitted: null,
                                        hasSystemFrames: false,
                                    },
                                },
                                {
                                    type: 'threads',
                                    data: {
                                        values: [
                                            {
                                                stacktrace: {
                                                    frames: [
                                                        {
                                                            function: 'start',
                                                            package: 'libdyld.dylib',
                                                            module: 'a.$a.a.a',
                                                        },
                                                        {
                                                            function: 'main',
                                                            package: 'iOS-Swift',
                                                            module: '',
                                                        },
                                                    ],
                                                },
                                            },
                                        ],
                                    },
                                },
                            ] });
                        const { bannerSummaryInfoText, errorItem } = yield renderComponent(newEvent);
                        expect(bannerSummaryInfoText).toEqual('There was 1 problem processing this event');
                        expect(errorItem.length).toBe(1);
                        const { type, message } = errorItem.at(0).props().error;
                        expect(type).toEqual('proguard_potentially_misconfigured_plugin');
                        expect(message).toBeTruthy();
                    });
                });
            });
        });
    });
});
//# sourceMappingURL=groupEventEntries.spec.jsx.map