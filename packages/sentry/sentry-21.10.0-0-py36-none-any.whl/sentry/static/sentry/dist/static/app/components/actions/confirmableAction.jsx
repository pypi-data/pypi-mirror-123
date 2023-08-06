Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
function ConfirmableAction(_a) {
    var { shouldConfirm, children } = _a, props = (0, tslib_1.__rest)(_a, ["shouldConfirm", "children"]);
    if (shouldConfirm) {
        return <confirm_1.default {...props}>{children}</confirm_1.default>;
    }
    return <React.Fragment>{children}</React.Fragment>;
}
exports.default = ConfirmableAction;
//# sourceMappingURL=confirmableAction.jsx.map