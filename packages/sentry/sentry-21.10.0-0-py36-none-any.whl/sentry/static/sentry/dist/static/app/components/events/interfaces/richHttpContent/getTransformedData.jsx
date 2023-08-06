Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/utils");
function getTransformedData(data) {
    if (Array.isArray(data)) {
        return data
            .filter(dataValue => {
            if (typeof dataValue === 'string') {
                return !!dataValue;
            }
            return (0, utils_1.defined)(dataValue);
        })
            .map(dataValue => {
            if (Array.isArray(dataValue)) {
                return dataValue;
            }
            if (typeof data === 'object') {
                return Object.keys(dataValue).flatMap(key => [key, dataValue[key]]);
            }
            return dataValue;
        });
    }
    if (typeof data === 'object') {
        return Object.keys(data).map(key => [key, data[key]]);
    }
    return [];
}
exports.default = getTransformedData;
//# sourceMappingURL=getTransformedData.jsx.map