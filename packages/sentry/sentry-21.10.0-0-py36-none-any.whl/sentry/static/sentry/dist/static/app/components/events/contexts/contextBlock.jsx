Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const ContextBlock = ({ data, raw = false }) => {
    if (data.length === 0) {
        return null;
    }
    return (<errorBoundary_1.default mini>
      <keyValueList_1.default data={data} raw={raw} isContextData/>
    </errorBoundary_1.default>);
};
exports.default = ContextBlock;
//# sourceMappingURL=contextBlock.jsx.map