Object.defineProperty(exports, "__esModule", { value: true });
exports.saveToSourceGroupData = exports.fetchSourceGroupData = void 0;
const types_1 = require("../types");
const utils_1 = require("../utils");
const localStorage_1 = require("./localStorage");
function fetchSourceGroupData() {
    const fetchedSourceGroupData = (0, localStorage_1.fetchFromStorage)();
    if (!fetchedSourceGroupData) {
        const sourceGroupData = {
            eventId: '',
            sourceSuggestions: utils_1.valueSuggestions,
        };
        (0, localStorage_1.saveToStorage)(sourceGroupData);
        return sourceGroupData;
    }
    return fetchedSourceGroupData;
}
exports.fetchSourceGroupData = fetchSourceGroupData;
function saveToSourceGroupData(eventId, sourceSuggestions = utils_1.valueSuggestions) {
    switch (eventId.status) {
        case types_1.EventIdStatus.LOADING:
            break;
        case types_1.EventIdStatus.LOADED:
            (0, localStorage_1.saveToStorage)({ eventId: eventId.value, sourceSuggestions });
            break;
        default:
            (0, localStorage_1.saveToStorage)({ eventId: '', sourceSuggestions });
    }
}
exports.saveToSourceGroupData = saveToSourceGroupData;
//# sourceMappingURL=utils.jsx.map