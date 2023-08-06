Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
function getKnownData(data) {
    return Object.entries(data)
        .filter(([k]) => k !== 'type' && k !== 'title')
        .map(([key, value]) => ({
        key,
        subject: key,
        value,
    }));
}
const DefaultContextType = ({ data }) => <contextBlock_1.default data={getKnownData(data)}/>;
exports.default = DefaultContextType;
//# sourceMappingURL=default.jsx.map