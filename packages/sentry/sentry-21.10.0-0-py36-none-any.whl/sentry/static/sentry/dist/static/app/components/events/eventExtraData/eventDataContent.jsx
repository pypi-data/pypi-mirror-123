Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const utils_1 = require("app/utils");
const getEventExtraDataKnownData_1 = (0, tslib_1.__importDefault)(require("./getEventExtraDataKnownData"));
const EventDataContent = ({ data, raw }) => {
    if (!(0, utils_1.defined)(data)) {
        return null;
    }
    return <contextBlock_1.default data={(0, getEventExtraDataKnownData_1.default)(data)} raw={raw}/>;
};
exports.default = EventDataContent;
//# sourceMappingURL=eventDataContent.jsx.map