Object.defineProperty(exports, "__esModule", { value: true });
exports.FullValue = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class Truncate extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isExpanded: false,
        };
        this.onFocus = () => {
            const { value, maxLength } = this.props;
            if (value.length <= maxLength) {
                return;
            }
            this.setState({ isExpanded: true });
        };
        this.onBlur = () => {
            if (this.state.isExpanded) {
                this.setState({ isExpanded: false });
            }
        };
    }
    render() {
        const { className, leftTrim, trimRegex, minLength, maxLength, value, expandable, expandDirection, } = this.props;
        const isTruncated = value.length > maxLength;
        let shortValue = '';
        if (isTruncated) {
            const slicedValue = leftTrim
                ? value.slice(value.length - (maxLength - 4), value.length)
                : value.slice(0, maxLength - 4);
            // Try to trim to values from the regex
            if (trimRegex && leftTrim) {
                const valueIndex = slicedValue.search(trimRegex);
                shortValue = (<span>
            …{' '}
            {valueIndex > 0 && valueIndex <= maxLength - minLength
                        ? slicedValue.slice(slicedValue.search(trimRegex), slicedValue.length)
                        : slicedValue}
          </span>);
            }
            else if (trimRegex && !leftTrim) {
                const matches = slicedValue.match(trimRegex);
                let lastIndex = matches
                    ? slicedValue.lastIndexOf(matches[matches.length - 1]) + 1
                    : slicedValue.length;
                if (lastIndex <= minLength) {
                    lastIndex = slicedValue.length;
                }
                shortValue = <span>{slicedValue.slice(0, lastIndex)} …</span>;
            }
            else if (leftTrim) {
                shortValue = <span>… {slicedValue}</span>;
            }
            else {
                shortValue = <span>{slicedValue} …</span>;
            }
        }
        else {
            shortValue = value;
        }
        return (<Wrapper className={className} onMouseOver={expandable ? this.onFocus : undefined} onMouseOut={expandable ? this.onBlur : undefined} onFocus={expandable ? this.onFocus : undefined} onBlur={expandable ? this.onBlur : undefined}>
        <span>{shortValue}</span>
        {isTruncated && (<exports.FullValue expanded={this.state.isExpanded} expandDirection={expandDirection}>
            {value}
          </exports.FullValue>)}
      </Wrapper>);
    }
}
Truncate.defaultProps = {
    className: '',
    minLength: 15,
    maxLength: 50,
    leftTrim: false,
    expandable: true,
    expandDirection: 'right',
};
const Wrapper = (0, styled_1.default)('span') `
  position: relative;
`;
exports.FullValue = (0, styled_1.default)('span') `
  display: none;
  position: absolute;
  background: ${p => p.theme.background};
  padding: ${(0, space_1.default)(0.5)};
  border: 1px solid ${p => p.theme.innerBorder};
  white-space: nowrap;
  border-radius: ${(0, space_1.default)(0.5)};
  top: -5px;
  ${p => p.expandDirection === 'left' && 'right: -5px;'}
  ${p => p.expandDirection === 'right' && 'left: -5px;'}

  ${p => p.expanded &&
    `
    z-index: ${p.theme.zIndex.truncationFullValue};
    display: block;
    `}
`;
exports.default = Truncate;
//# sourceMappingURL=truncate.jsx.map