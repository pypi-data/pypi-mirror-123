Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const ExternalLink = React.forwardRef(function ExternalLink(_a, ref) {
    var { openInNewTab = true } = _a, props = (0, tslib_1.__rest)(_a, ["openInNewTab"]);
    const anchorProps = openInNewTab ? { target: '_blank', rel: 'noreferrer noopener' } : {};
    return <a ref={ref} {...anchorProps} {...props}/>;
});
exports.default = ExternalLink;
//# sourceMappingURL=externalLink.jsx.map