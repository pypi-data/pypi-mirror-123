Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class ArrayValue extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            expanded: false,
        };
        this.handleToggle = () => {
            this.setState(prevState => ({
                expanded: !prevState.expanded,
            }));
        };
    }
    render() {
        const { expanded } = this.state;
        const { value } = this.props;
        return (<ArrayContainer expanded={expanded}>
        {expanded &&
                value
                    .slice(0, value.length - 1)
                    .map((item, i) => <ArrayItem key={`${i}:${item}`}>{item}</ArrayItem>)}
        <ArrayItem>{value.slice(-1)[0]}</ArrayItem>
        {value.length > 1 ? (<ButtonContainer>
            <button onClick={this.handleToggle}>
              {expanded ? (0, locale_1.t)('[collapse]') : (0, locale_1.t)('[+%s more]', value.length - 1)}
            </button>
          </ButtonContainer>) : null}
      </ArrayContainer>);
    }
}
const ArrayContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: ${p => (p.expanded ? 'column' : 'row')};

  & button {
    background: none;
    border: 0;
    outline: none;
    padding: 0;
    cursor: pointer;
    color: ${p => p.theme.blue300};
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const ArrayItem = (0, styled_1.default)('span') `
  flex-shrink: 1;
  display: block;

  ${overflowEllipsis_1.default};
  width: unset;
`;
const ButtonContainer = (0, styled_1.default)('div') `
  white-space: nowrap;
`;
exports.default = ArrayValue;
//# sourceMappingURL=arrayValue.jsx.map