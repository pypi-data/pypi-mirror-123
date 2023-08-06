Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("./utils");
const List = (0, styled_1.default)((_a) => {
    var { children, className, symbol, initialCounterValue: _initialCounterValue } = _a, props = (0, tslib_1.__rest)(_a, ["children", "className", "symbol", "initialCounterValue"]);
    const getWrapperComponent = () => {
        switch (symbol) {
            case 'numeric':
            case 'colored-numeric':
                return 'ol';
            default:
                return 'ul';
        }
    };
    const Wrapper = getWrapperComponent();
    return (<Wrapper className={className} {...props}>
        {!symbol || typeof symbol === 'string'
            ? children
            : React.Children.map(children, child => {
                if (!React.isValidElement(child)) {
                    return child;
                }
                return React.cloneElement(child, {
                    symbol,
                });
            })}
      </Wrapper>);
}) `
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  ${p => typeof p.symbol === 'string' &&
    utils_1.listSymbol[p.symbol] &&
    (0, utils_1.getListSymbolStyle)(p.theme, p.symbol, p.initialCounterValue)}
`;
exports.default = List;
//# sourceMappingURL=index.jsx.map