Object.defineProperty(exports, "__esModule", { value: true });
const types_1 = require("app/views/dashboardsV2/types");
const utils_1 = require("app/views/dashboardsV2/utils");
describe('Dashboards util', () => {
    describe('constructWidgetFromQuery', () => {
        let baseQuery;
        beforeEach(() => {
            baseQuery = {
                displayType: 'line',
                interval: '5m',
                queryConditions: ['title:test', 'event.type:test'],
                queryFields: ['count()', 'failure_count()'],
                queryNames: ['1', '2'],
                queryOrderby: '',
                title: 'Widget Title',
            };
        });
        it('returns a widget when given a valid query', () => {
            const widget = (0, utils_1.constructWidgetFromQuery)(baseQuery);
            expect(widget === null || widget === void 0 ? void 0 : widget.displayType).toEqual(types_1.DisplayType.LINE);
            expect(widget === null || widget === void 0 ? void 0 : widget.interval).toEqual('5m');
            expect(widget === null || widget === void 0 ? void 0 : widget.title).toEqual('Widget Title');
            expect(widget === null || widget === void 0 ? void 0 : widget.queries).toEqual([
                {
                    name: '1',
                    fields: ['count()', 'failure_count()'],
                    conditions: 'title:test',
                    orderby: '',
                },
                {
                    name: '2',
                    fields: ['count()', 'failure_count()'],
                    conditions: 'event.type:test',
                    orderby: '',
                },
            ]);
        });
        it('returns undefined if query is missing title', () => {
            baseQuery.title = '';
            const widget = (0, utils_1.constructWidgetFromQuery)(baseQuery);
            expect(widget).toBeUndefined();
        });
        it('returns undefined if query is missing interval', () => {
            baseQuery.interval = '';
            const widget = (0, utils_1.constructWidgetFromQuery)(baseQuery);
            expect(widget).toBeUndefined();
        });
        it('returns undefined if query is missing displayType', () => {
            baseQuery.displayType = '';
            const widget = (0, utils_1.constructWidgetFromQuery)(baseQuery);
            expect(widget).toBeUndefined();
        });
        it('returns a widget when given string fields and conditions', () => {
            baseQuery.queryConditions = 'title:test';
            baseQuery.queryFields = 'count()';
            const widget = (0, utils_1.constructWidgetFromQuery)(baseQuery);
            expect(widget === null || widget === void 0 ? void 0 : widget.displayType).toEqual(types_1.DisplayType.LINE);
            expect(widget === null || widget === void 0 ? void 0 : widget.interval).toEqual('5m');
            expect(widget === null || widget === void 0 ? void 0 : widget.title).toEqual('Widget Title');
            expect(widget === null || widget === void 0 ? void 0 : widget.queries).toEqual([
                {
                    name: '1',
                    fields: ['count()'],
                    conditions: 'title:test',
                    orderby: '',
                },
            ]);
        });
    });
});
//# sourceMappingURL=utils.spec.jsx.map