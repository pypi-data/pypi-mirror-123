Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const locale_1 = require("app/locale");
const redaction_1 = (0, tslib_1.__importDefault)(require("./redaction"));
// If you find yourself modifying this component to fix some tooltip bug,
// consider that `meta` is not properly passed into this component in the
// first place. It's much more likely that `withMeta` is buggy or improperly
// used than that this component has a bug.
const ValueElement = ({ value, meta }) => {
    var _a, _b;
    if (value && meta) {
        return <redaction_1.default>{value}</redaction_1.default>;
    }
    if ((_a = meta === null || meta === void 0 ? void 0 : meta.err) === null || _a === void 0 ? void 0 : _a.length) {
        return (<redaction_1.default withoutBackground>
        <i>{`<${(0, locale_1.t)('invalid')}>`}</i>
      </redaction_1.default>);
    }
    if ((_b = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _b === void 0 ? void 0 : _b.length) {
        return (<redaction_1.default>
        <i>{`<${(0, locale_1.t)('redacted')}>`}</i>
      </redaction_1.default>);
    }
    if (React.isValidElement(value)) {
        return value;
    }
    return (<React.Fragment>
      {typeof value === 'object' || typeof value === 'boolean'
            ? JSON.stringify(value)
            : value}
    </React.Fragment>);
};
exports.default = ValueElement;
//# sourceMappingURL=valueElement.jsx.map