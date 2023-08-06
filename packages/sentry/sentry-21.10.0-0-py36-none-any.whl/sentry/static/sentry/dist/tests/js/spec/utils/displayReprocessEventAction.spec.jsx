Object.defineProperty(exports, "__esModule", { value: true });
const displayReprocessEventAction_1 = require("app/utils/displayReprocessEventAction");
describe('DisplayReprocessEventAction', function () {
    const orgFeatures = ['reprocessing-v2'];
    it('returns false in case of no reprocessing-v2 feature', function () {
        // @ts-expect-error
        const event = TestStubs.EventStacktraceMessage();
        expect((0, displayReprocessEventAction_1.displayReprocessEventAction)([], event)).toBe(false);
    });
    it('returns false in case of no event', function () {
        expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures)).toBe(false);
    });
    it('returns false if no exception entry is found', function () {
        // @ts-expect-error
        const event = TestStubs.EventStacktraceMessage();
        expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(false);
    });
    it('returns false if the event is not a mini-dump event or an Apple crash report event or a Native event', function () {
        // @ts-expect-error
        const event = TestStubs.EventStacktraceException();
        expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(false);
    });
    describe('returns true', function () {
        describe('native event', function () {
            describe('event with defined platform', function () {
                it('native', function () {
                    // @ts-expect-error
                    const event = TestStubs.EventStacktraceException({
                        platform: 'native',
                    });
                    expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
                });
                it('cocoa', function () {
                    // @ts-expect-error
                    const event = TestStubs.EventStacktraceException({
                        platform: 'cocoa',
                    });
                    expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
                });
            });
            describe('event with undefined platform, but stack trace has platform', function () {
                it('native', function () {
                    // @ts-expect-error
                    const event = TestStubs.EventStacktraceException({
                        platform: undefined,
                    });
                    event.entries[0].data.values[0].stacktrace.frames[0].platform = 'native';
                    expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
                });
                it('cocoa', function () {
                    // @ts-expect-error
                    const event = TestStubs.EventStacktraceException({
                        platform: undefined,
                    });
                    event.entries[0].data.values[0].stacktrace.frames[0].platform = 'cocoa';
                    expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
                });
            });
        });
        it('mini-dump event', function () {
            // @ts-expect-error
            const event = TestStubs.EventStacktraceException({
                platform: undefined,
            });
            event.entries[0].data.values[0] = Object.assign(Object.assign({}, event.entries[0].data.values[0]), { mechanism: {
                    type: 'minidump',
                } });
            expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
        });
        it('apple crash report event', function () {
            // @ts-expect-error
            const event = TestStubs.EventStacktraceException({
                platform: undefined,
            });
            event.entries[0].data.values[0] = Object.assign(Object.assign({}, event.entries[0].data.values[0]), { mechanism: {
                    type: 'applecrashreport',
                } });
            expect((0, displayReprocessEventAction_1.displayReprocessEventAction)(orgFeatures, event)).toBe(true);
        });
    });
});
//# sourceMappingURL=displayReprocessEventAction.spec.jsx.map