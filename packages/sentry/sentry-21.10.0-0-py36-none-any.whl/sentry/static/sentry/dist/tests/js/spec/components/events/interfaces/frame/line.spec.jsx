Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const line_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/frame/line"));
describe('Frame - Line', function () {
    // @ts-expect-error
    const event = TestStubs.Event();
    const data = {
        absPath: null,
        colNo: null,
        context: [],
        errors: null,
        filename: null,
        function: null,
        inApp: false,
        instructionAddr: null,
        lineNo: null,
        module: null,
        package: null,
        platform: null,
        rawFunction: null,
        symbol: null,
        symbolAddr: null,
        trust: null,
        vars: null,
    };
    describe('renderOriginalSourceInfo()', function () {
        it('should render the source map information as a HTML string', function () {
            const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<line_1.default data={Object.assign({ origAbsPath: 'https://beta.getsentry.com/_static/sentry/dist/vendor.js', mapUrl: 'https://beta.getsentry.com/_static/sentry/dist/vendor.js.map', map: 'vendor.js.map' }, data)} registers={{}} components={[]} event={event}/>);
            expect(container).toSnapshot();
        });
    });
    describe('renderContext()', () => {
        it('should render context lines', () => {
            (0, reactTestingLibrary_1.mountWithTheme)(<line_1.default data={Object.assign(Object.assign({}, data), { context: [
                        [
                            211,
                            '    # Mark the crashed thread and add its stacktrace to the exception',
                        ],
                        [212, "    crashed_thread = data['threads'][state.requesting_thread]"],
                        [213, "    crashed_thread['crashed'] = True"],
                    ] })} registers={{}} components={[]} event={event} isExpanded/>);
            expect(reactTestingLibrary_1.screen.queryByRole('list')).toSnapshot();
        });
        it('should render register values', () => {
            (0, reactTestingLibrary_1.mountWithTheme)(<line_1.default data={data} registers={{
                    r10: '0x00007fff9300bf70',
                    r11: '0xffffffffffffffff',
                    r12: '0x0000000000000000',
                    r13: '0x0000000000000000',
                    r14: '0x000000000000000a',
                    r15: '0x0000000000000000',
                    r8: '0x00007fff9300bf78',
                    r9: '0x0000000000000040',
                    rax: '0x00007fff9291e660',
                    rbp: '0x00007ffedfdff7e0',
                    rbx: '0x00007fff9291e660',
                    rcx: '0x0000000000000008',
                    rdi: '0x00007ffedfdff790',
                    rdx: '0x0000020000000303',
                    rip: '0x000000010fe00a59',
                    rsi: '0x0000000000000300',
                    rsp: '0x00007ffedfdff7c0',
                }} components={[]} event={event} isExpanded/>);
            expect(reactTestingLibrary_1.screen.getByText('registers')).toBeInTheDocument();
        });
        it('should not render empty registers', () => {
            (0, reactTestingLibrary_1.mountWithTheme)(<line_1.default data={data} registers={{}} components={[]} event={event} isExpanded/>);
            expect(reactTestingLibrary_1.screen.queryByText('registers')).toBeFalsy();
        });
        it('should render context vars', () => {
            const vars = {
                origin: null,
                helper: '<sentry.coreapi.MinidumpApiHelper object at 0x10e157ed0>',
                self: '<sentry.web.api.MinidumpView object at 0x10e157250>',
                args: [],
                request: '<WSGIRequest at 0x4531253712>',
                content: '[Filtered]',
                kwargs: {},
                project_id: "u'3'",
            };
            (0, reactTestingLibrary_1.mountWithTheme)(<line_1.default data={Object.assign(Object.assign({}, data), { vars })} registers={{}} components={[]} event={event} isExpanded/>);
            for (const [key, value] of Object.entries(vars)) {
                const row = reactTestingLibrary_1.screen.getByText(key).closest('tr');
                expect(row).toBeTruthy();
                if (!row) {
                    return;
                }
                const utils = (0, reactTestingLibrary_1.within)(row);
                expect(utils.getByText(key)).toBeInTheDocument();
                if (typeof value !== 'string') {
                    return;
                }
                expect(utils.getByText(value)).toBeInTheDocument();
            }
        });
    });
});
//# sourceMappingURL=line.spec.jsx.map