Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@sentry/react");
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const sentry_loader_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/sentry-loader.svg"));
function renderLogoSpinner() {
    return <img src={sentry_loader_svg_1.default}/>;
}
function LoadingIndicator(props) {
    const { hideMessage, mini, triangle, overlay, dark, children, finished, className, style, relative, size, hideSpinner, } = props;
    const cx = (0, classnames_1.default)(className, {
        overlay,
        dark,
        loading: true,
        mini,
        triangle,
    });
    const loadingCx = (0, classnames_1.default)({
        relative,
        'loading-indicator': true,
        'load-complete': finished,
    });
    let loadingStyle = {};
    if (size) {
        loadingStyle = {
            width: size,
            height: size,
        };
    }
    return (<div className={cx} style={style} data-test-id="loading-indicator">
      {!hideSpinner && (<div className={loadingCx} style={loadingStyle}>
          {triangle && renderLogoSpinner()}
          {finished ? <div className="checkmark draw" style={style}/> : null}
        </div>)}
      {!hideMessage && <div className="loading-message">{children}</div>}
    </div>);
}
exports.default = (0, react_1.withProfiler)(LoadingIndicator, {
    includeUpdates: false,
});
//# sourceMappingURL=loadingIndicator.jsx.map