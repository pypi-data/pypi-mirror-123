Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const parser_1 = require("./parser");
const utils_1 = require("./utils");
/**
 * Renders the parsed query with syntax highlighting.
 */
function HighlightQuery({ parsedQuery, cursorPosition }) {
    const result = renderResult(parsedQuery, cursorPosition !== null && cursorPosition !== void 0 ? cursorPosition : -1);
    return <react_1.Fragment>{result}</react_1.Fragment>;
}
exports.default = HighlightQuery;
function renderResult(result, cursor) {
    return result
        .map(t => renderToken(t, cursor))
        .map((renderedToken, i) => <react_1.Fragment key={i}>{renderedToken}</react_1.Fragment>);
}
function renderToken(token, cursor) {
    switch (token.type) {
        case parser_1.Token.Spaces:
            return token.value;
        case parser_1.Token.Filter:
            return <FilterToken filter={token} cursor={cursor}/>;
        case parser_1.Token.ValueTextList:
        case parser_1.Token.ValueNumberList:
            return <ListToken token={token} cursor={cursor}/>;
        case parser_1.Token.ValueNumber:
            return <NumberToken token={token}/>;
        case parser_1.Token.ValueBoolean:
            return <Boolean>{token.text}</Boolean>;
        case parser_1.Token.ValueIso8601Date:
            return <DateTime>{token.text}</DateTime>;
        case parser_1.Token.LogicGroup:
            return <LogicGroup>{renderResult(token.inner, cursor)}</LogicGroup>;
        case parser_1.Token.LogicBoolean:
            return <LogicBoolean>{token.value}</LogicBoolean>;
        default:
            return token.text;
    }
}
// XXX(epurkhiser): We have to animate `left` here instead of `transform` since
// inline elements cannot be transformed. The filter _must_ be inline to
// support text wrapping.
const shakeAnimation = (0, react_2.keyframes) `
  ${new Array(4)
    .fill(0)
    .map((_, i) => `${i * (100 / 4)}% { left: ${3 * (i % 2 === 0 ? 1 : -1)}px; }`)
    .join('\n')}
`;
const FilterToken = ({ filter, cursor, }) => {
    var _a;
    const isActive = (0, utils_1.isWithinToken)(filter, cursor);
    // This state tracks if the cursor has left the filter token. We initialize it
    // to !isActive in the case where the filter token is rendered without the
    // cursor initally being in it.
    const [hasLeft, setHasLeft] = (0, react_1.useState)(!isActive);
    // Used to trigger the shake animation when the element becomes invalid
    const filterElementRef = (0, react_1.useRef)(null);
    // Trigger the effect when isActive changes to updated whether the cursor has
    // left the token.
    (0, react_1.useEffect)(() => {
        if (!isActive && !hasLeft) {
            setHasLeft(true);
        }
    }, [isActive]);
    const showInvalid = hasLeft && !!filter.invalid;
    const showTooltip = showInvalid && isActive;
    const reduceMotion = (0, framer_motion_1.useReducedMotion)();
    // Trigger the shakeAnimation when showInvalid is set to true. We reset the
    // animation by clearing the style, set it to running, and re-applying the
    // animation
    (0, react_1.useEffect)(() => {
        if (!filterElementRef.current || !showInvalid || reduceMotion) {
            return;
        }
        const style = filterElementRef.current.style;
        style.animation = 'none';
        void filterElementRef.current.offsetTop;
        window.requestAnimationFrame(() => (style.animation = `${shakeAnimation.name} 300ms`));
    }, [showInvalid]);
    return (<tooltip_1.default disabled={!showTooltip} title={(_a = filter.invalid) === null || _a === void 0 ? void 0 : _a.reason} popperStyle={{ maxWidth: '350px' }} forceShow skipWrapper>
      <Filter ref={filterElementRef} active={isActive} invalid={showInvalid}>
        {filter.negated && <Negation>!</Negation>}
        <KeyToken token={filter.key} negated={filter.negated}/>
        {filter.operator && <Operator>{filter.operator}</Operator>}
        <Value>{renderToken(filter.value, cursor)}</Value>
      </Filter>
    </tooltip_1.default>);
};
const KeyToken = ({ token, negated, }) => {
    let value = token.text;
    if (token.type === parser_1.Token.KeyExplicitTag) {
        value = (<ExplicitKey prefix={token.prefix}>
        {token.key.quoted ? `"${token.key.value}"` : token.key.value}
      </ExplicitKey>);
    }
    return <Key negated={!!negated}>{value}:</Key>;
};
const ListToken = ({ token, cursor, }) => (<InList>
    {token.items.map(({ value, separator }) => [
        <ListComma key="comma">{separator}</ListComma>,
        value && renderToken(value, cursor),
    ])}
  </InList>);
const NumberToken = ({ token }) => (<react_1.Fragment>
    {token.value}
    <Unit>{token.unit}</Unit>
  </react_1.Fragment>);
const colorType = (p) => `${p.invalid ? 'invalid' : 'valid'}${p.active ? 'Active' : ''}`;
const Filter = (0, styled_1.default)('span') `
  --token-bg: ${p => p.theme.searchTokenBackground[colorType(p)]};
  --token-border: ${p => p.theme.searchTokenBorder[colorType(p)]};
  --token-value-color: ${p => (p.invalid ? p.theme.red300 : p.theme.blue300)};

  position: relative;
  animation-name: ${shakeAnimation};
`;
const filterCss = (0, react_2.css) `
  background: var(--token-bg);
  border: 0.5px solid var(--token-border);
  padding: ${(0, space_1.default)(0.25)} 0;
`;
const Negation = (0, styled_1.default)('span') `
  ${filterCss};
  border-right: none;
  padding-left: 1px;
  margin-left: -2px;
  font-weight: bold;
  border-radius: 2px 0 0 2px;
  color: ${p => p.theme.red300};
`;
const Key = (0, styled_1.default)('span') `
  ${filterCss};
  border-right: none;
  font-weight: bold;
  ${p => !p.negated
    ? (0, react_2.css) `
          border-radius: 2px 0 0 2px;
          padding-left: 1px;
          margin-left: -2px;
        `
    : (0, react_2.css) `
          border-left: none;
          margin-left: 0;
        `};
`;
const ExplicitKey = (0, styled_1.default)('span') `
  &:before,
  &:after {
    color: ${p => p.theme.subText};
  }
  &:before {
    content: '${p => p.prefix}[';
  }
  &:after {
    content: ']';
  }
`;
const Operator = (0, styled_1.default)('span') `
  ${filterCss};
  border-left: none;
  border-right: none;
  margin: -1px 0;
  color: ${p => p.theme.orange400};
`;
const Value = (0, styled_1.default)('span') `
  ${filterCss};
  border-left: none;
  border-radius: 0 2px 2px 0;
  color: var(--token-value-color);
  margin: -1px -2px -1px 0;
  padding-right: 1px;
`;
const Unit = (0, styled_1.default)('span') `
  font-weight: bold;
  color: ${p => p.theme.green300};
`;
const LogicBoolean = (0, styled_1.default)('span') `
  font-weight: bold;
  color: ${p => p.theme.gray300};
`;
const Boolean = (0, styled_1.default)('span') `
  color: ${p => p.theme.pink300};
`;
const DateTime = (0, styled_1.default)('span') `
  color: ${p => p.theme.green300};
`;
const ListComma = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
`;
const InList = (0, styled_1.default)('span') `
  &:before {
    content: '[';
    font-weight: bold;
    color: ${p => p.theme.purple300};
  }
  &:after {
    content: ']';
    font-weight: bold;
    color: ${p => p.theme.purple300};
  }

  ${Value} {
    color: ${p => p.theme.purple300};
  }
`;
const LogicGroup = (0, styled_1.default)((_a) => {
    var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
    return (<span {...props}>
    <span>(</span>
    {children}
    <span>)</span>
  </span>);
}) `
  > span:first-child,
  > span:last-child {
    position: relative;
    color: transparent;

    &:before {
      position: absolute;
      top: -5px;
      color: ${p => p.theme.orange400};
      font-size: 16px;
      font-weight: bold;
    }
  }

  > span:first-child:before {
    left: -3px;
    content: '(';
  }
  > span:last-child:before {
    right: -3px;
    content: ')';
  }
`;
//# sourceMappingURL=renderer.jsx.map