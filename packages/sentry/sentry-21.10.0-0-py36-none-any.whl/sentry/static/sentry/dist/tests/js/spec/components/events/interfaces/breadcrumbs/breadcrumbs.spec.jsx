Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const utils_1 = require("sentry-test/utils");
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/breadcrumbs"));
const breadcrumbs_2 = require("app/types/breadcrumbs");
const event_1 = require("app/types/event");
describe('Breadcrumbs', () => {
    let props;
    const { router } = (0, initializeOrg_1.initializeOrg)();
    beforeEach(() => {
        props = {
            route: {},
            router,
            // @ts-expect-error
            organization: TestStubs.Organization(),
            // @ts-expect-error
            event: TestStubs.Event({ entries: [] }),
            type: event_1.EntryType.BREADCRUMBS,
            data: {
                values: [
                    {
                        message: 'sup',
                        category: 'default',
                        level: breadcrumbs_2.BreadcrumbLevelType.WARNING,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'hey',
                        category: 'error',
                        level: breadcrumbs_2.BreadcrumbLevelType.INFO,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'hello',
                        category: 'default',
                        level: breadcrumbs_2.BreadcrumbLevelType.WARNING,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'bye',
                        category: 'default',
                        level: breadcrumbs_2.BreadcrumbLevelType.WARNING,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'ok',
                        category: 'error',
                        level: breadcrumbs_2.BreadcrumbLevelType.WARNING,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'sup',
                        category: 'default',
                        level: breadcrumbs_2.BreadcrumbLevelType.WARNING,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                    {
                        message: 'sup',
                        category: 'default',
                        level: breadcrumbs_2.BreadcrumbLevelType.INFO,
                        type: breadcrumbs_2.BreadcrumbType.INFO,
                    },
                ],
            },
        };
    });
    describe('filterCrumbs', function () {
        it('should filter crumbs based on crumb message', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
                const searchInput = reactTestingLibrary_1.screen.getByPlaceholderText('Search breadcrumbs');
                reactTestingLibrary_1.fireEvent.change(searchInput, { target: { value: 'hi' } });
                expect(yield reactTestingLibrary_1.screen.findByText('Sorry, no breadcrumbs match your search query')).toBeInTheDocument();
                reactTestingLibrary_1.fireEvent.change(searchInput, { target: { value: 'up' } });
                expect(reactTestingLibrary_1.screen.queryByText('Sorry, no breadcrumbs match your search query')).toBe(null);
                expect(yield (0, utils_1.findAllByTextContent)(component, 'sup')).toHaveLength(3);
            });
        });
        it('should filter crumbs based on crumb level', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
                const searchInput = reactTestingLibrary_1.screen.getByPlaceholderText('Search breadcrumbs');
                reactTestingLibrary_1.fireEvent.change(searchInput, { target: { value: 'war' } });
                // breadcrumbs + filter item
                // TODO(Priscila): Filter should not render in the dom if not open
                expect(yield (0, utils_1.findAllByTextContent)(component, 'Warning')).toHaveLength(6);
            });
        });
        it('should filter crumbs based on crumb category', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
                const searchInput = reactTestingLibrary_1.screen.getByPlaceholderText('Search breadcrumbs');
                reactTestingLibrary_1.fireEvent.change(searchInput, { target: { value: 'error' } });
                expect(yield (0, utils_1.findAllByTextContent)(component, 'error')).toHaveLength(2);
            });
        });
    });
    describe('render', function () {
        it('should display the correct number of crumbs with no filter', function () {
            props.data.values = props.data.values.slice(0, 4);
            (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
            // data.values + virtual crumb
            expect(reactTestingLibrary_1.screen.queryAllByTestId('crumb')).toHaveLength(4);
            expect(reactTestingLibrary_1.screen.getByTestId('last-crumb')).toBeInTheDocument();
        });
        it('should display the correct number of crumbs with a filter', function () {
            props.data.values = props.data.values.slice(0, 4);
            (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
            const searchInput = reactTestingLibrary_1.screen.getByPlaceholderText('Search breadcrumbs');
            reactTestingLibrary_1.fireEvent.change(searchInput, { target: { value: 'sup' } });
            expect(reactTestingLibrary_1.screen.queryAllByTestId('crumb')).toHaveLength(0);
            expect(reactTestingLibrary_1.screen.getByTestId('last-crumb')).toBeInTheDocument();
        });
        it('should not crash if data contains a toString attribute', function () {
            // Regression test: A "toString" property in data should not falsely be
            // used to coerce breadcrumb data to string. This would cause a TypeError.
            const data = { nested: { toString: 'hello' } };
            props.data.values = [
                {
                    message: 'sup',
                    category: 'default',
                    level: breadcrumbs_2.BreadcrumbLevelType.INFO,
                    type: breadcrumbs_2.BreadcrumbType.INFO,
                    data,
                },
            ];
            (0, reactTestingLibrary_1.mountWithTheme)(<breadcrumbs_1.default {...props}/>);
            // data.values + virtual crumb
            expect(reactTestingLibrary_1.screen.queryAllByTestId('crumb')).toHaveLength(1);
            expect(reactTestingLibrary_1.screen.getByTestId('last-crumb')).toBeInTheDocument();
        });
    });
});
//# sourceMappingURL=breadcrumbs.spec.jsx.map