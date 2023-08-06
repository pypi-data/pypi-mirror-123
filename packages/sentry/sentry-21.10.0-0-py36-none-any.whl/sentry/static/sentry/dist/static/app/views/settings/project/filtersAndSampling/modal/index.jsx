Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errorRuleModal_1 = (0, tslib_1.__importDefault)(require("./errorRuleModal"));
const transactionRuleModal_1 = (0, tslib_1.__importDefault)(require("./transactionRuleModal"));
function Modal(_a) {
    var { type } = _a, props = (0, tslib_1.__rest)(_a, ["type"]);
    if (type === 'error') {
        return <errorRuleModal_1.default {...props}/>;
    }
    return <transactionRuleModal_1.default {...props}/>;
}
exports.default = Modal;
//# sourceMappingURL=index.jsx.map