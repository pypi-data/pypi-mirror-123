Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
exports.default = (0, react_1.forwardRef)(function MultiSelectControl(props, ref) {
    return <selectControl_1.default forwardedRef={ref} {...props} multiple/>;
});
//# sourceMappingURL=multiSelectControl.jsx.map