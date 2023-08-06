Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const React = (0, tslib_1.__importStar)(require("react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const selectText_1 = require("app/utils/selectText");
const AutoSelectText = (_a, forwardedRef) => {
    var { children, className } = _a, props = (0, tslib_1.__rest)(_a, ["children", "className"]);
    const element = (0, react_1.useRef)(null);
    // We need to expose a selectText method to parent components
    // and need an imperitive ref handle.
    (0, react_1.useImperativeHandle)(forwardedRef, () => ({
        selectText: () => handleClick(),
    }));
    function handleClick() {
        if (!element.current) {
            return;
        }
        (0, selectText_1.selectText)(element.current);
    }
    // use an inner span here for the selection as otherwise the selectText
    // function will create a range that includes the entire part of the
    // div (including the div itself) which causes newlines to be selected
    // in chrome.
    return (<div {...props} onClick={handleClick} className={(0, classnames_1.default)('auto-select-text', className)}>
      <span ref={element}>{children}</span>
    </div>);
};
exports.default = (0, react_1.forwardRef)(AutoSelectText);
//# sourceMappingURL=autoSelectText.jsx.map