Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const api_1 = require("app/api");
const spanTreeModel_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/spans/spanTreeModel"));
const utils_1 = require("app/components/events/interfaces/spans/utils");
const event_1 = require("app/types/event");
const utils_2 = require("app/types/utils");
describe('SpanTreeModel', () => {
    const api = new api_1.Client();
    const event = {
        id: '2b658a829a21496b87fd1f14a61abf65',
        eventID: '2b658a829a21496b87fd1f14a61abf65',
        title: '/organizations/:orgId/discover/results/',
        type: 'transaction',
        startTimestamp: 1622079935.86141,
        endTimestamp: 1622079940.032905,
        contexts: {
            trace: {
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                span_id: 'a934857184bdf5a6',
                op: 'pageload',
                status: 'unknown',
                type: 'trace',
            },
        },
        entries: [
            {
                data: [
                    {
                        timestamp: 1622079937.227645,
                        start_timestamp: 1622079936.90689,
                        description: 'GET /api/0/organizations/?member=1',
                        op: 'http',
                        span_id: 'b23703998ae619e7',
                        parent_span_id: 'a934857184bdf5a6',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        status: 'ok',
                        tags: {
                            'http.status_code': '200',
                        },
                        data: {
                            method: 'GET',
                            type: 'fetch',
                            url: '/api/0/organizations/?member=1',
                        },
                    },
                    {
                        timestamp: 1622079937.20331,
                        start_timestamp: 1622079936.907515,
                        description: 'GET /api/0/internal/health/',
                        op: 'http',
                        span_id: 'a453cc713e5baf9c',
                        parent_span_id: 'a934857184bdf5a6',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        status: 'ok',
                        tags: {
                            'http.status_code': '200',
                        },
                        data: {
                            method: 'GET',
                            type: 'fetch',
                            url: '/api/0/internal/health/',
                        },
                    },
                    {
                        timestamp: 1622079936.05839,
                        start_timestamp: 1622079936.048125,
                        description: '/_static/dist/sentry/sentry.541f5b.css',
                        op: 'resource.link',
                        span_id: 'a23f26b939d1a735',
                        parent_span_id: 'a453cc713e5baf9c',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        data: {
                            'Decoded Body Size': 159248,
                            'Encoded Body Size': 159248,
                            'Transfer Size': 275,
                        },
                    },
                ],
                type: event_1.EntryType.SPANS,
            },
        ],
    };
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/sentry/events/project:19c403a10af34db2b7d93ad669bb51ed/',
        body: Object.assign(Object.assign({}, event), { contexts: {
                trace: {
                    trace_id: '61d2d7c5acf448ffa8e2f8f973e2cd36',
                    span_id: 'a5702f287954a9ef',
                    parent_span_id: 'b23703998ae619e7',
                    op: 'something',
                    status: 'unknown',
                    type: 'trace',
                },
            }, entries: [
                {
                    data: [
                        {
                            timestamp: 1622079937.227645,
                            start_timestamp: 1622079936.90689,
                            description: 'something child',
                            op: 'child',
                            span_id: 'bcbea9f18a11e161',
                            parent_span_id: 'a5702f287954a9ef',
                            trace_id: '61d2d7c5acf448ffa8e2f8f973e2cd36',
                            status: 'ok',
                            data: {},
                        },
                    ],
                    type: event_1.EntryType.SPANS,
                },
            ] }),
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/sentry/events/project:broken/',
        body: Object.assign({}, event),
        statusCode: 500,
    });
    it('makes children', () => {
        const parsedTrace = (0, utils_1.parseTrace)(event);
        const rootSpan = (0, utils_1.generateRootSpan)(parsedTrace);
        const spanTreeModel = new spanTreeModel_1.default(rootSpan, parsedTrace.childSpans, api);
        expect(spanTreeModel.children).toHaveLength(2);
    });
    it('handles recursive children', () => {
        const event2 = Object.assign(Object.assign({}, event), { entries: [
                {
                    data: [
                        {
                            timestamp: 1622079937.227645,
                            start_timestamp: 1622079936.90689,
                            description: 'GET /api/0/organizations/?member=1',
                            op: 'http',
                            span_id: 'a934857184bdf5a6',
                            parent_span_id: 'a934857184bdf5a6',
                            trace_id: '8cbbc19c0f54447ab702f00263262726',
                            status: 'ok',
                            tags: {
                                'http.status_code': '200',
                            },
                            data: {
                                method: 'GET',
                                type: 'fetch',
                                url: '/api/0/organizations/?member=1',
                            },
                        },
                    ],
                    type: event_1.EntryType.SPANS,
                },
            ] });
        const parsedTrace = (0, utils_1.parseTrace)(event2);
        const rootSpan = (0, utils_1.generateRootSpan)(parsedTrace);
        const spanTreeModel = new spanTreeModel_1.default(rootSpan, parsedTrace.childSpans, api);
        expect(spanTreeModel.children).toHaveLength(1);
    });
    it('operationNameCounts', () => {
        const parsedTrace = (0, utils_1.parseTrace)(event);
        const rootSpan = (0, utils_1.generateRootSpan)(parsedTrace);
        const spanTreeModel = new spanTreeModel_1.default(rootSpan, parsedTrace.childSpans, api);
        expect(Object.fromEntries(spanTreeModel.operationNameCounts)).toMatchObject({
            http: 2,
            pageload: 1,
            'resource.link': 1,
        });
    });
    it('toggleEmbeddedChildren - happy path', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const parsedTrace = (0, utils_1.parseTrace)(event);
        const rootSpan = (0, utils_1.generateRootSpan)(parsedTrace);
        const spanTreeModel = new spanTreeModel_1.default(rootSpan, parsedTrace.childSpans, api);
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('idle');
        const fullWaterfall = [
            {
                type: 'span',
                span: {
                    trace_id: '8cbbc19c0f54447ab702f00263262726',
                    span_id: 'a934857184bdf5a6',
                    parent_span_id: undefined,
                    start_timestamp: 1622079935.86141,
                    timestamp: 1622079940.032905,
                    op: 'pageload',
                    description: undefined,
                    data: {},
                    status: 'unknown',
                },
                numOfSpanChildren: 2,
                treeDepth: 0,
                isLastSibling: true,
                continuingTreeDepths: [],
                showEmbeddedChildren: false,
                toggleEmbeddedChildren: expect.any(Function),
                fetchEmbeddedChildrenState: 'idle',
                toggleSpanGroup: undefined,
            },
            {
                type: 'span',
                span: {
                    timestamp: 1622079937.227645,
                    start_timestamp: 1622079936.90689,
                    description: 'GET /api/0/organizations/?member=1',
                    op: 'http',
                    span_id: 'b23703998ae619e7',
                    parent_span_id: 'a934857184bdf5a6',
                    trace_id: '8cbbc19c0f54447ab702f00263262726',
                    status: 'ok',
                    tags: {
                        'http.status_code': '200',
                    },
                    data: {
                        method: 'GET',
                        type: 'fetch',
                        url: '/api/0/organizations/?member=1',
                    },
                },
                numOfSpanChildren: 0,
                treeDepth: 1,
                isLastSibling: false,
                continuingTreeDepths: [],
                showEmbeddedChildren: false,
                toggleEmbeddedChildren: expect.any(Function),
                fetchEmbeddedChildrenState: 'idle',
                toggleSpanGroup: undefined,
            },
            {
                type: 'span',
                span: {
                    timestamp: 1622079937.20331,
                    start_timestamp: 1622079936.907515,
                    description: 'GET /api/0/internal/health/',
                    op: 'http',
                    span_id: 'a453cc713e5baf9c',
                    parent_span_id: 'a934857184bdf5a6',
                    trace_id: '8cbbc19c0f54447ab702f00263262726',
                    status: 'ok',
                    tags: {
                        'http.status_code': '200',
                    },
                    data: {
                        method: 'GET',
                        type: 'fetch',
                        url: '/api/0/internal/health/',
                    },
                },
                numOfSpanChildren: 1,
                treeDepth: 1,
                isLastSibling: true,
                continuingTreeDepths: [],
                showEmbeddedChildren: false,
                toggleEmbeddedChildren: expect.any(Function),
                fetchEmbeddedChildrenState: 'idle',
                toggleSpanGroup: undefined,
            },
            {
                type: 'span',
                span: {
                    timestamp: 1622079936.05839,
                    start_timestamp: 1622079936.048125,
                    description: '/_static/dist/sentry/sentry.541f5b.css',
                    op: 'resource.link',
                    span_id: 'a23f26b939d1a735',
                    parent_span_id: 'a453cc713e5baf9c',
                    trace_id: '8cbbc19c0f54447ab702f00263262726',
                    data: {
                        'Decoded Body Size': 159248,
                        'Encoded Body Size': 159248,
                        'Transfer Size': 275,
                    },
                },
                numOfSpanChildren: 0,
                treeDepth: 2,
                isLastSibling: true,
                continuingTreeDepths: [],
                showEmbeddedChildren: false,
                toggleEmbeddedChildren: expect.any(Function),
                fetchEmbeddedChildrenState: 'idle',
                toggleSpanGroup: undefined,
            },
        ];
        const generateBounds = (0, utils_1.boundsGenerator)({
            traceStartTimestamp: parsedTrace.traceStartTimestamp,
            traceEndTimestamp: parsedTrace.traceEndTimestamp,
            viewStart: 0,
            viewEnd: 1,
        });
        let spans = spanTreeModel.getSpansList({
            operationNameFilters: {
                type: 'no_filter',
            },
            generateBounds,
            treeDepth: 0,
            isLastSibling: true,
            continuingTreeDepths: [],
            hiddenSpanGroups: new Set(),
            spanGroups: new Set(),
            filterSpans: undefined,
            previousSiblingEndTimestamp: undefined,
            event,
            isOnlySibling: true,
            spanGrouping: undefined,
            toggleSpanGroup: undefined,
            showSpanGroup: false,
            addTraceBounds: () => { },
            removeTraceBounds: () => { },
        });
        expect(spans).toEqual(fullWaterfall);
        let mockAddTraceBounds = jest.fn();
        let mockRemoveTraceBounds = jest.fn();
        // embed a child transaction
        let promise = spanTreeModel.toggleEmbeddedChildren({
            addTraceBounds: mockAddTraceBounds,
            removeTraceBounds: mockRemoveTraceBounds,
        })({
            orgSlug: 'sentry',
            eventSlug: 'project:19c403a10af34db2b7d93ad669bb51ed',
        });
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('loading_embedded_transactions');
        yield promise;
        expect(mockAddTraceBounds).toHaveBeenCalled();
        expect(mockRemoveTraceBounds).not.toHaveBeenCalled();
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('idle');
        spans = spanTreeModel.getSpansList({
            operationNameFilters: {
                type: 'no_filter',
            },
            generateBounds,
            treeDepth: 0,
            isLastSibling: true,
            continuingTreeDepths: [],
            hiddenSpanGroups: new Set(),
            spanGroups: new Set(),
            filterSpans: undefined,
            previousSiblingEndTimestamp: undefined,
            event,
            isOnlySibling: true,
            spanGrouping: undefined,
            toggleSpanGroup: undefined,
            showSpanGroup: false,
            addTraceBounds: () => { },
            removeTraceBounds: () => { },
        });
        const fullWaterfallExpected = [...fullWaterfall];
        fullWaterfallExpected.splice(1, 0, 
        // Expect these spans to be embedded
        {
            type: 'span',
            span: {
                trace_id: '61d2d7c5acf448ffa8e2f8f973e2cd36',
                span_id: 'a5702f287954a9ef',
                parent_span_id: 'b23703998ae619e7',
                start_timestamp: 1622079935.86141,
                timestamp: 1622079940.032905,
                op: 'something',
                description: undefined,
                data: {},
                status: 'unknown',
            },
            numOfSpanChildren: 1,
            treeDepth: 1,
            isLastSibling: false,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        }, {
            type: 'span',
            span: {
                trace_id: '61d2d7c5acf448ffa8e2f8f973e2cd36',
                span_id: 'bcbea9f18a11e161',
                parent_span_id: 'a5702f287954a9ef',
                start_timestamp: 1622079936.90689,
                timestamp: 1622079937.227645,
                op: 'child',
                description: 'something child',
                data: {},
                status: 'ok',
            },
            numOfSpanChildren: 0,
            treeDepth: 2,
            isLastSibling: true,
            continuingTreeDepths: [1],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        });
        fullWaterfallExpected[0] = Object.assign({}, fullWaterfallExpected[0]);
        (0, utils_2.assert)(fullWaterfallExpected[0].type === 'span');
        fullWaterfallExpected[0].numOfSpanChildren += 1;
        fullWaterfallExpected[0].showEmbeddedChildren = true;
        expect(spans).toEqual(fullWaterfallExpected);
        mockAddTraceBounds = jest.fn();
        mockRemoveTraceBounds = jest.fn();
        // un-embed a child transaction
        promise = spanTreeModel.toggleEmbeddedChildren({
            addTraceBounds: mockAddTraceBounds,
            removeTraceBounds: mockRemoveTraceBounds,
        })({
            orgSlug: 'sentry',
            eventSlug: 'project:19c403a10af34db2b7d93ad669bb51ed',
        });
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('idle');
        yield promise;
        expect(mockAddTraceBounds).not.toHaveBeenCalled();
        expect(mockRemoveTraceBounds).toHaveBeenCalled();
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('idle');
        spans = spanTreeModel.getSpansList({
            operationNameFilters: {
                type: 'no_filter',
            },
            generateBounds,
            treeDepth: 0,
            isLastSibling: true,
            continuingTreeDepths: [],
            hiddenSpanGroups: new Set(),
            spanGroups: new Set(),
            filterSpans: undefined,
            previousSiblingEndTimestamp: undefined,
            event,
            isOnlySibling: true,
            spanGrouping: undefined,
            toggleSpanGroup: undefined,
            showSpanGroup: false,
            addTraceBounds: () => { },
            removeTraceBounds: () => { },
        });
        expect(spans).toEqual(fullWaterfall);
    }));
    it('toggleEmbeddedChildren - error state', () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const parsedTrace = (0, utils_1.parseTrace)(event);
        const rootSpan = (0, utils_1.generateRootSpan)(parsedTrace);
        const spanTreeModel = new spanTreeModel_1.default(rootSpan, parsedTrace.childSpans, api);
        const promise = spanTreeModel.toggleEmbeddedChildren({
            addTraceBounds: () => { },
            removeTraceBounds: () => { },
        })({
            orgSlug: 'sentry',
            eventSlug: 'project:broken',
        });
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('loading_embedded_transactions');
        yield promise;
        expect(spanTreeModel.fetchEmbeddedChildrenState).toBe('error_fetching_embedded_transactions');
    }));
});
//# sourceMappingURL=spanTreeModel.spec.jsx.map