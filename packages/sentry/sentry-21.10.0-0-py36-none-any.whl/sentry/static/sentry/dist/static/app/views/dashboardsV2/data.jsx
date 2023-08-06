Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_STATS_PERIOD = exports.INTERVAL_CHOICES = exports.DISPLAY_TYPE_CHOICES = exports.EMPTY_DASHBOARD = void 0;
const locale_1 = require("app/locale");
exports.EMPTY_DASHBOARD = {
    id: '',
    dateCreated: '',
    createdBy: undefined,
    title: (0, locale_1.t)('Untitled dashboard'),
    widgets: [],
};
exports.DISPLAY_TYPE_CHOICES = [
    { label: (0, locale_1.t)('Area Chart'), value: 'area' },
    { label: (0, locale_1.t)('Bar Chart'), value: 'bar' },
    { label: (0, locale_1.t)('Line Chart'), value: 'line' },
    { label: (0, locale_1.t)('Table'), value: 'table' },
    { label: (0, locale_1.t)('World Map'), value: 'world_map' },
    { label: (0, locale_1.t)('Big Number'), value: 'big_number' },
    { label: (0, locale_1.t)('Top Events'), value: 'top_n' },
];
exports.INTERVAL_CHOICES = [
    { label: (0, locale_1.t)('1 Minute'), value: '1m' },
    { label: (0, locale_1.t)('5 Minutes'), value: '5m' },
    { label: (0, locale_1.t)('15 Minutes'), value: '15m' },
    { label: (0, locale_1.t)('30 Minutes'), value: '30m' },
    { label: (0, locale_1.t)('1 Hour'), value: '1h' },
    { label: (0, locale_1.t)('1 Day'), value: '1d' },
];
exports.DEFAULT_STATS_PERIOD = '24h';
//# sourceMappingURL=data.jsx.map