Object.defineProperty(exports, "__esModule", { value: true });
exports.formattedValue = void 0;
const formatters_1 = require("app/utils/formatters");
function formattedValue(record, value) {
    if (record && record.type === 'duration') {
        return (0, formatters_1.getDuration)(value / 1000, 3);
    }
    else if (record && record.type === 'integer') {
        return value.toFixed(0);
    }
    return value.toFixed(3);
}
exports.formattedValue = formattedValue;
//# sourceMappingURL=index.jsx.map