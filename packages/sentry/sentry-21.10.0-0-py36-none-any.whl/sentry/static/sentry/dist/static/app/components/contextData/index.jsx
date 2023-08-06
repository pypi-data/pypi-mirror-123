Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const isNumber_1 = (0, tslib_1.__importDefault)(require("lodash/isNumber"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const utils_1 = require("app/utils");
const toggle_1 = (0, tslib_1.__importDefault)(require("./toggle"));
const utils_2 = require("./utils");
function getValueWithAnnotatedText(v, meta) {
    return <annotatedText_1.default value={v} meta={meta}/>;
}
class ContextData extends React.Component {
    renderValue(value) {
        const { preserveQuotes, meta, withAnnotatedText, jsonConsts, maxDefaultDepth } = this.props;
        const maxDepth = maxDefaultDepth !== null && maxDefaultDepth !== void 0 ? maxDefaultDepth : 2;
        // eslint-disable-next-line @typescript-eslint/no-shadow
        function walk(value, depth) {
            let i = 0;
            const children = [];
            if (value === null) {
                return <span className="val-null">{jsonConsts ? 'null' : 'None'}</span>;
            }
            if (value === true || value === false) {
                return (<span className="val-bool">
            {jsonConsts ? (value ? 'true' : 'false') : value ? 'True' : 'False'}
          </span>);
            }
            if ((0, isString_1.default)(value)) {
                const valueInfo = (0, utils_2.analyzeStringForRepr)(value);
                const valueToBeReturned = withAnnotatedText
                    ? getValueWithAnnotatedText(valueInfo.repr, meta)
                    : valueInfo.repr;
                const out = [
                    <span key="value" className={(valueInfo.isString ? 'val-string' : '') +
                            (valueInfo.isStripped ? ' val-stripped' : '') +
                            (valueInfo.isMultiLine ? ' val-string-multiline' : '')}>
            {preserveQuotes ? `"${valueToBeReturned}"` : valueToBeReturned}
          </span>,
                ];
                if (valueInfo.isString && (0, utils_1.isUrl)(value)) {
                    out.push(<externalLink_1.default key="external" href={value} className="external-icon">
              <StyledIconOpen size="xs"/>
            </externalLink_1.default>);
                }
                return out;
            }
            if ((0, isNumber_1.default)(value)) {
                const valueToBeReturned = withAnnotatedText && meta ? getValueWithAnnotatedText(value, meta) : value;
                return <span>{valueToBeReturned}</span>;
            }
            if ((0, isArray_1.default)(value)) {
                for (i = 0; i < value.length; i++) {
                    children.push(<span className="val-array-item" key={i}>
              {walk(value[i], depth + 1)}
              {i < value.length - 1 ? (<span className="val-array-sep">{', '}</span>) : null}
            </span>);
                }
                return (<span className="val-array">
            <span className="val-array-marker">{'['}</span>
            <toggle_1.default highUp={depth <= maxDepth} wrapClassName="val-array-items">
              {children}
            </toggle_1.default>
            <span className="val-array-marker">{']'}</span>
          </span>);
            }
            if (React.isValidElement(value)) {
                return value;
            }
            const keys = Object.keys(value);
            keys.sort(utils_2.naturalCaseInsensitiveSort);
            for (i = 0; i < keys.length; i++) {
                const key = keys[i];
                children.push(<span className="val-dict-pair" key={key}>
            <span className="val-dict-key">
              <span className="val-string">{preserveQuotes ? `"${key}"` : key}</span>
            </span>
            <span className="val-dict-col">{': '}</span>
            <span className="val-dict-value">
              {walk(value[key], depth + 1)}
              {i < keys.length - 1 ? <span className="val-dict-sep">{', '}</span> : null}
            </span>
          </span>);
            }
            return (<span className="val-dict">
          <span className="val-dict-marker">{'{'}</span>
          <toggle_1.default highUp={depth <= maxDepth - 1} wrapClassName="val-dict-items">
            {children}
          </toggle_1.default>
          <span className="val-dict-marker">{'}'}</span>
        </span>);
        }
        return walk(value, 0);
    }
    render() {
        const _a = this.props, { data, preserveQuotes: _preserveQuotes, withAnnotatedText: _withAnnotatedText, meta: _meta, children } = _a, other = (0, tslib_1.__rest)(_a, ["data", "preserveQuotes", "withAnnotatedText", "meta", "children"]);
        return (<pre {...other}>
        {this.renderValue(data)}
        {children}
      </pre>);
    }
}
ContextData.defaultProps = {
    data: null,
    withAnnotatedText: false,
};
const StyledIconOpen = (0, styled_1.default)(icons_1.IconOpen) `
  position: relative;
  top: 1px;
`;
exports.default = ContextData;
//# sourceMappingURL=index.jsx.map